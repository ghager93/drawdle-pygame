import pygame as pg

from core.states.state import State
from core.states.canvas import CanvasState
from core.states.globalstate import GlobalState


pg.init()
pg.display.set_caption("Drawdle")
screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
fps = 60.0
dt = 0

FPS_DRAW_EVENT = pg.USEREVENT + 1
pg.time.set_timer(FPS_DRAW_EVENT, 1000)

state_dict = {
    GlobalState.name: GlobalState(),
    CanvasState.name: CanvasState(),
}


global_state: State = state_dict[GlobalState.name]
current_state_name: str = CanvasState.name
current_state: State = state_dict[current_state_name]

is_running = True
while is_running:
    # Handle events
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False
        global_state.handle_event(event)
        current_state.handle_event(event)

    # Update
    global_state.update(dt)
    current_state.update(dt)

    # Draw
    global_state.draw(screen)
    current_state.draw(screen)

    pg.display.update()

    dt = clock.tick(fps)

pg.quit()
