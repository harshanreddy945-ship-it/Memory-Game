import pygame

TILE_SIZE = 80
PADDING = 10
TOP_PANEL_HEIGHT = 100

BG_COLOR = (30, 30, 30)
TILE_FACE_DOWN = (70, 70, 120)
TILE_FACE_UP = (200, 200, 240)
TILE_MATCHED = (100, 200, 100)
TEXT_COLOR = (255, 255, 255)
TEXT_DARK = (0, 0, 0)

_screen = None
_font = None
_small_font = None
_rows = 0
_cols = 0
_grid_origin = (0, 0)


def init_ui(rows, cols, window_title="Memory Match"):

    global _screen, _font, _small_font, _rows, _cols, _grid_origin

    _rows, _cols = rows, cols

    pygame.init()
    pygame.display.set_caption(window_title)

    width = cols * (TILE_SIZE + PADDING) + PADDING
    height = TOP_PANEL_HEIGHT + rows * (TILE_SIZE + PADDING) + PADDING

    _screen = pygame.display.set_mode((width, height))

    _font = pygame.font.SysFont(None, 40)
    _small_font = pygame.font.SysFont(None, 26)

    _grid_origin = (PADDING, TOP_PANEL_HEIGHT)


def draw_ui(board, stats, elapsed_time, difficulty="easy", best_time=None):

    _screen.fill(BG_COLOR)

    moves = stats.get("moves_count", 0)
    pairs_found = stats.get("pairs_found", 0)
    total_pairs = stats.get("total_pairs", 0)
    status = stats.get("status", "")

    line1 = f"Difficulty: {difficulty}   Time: {elapsed_time:.1f}s"
    line2 = f"Moves: {moves}   Pairs: {pairs_found}/{total_pairs}"
    if best_time is not None:
        line3 = f"Best: {best_time:.1f}s"
    else:
        line3 = "Best: --"

    _draw_text(line1, 10)
    _draw_text(line2, 35)
    _draw_text(line3, 60)

    if status == "game_over":
        _draw_text("GAME OVER! Press R to restart.", 60, center_x=True)

    for r, row in enumerate(board):
        for c, tile in enumerate(row):
            _draw_tile(r, c, tile)

    pygame.display.flip()


def _draw_text(text, y, center_x=False):
    surf = _small_font.render(text, True, TEXT_COLOR)
    rect = surf.get_rect()
    if center_x:
        rect.centerx = _screen.get_width() // 2
    else:
        rect.x = PADDING
    rect.y = y
    _screen.blit(surf, rect)


def _draw_tile(r, c, tile):
    x0, y0 = _grid_origin
    x = x0 + c * (TILE_SIZE + PADDING)
    y = y0 + r * (TILE_SIZE + PADDING)

    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    if tile["matched"]:
        color = TILE_MATCHED
    elif tile["revealed"]:
        color = TILE_FACE_UP
    else:
        color = TILE_FACE_DOWN

    pygame.draw.rect(_screen, color, rect, border_radius=8)

    if tile["revealed"] or tile["matched"]:
        value_text = str(tile["value"])
        surf = _font.render(value_text, True, TEXT_DARK)
        text_rect = surf.get_rect(center=rect.center)
        _screen.blit(surf, text_rect)


def get_tile_at_pos(pos):
    x, y = pos
    x0, y0 = _grid_origin

    if y < y0:
        return None

    rel_x = x - x0
    rel_y = y - y0

    if rel_x < 0 or rel_y < 0:
        return None

    col = rel_x // (TILE_SIZE + PADDING)
    row = rel_y // (TILE_SIZE + PADDING)

    if row < 0 or row >= _rows or col < 0 or col >= _cols:
        return None

    if (rel_x % (TILE_SIZE + PADDING)) > TILE_SIZE:
        return None
    if (rel_y % (TILE_SIZE + PADDING)) > TILE_SIZE:
        return None

    return int(row), int(col)


def get_click_tile_from_event(event):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        return get_tile_at_pos(event.pos)
    return None


def quit_ui():
    pygame.quit()
