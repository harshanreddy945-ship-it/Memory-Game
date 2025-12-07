import board

def init_game_state(game_board):
    rows = len(game_board)
    cols = len(game_board[0]) if rows > 0 else 0
    total_pairs = (rows * cols) // 2

    state = {
        "first_selected": None,      
        "second_selected": None,     
        "moves_count": 0,            
        "pairs_found": 0,            
        "total_pairs": total_pairs,  
        "status": "waiting_first",   
        "last_result": None          
    }
    return state


def can_flip_tile(game_board, state, r, c):
    
    rows = len(game_board)
    cols = len(game_board[0]) if rows > 0 else 0

    if r < 0 or r >= rows or c < 0 or c >= cols:
        return False

    if state["status"] in ("checking", "mismatch_pending", "game_over"):
        return False

    if board.is_revealed(game_board, r, c):
        return False

    if board.is_matched(game_board, r, c):
        return False

    return True


def flip_tile(game_board, state, r, c):
    if not can_flip_tile(game_board, state, r, c):
        return "ignore"
    board.reveal_tile(game_board, r, c)
    pos = (r, c)
    if state["first_selected"] is None:
        
        state["first_selected"] = pos
        state["status"] = "waiting_second"
        state["last_result"] = None
        return "first_flip"

    elif state["second_selected"] is None:
        state["second_selected"] = pos
        state["status"] = "checking"
        return "second_flip"

    else:
        return "ignore"


def check_match(game_board, state):
    pos1 = state["first_selected"]
    pos2 = state["second_selected"]

    if pos1 is None or pos2 is None:
        return "no_pair"

    r1, c1 = pos1
    r2, c2 = pos2

    v1 = board.get_value(game_board, r1, c1)
    v2 = board.get_value(game_board, r2, c2)

    state["moves_count"] += 1

    if v1 == v2:
        board.match_tiles(game_board, pos1, pos2)
        state["pairs_found"] += 1
        state["first_selected"] = None
        state["second_selected"] = None
        state["last_result"] = "match"

        if state["pairs_found"] == state["total_pairs"]:
            state["status"] = "game_over"
        else:
            state["status"] = "waiting_first"

        return "match"

    else:
        state["last_result"] = "mismatch"
        state["status"] = "mismatch_pending"
        return "mismatch"


def finalize_mismatch(game_board, state):
    if state["status"] != "mismatch_pending":
        return

    pos1 = state["first_selected"]
    pos2 = state["second_selected"]

    if pos1 is not None:
        r1, c1 = pos1
        board.hide_tile(game_board, r1, c1)

    if pos2 is not None:
        r2, c2 = pos2
        board.hide_tile(game_board, r2, c2)

    state["first_selected"] = None
    state["second_selected"] = None

    state["status"] = "waiting_first"


def is_game_over(state):
    return state["status"] == "game_over"


def get_stats(state):
    return {
        "moves_count": state["moves_count"],
        "pairs_found": state["pairs_found"],
        "total_pairs": state["total_pairs"],
        "status": state["status"],
        "last_result": state["last_result"],
    }
