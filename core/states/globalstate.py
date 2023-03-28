import pygame as pg

from core import timers, clock
from core.states.state import State


class GlobalState(State):
    """
    Holds global variables, handles global events and draws global objects.
    """
    name = "global"

    def __init__(self) -> None:
        super().__init__()
        self.fps_draw = ""
        self.font = pg.font.Font(size=32)

    def handle_event(self, event: pg.event.Event) -> None:
        if event.type == timers.FPS_DRAW_EVENT:
            self.fps_draw = str(int(clock.get_clock().get_fps()))

    def draw(self, screen: pg.Surface) -> None:
        screen.blit(self.font.render(self.fps_draw, True, "Black"), (0, 0))

    def update(self, dt: int) -> None:
        pass

    def teardown(self) -> None:
        pass
