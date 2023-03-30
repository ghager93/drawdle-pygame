import abc

import pygame as pg


class State:
    """
    Prototype for state classes.
    """

    def __init__(self, persistant: dict = {}) -> None:
        self.start_time = 0.0
        self.now = 0.0
        self.done = False
        self.quit = False
        self.persist = persistant

    @abc.abstractmethod
    def handle_event(self, event: pg.event.Event) -> None:
        return NotImplementedError

    @abc.abstractmethod
    def draw(self, screen: pg.Surface) -> None:
        return NotImplementedError

    @abc.abstractmethod
    def update(self, dt: int) -> None:
        return NotImplementedError

    @abc.abstractmethod
    def teardown(self) -> None:
        return NotImplementedError

    @abc.abstractmethod
    def transition_in(self, now: float = 0.0, persistant: dict = {}) -> None:
        self.start_time = now
        self.persist = persistant

    @abc.abstractmethod
    def transition_out(self) -> dict:
        self.done = False
        return self.persist
