"""
Layout helpers. All position math lives here — never in screen files.

Usage:
    from src.utils.layout import center_rect, stack_rects, anchor

    btn_rect = center_rect(width=200, height=40, within=(SCREEN_WIDTH, SCREEN_HEIGHT))
    rects = stack_rects(count=4, item_h=40, gap=12, top=300, screen_w=SCREEN_WIDTH)
"""
import pygame
import src.config.config as cfg


def center_rect(width: int, height: int, within: tuple = None) -> pygame.Rect:
    """Return a Rect centered in `within` (defaults to full screen)."""
    w, h = within or (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    return pygame.Rect((w - width) // 2, (h - height) // 2, width, height)


def stack_rects(count: int, item_w: int, item_h: int, gap: int,
                top: int, screen_w: int = None) -> list:
    """Return a vertical stack of `count` Rects centered horizontally."""
    sw = screen_w or cfg.SCREEN_WIDTH
    x = (sw - item_w) // 2
    return [pygame.Rect(x, top + i * (item_h + gap), item_w, item_h) for i in range(count)]


def anchor(obj_w: int, obj_h: int,
           h: str = 'center', v: str = 'center',
           margin: int = 0, within: tuple = None) -> tuple:
    """
    Return (x, y) for an object anchored within a container.
    h: 'left' | 'center' | 'right'
    v: 'top'  | 'center' | 'bottom'
    """
    cw, ch = within or (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
    x = {'left': margin, 'center': (cw - obj_w) // 2, 'right': cw - obj_w - margin}[h]
    y = {'top': margin, 'center': (ch - obj_h) // 2, 'bottom': ch - obj_h - margin}[v]
    return x, y
