from typing import Tuple

from core.screen import get_screen


def is_border_pos(pos: Tuple[int, int]) -> bool:
    screen = get_screen()
    return (
        pos[0] == 0
        or pos[1] == 0
        or pos[0] == screen.get_width() - 1
        or pos[1] == screen.get_height() - 1
    )
