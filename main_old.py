from typing import Tuple

import pygame as pg


def is_border_pos(pos: Tuple[int, int]) -> bool:
    return (
        pos[0] == 0
        or pos[1] == 0
        or pos[0] == screen.get_width() - 1
        or pos[1] == screen.get_height() - 1
    )


def draw() -> None:
    screen.fill("white")

    for line in line_list:
        for i in range(len(line) - 1):
            pg.draw.line(screen, "black", line[i], line[i + 1], 3)

    # Draw current line
    for i in range(len(current_line) - 1):
        pg.draw.line(screen, "black", current_line[i], current_line[i + 1], 3)

    screen.blit(font.render(fps_draw, True, "Black"), (0, 0))


pg.init()
pg.display.set_caption("Drawdle")
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()

FPS_DRAW_EVENT = pg.USEREVENT + 1
pg.time.set_timer(FPS_DRAW_EVENT, 1000)
fps_draw = ""

font = pg.font.Font(size=32)

is_drawing = False

line_list = list()
current_line = list()

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == FPS_DRAW_EVENT:
            fps_draw = str(int(clock.get_fps()))

    # Start of line
    if pg.mouse.get_pressed()[0] and not is_drawing:
        is_drawing = True

    # End of line
    if (
        not pg.mouse.get_pressed()[0] or is_border_pos(pg.mouse.get_pos())
    ) and is_drawing:
        # If on border, add current mouse position as last point on line
        if is_border_pos(pg.mouse.get_pos()):
            current_line.append(pg.mouse.get_pos())
        is_drawing = False
        line_list.append(current_line)
        current_line = list()

    if is_drawing:
        current_line.append(pg.mouse.get_pos())

    draw()

    clock.tick()

    pg.display.update()

pg.quit()
