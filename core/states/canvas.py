import pygame as pg

from datetime import datetime

from core import utils
from core.states.state import State
from core.logic import linefuncs
from core.logic import export

class CanvasState(State):
    """
    State holding drawing canvas.
    """

    name = "canvas"

    def __init__(self) -> None:
        super().__init__()

        self._screen = pg.display.get_surface()

        self._brush_width = 3
        self._brush_colour = "black"

        self._is_drawing = False

        _canvas_size = self._screen.get_height() - 100, self._screen.get_height() - 100
        self._canvas_rect = pg.Rect((50, 50), _canvas_size)

        self._mini_canvas_size = 256, 256
        self._mini_canvas_rect = pg.Rect((1000, 50), self._mini_canvas_size)

        self._lines = []
        self._current_line = []
        self._decimated_lines = []
        self._normalised_lines = []
        self._mini_lines = []

        self._epsilon = 2

        self._font = pg.font.Font(None, size=32)

        self._is_mouse_on_canvas = False

        self._drawing_bound_rect = None

        self._export_rect = pg.Rect((0, 0), self._mini_canvas_size)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_n and self._epsilon > 0:
                self._epsilon -= 1
                print("epsilon:", self._epsilon)
                self._recalculate_mini_lines()
            elif event.key == pg.K_m:
                self._epsilon += 1
                print("epsilon:", self._epsilon)
                self._recalculate_mini_lines()
            elif event.key == pg.K_s:
                export_lines = [linefuncs.round_line_to_int(linefuncs.scale_line(line, self._export_rect)) for line in self._normalised_lines]
                filename = datetime.now().strftime("%Y%m%d-%H%M%S") + ".bmp"
                export.to_bmp(filename, self._mini_canvas_size, export_lines)
                print("Image saved as", filename)

    def draw(self, screen: pg.Surface) -> None:
        pg.draw.rect(screen, "white", self._canvas_rect)

        for line in self._lines:
            for i in range(len(line) - 1):
                pg.draw.line(
                    screen, self._brush_colour, line[i], line[i + 1], self._brush_width
                )

        # Draw current line
        for i in range(len(self._current_line) - 1):
            pg.draw.line(
                screen,
                self._brush_colour,
                self._current_line[i],
                self._current_line[i + 1],
                self._brush_width,
            )

        if self._drawing_bound_rect:
            pg.draw.rect(screen, "red", self._square_bound_rect, width=1)

        pg.draw.rect(screen, "white", self._mini_canvas_rect)

        for line in self._mini_lines:
            for i in range(len(line) - 1):
                pg.draw.line(
                    screen, self._brush_colour, line[i], line[i + 1], self._brush_width
                )

        screen.blit(
            self._font.render(str(self._is_mouse_on_canvas), True, "black"), (50, 0)
        )

    def update(self, dt: int) -> None:
        mouse_pos = pg.mouse.get_pos()
        self._is_mouse_on_canvas = self._canvas_rect.collidepoint(mouse_pos)

        # Start of line
        if self._is_line_start():
            self._is_drawing = True

        # End of line
        if self._is_line_end():
            # If on border, add current mouse position as last point on line
            if utils.is_border_pos(mouse_pos):
                self._current_line.append(mouse_pos)
            self._is_drawing = False
            self._lines.append(self._current_line)

            line_bound = linefuncs.calculate_line_bounds(self._current_line)
            if self._drawing_bound_rect:
                self._update_drawing_bound_rect(line_bound)
            else:
                self._drawing_bound_rect = pg.Rect(
                    line_bound[0],
                    line_bound[2],
                    line_bound[1] - line_bound[0],
                    line_bound[3] - line_bound[2],
                )

            self._decimated_lines.append(
                linefuncs.decimate_line(self._current_line, self._epsilon)
            )
            self._normalised_lines = [
                linefuncs.normalise_line(line, self._square_bound_rect)
                for line in self._decimated_lines
            ]
            self._mini_lines = [
                linefuncs.scale_line(line, self._mini_canvas_rect)
                for line in self._normalised_lines
            ]
            self._mini_lines = [
                linefuncs.round_line_to_int(line)
                for line in self._mini_lines
            ]
            self._current_line = list()

        if self._is_drawing:
            self._current_line.append(mouse_pos)

    def _is_line_start(self):
        return (
            self._is_mouse_on_canvas
            and pg.mouse.get_pressed()[0]
            and not self._is_drawing
        )

    def _is_line_end(self):
        return (
            not pg.mouse.get_pressed()[0] or not self._is_mouse_on_canvas
        ) and self._is_drawing

    def _recalculate_mini_lines(self):
        self._mini_lines = [
            linefuncs.decimate_line(
                linefuncs.scale_line(line, self._mini_canvas_rect), self._epsilon
            )
            for line in self._normalised_lines
        ]

    def _update_drawing_bound_rect(self, new_bound):
        updated_bound = [
            self._drawing_bound_rect.x,
            self._drawing_bound_rect.w + self._drawing_bound_rect.x,
            self._drawing_bound_rect.y,
            self._drawing_bound_rect.h + self._drawing_bound_rect.y,
        ]
        if new_bound[0] < updated_bound[0]:
            updated_bound[0] = new_bound[0]
        if new_bound[1] > updated_bound[1]:
            updated_bound[1] = new_bound[1]
        if new_bound[2] < updated_bound[2]:
            updated_bound[2] = new_bound[2]
        if new_bound[3] > updated_bound[3]:
            updated_bound[3] = new_bound[3]

        self._drawing_bound_rect.x = updated_bound[0]
        self._drawing_bound_rect.w = updated_bound[1] - updated_bound[0]
        self._drawing_bound_rect.y = updated_bound[2]
        self._drawing_bound_rect.h = updated_bound[3] - updated_bound[2]

    @property
    def _square_bound_rect(self):
        width = max(self._drawing_bound_rect.w, self._drawing_bound_rect.h)
        return pg.Rect((self._drawing_bound_rect.x, self._drawing_bound_rect.y), (width, width))

    def teardown(self) -> None:
        pass
