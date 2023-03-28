import pygame as pg

from core.states.state import State
from core import utils


class CanvasState(State):
    """
    State holding drawing canvas.
    """
    name = "canvas"

    def __init__(self) -> None:
        super().__init__()
        self._brush_width = 3
        self._brush_colour = "black"
        self._lines = []
        self._current_line = []
        self._is_drawing = False


    def handle_event(self, event: pg.event.Event) -> None:
        pass

    def draw(self, screen: pg.Surface) -> None:
        screen.fill("white")

        for line in self._lines:
            for i in range(len(line)-1):
                pg.draw.line(screen, self._brush_colour, line[i], line[i+1], self._brush_width)

        # Draw current line
        for i in range(len(self._current_line)-1):
            pg.draw.line(screen, self._brush_colour, self._current_line[i], self._current_line[i+1], self._brush_width)

    def update(self, dt: int) -> None:
        # Start of line
        if self._is_line_start():
            self._is_drawing = True

        # End of line
        if self._is_line_end():
            # If on border, add current mouse position as last point on line
            if utils.is_border_pos(pg.mouse.get_pos()):
                self._current_line.append(pg.mouse.get_pos())
            self._is_drawing = False
            self._lines.append(self._current_line)
            self._current_line = list()

        if self._is_drawing:
            self._current_line.append(pg.mouse.get_pos())

    def _is_line_start(self):
        return pg.mouse.get_pressed()[0] and not self._is_drawing
    
    def _is_line_end(self):
        return (not pg.mouse.get_pressed()[0] or utils.is_border_pos(pg.mouse.get_pos())) and self._is_drawing

    def teardown(self) -> None:
        pass