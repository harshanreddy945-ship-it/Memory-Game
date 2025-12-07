import time
import pygame

import board
import logic
import data_manager
import ui

DIFFICULTY_SETTINGS = {
    "easy":   (4, 4),
    "medium": (4, 6),
    "hard":   (6, 6),
}

SYMBOLS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")

def choose_difficulty():
    while True:
        print("Choose difficulty: easy / medium / hard")
        diff = input("Enter difficulty: ").strip().lower()
        if diff in DIFFICULTY_SETTINGS:
            return diff
        print("Invalid difficulty, try again.\n")


def start_new_game(difficulty):

    rows, cols = DIFFICULTY_SETTINGS[difficulty]
    game_board = board.create_board(rows, cols, SYMBOLS)
    state = logic.init_game_state(game_board)

    start_time = None
    mismatch_timer = None  
    score_saved = False    

    ui.init_ui(rows, cols, window_title="Memory Match - " + difficulty.title())
    return game_board, state, start_time, mismatch_timer, score_saved

def main():
    highscores = data_manager.load_highscores()
    difficulty = choose_difficulty()
    game_board, state, start_time, mismatch_timer, score_saved = start_new_game(
        difficulty
    )

    clock = pygame.time.Clock()
    running = True

    while running:
        if start_time is None:
            elapsed = 0.0
        else:
            elapsed = time.time() - start_time

        stats = logic.get_stats(state)
        best_time = data_manager.get_best_time(highscores, difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                game_board, state, start_time, mismatch_timer, score_saved = start_new_game(
                    difficulty
                )
            else:
                if mismatch_timer is None:
                    tile = ui.get_click_tile_from_event(event)
                    if tile is not None and not logic.is_game_over(state):
                        r, c = tile

                        if start_time is None:
                            start_time = time.time()
                            elapsed = 0.0

                        result = logic.flip_tile(game_board, state, r, c)

                        if result == "second_flip":
                            match_result = logic.check_match(game_board, state)
                            if match_result == "mismatch":
                                mismatch_timer = time.time()

        if mismatch_timer is not None:
            if time.time() - mismatch_timer >= 0.8:
                logic.finalize_mismatch(game_board, state)
                mismatch_timer = None

        if logic.is_game_over(state) and not score_saved:
            if start_time is not None:
                final_time = time.time() - start_time
            else:
                final_time = 0.0

            improved = data_manager.update_highscore(
                highscores, difficulty, final_time
            )
            data_manager.save_highscores(highscores)

            if improved:
                print(f"New high score for {difficulty}! Time: {final_time:.2f} s")
            else:
                print(
                    f"Finished {difficulty} in {final_time:.2f} s, "
                    "but did not beat the best time."
                )

            score_saved = True

        ui.draw_ui(game_board, stats, elapsed, difficulty, best_time)

        clock.tick(60)

    ui.quit_ui()

if __name__ == "__main__":
    main()
