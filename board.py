import random

def create_board(rows, cols, symbols):

    pairs = (rows * cols) // 2

    tiles = symbols[:pairs] * 2

    random.shuffle(tiles)

    board = []
    index = 0

    for r in range(rows):
        row = []
        for c in range(cols):
            row.append({
                "value": tiles[index],
                "revealed": False,
                "matched": False
            })
            index += 1
        board.append(row)

    return board

def reveal_tile(board, r, c):
    board[r][c]["revealed"] = True
    return board[r][c]["value"]

def hide_tile(board, r, c):
    board[r][c]["revealed"] = False

def match_tiles(board, pos1, pos2):
    r1, c1 = pos1
    r2, c2 = pos2
    board[r1][c1]["matched"] = True
    board[r2][c2]["matched"] = True

def get_value(board, r, c):
    return board[r][c]["value"]

def is_revealed(board, r, c):
    return board[r][c]["revealed"]

def is_matched(board, r, c):
    return board[r][c]["matched"]

def reset_board(board):
    for row in board:
        for tile in row:
            if not tile["matched"]:
                tile["revealed"] = False
