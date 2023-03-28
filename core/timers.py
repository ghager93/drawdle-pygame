import pygame as pg


FPS_DRAW_EVENT = pg.USEREVENT + 1


def init_timers() -> None:
    pg.time.set_timer(FPS_DRAW_EVENT, 1000)
