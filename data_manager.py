import json
import os

HIGHSCORE_FILE = "highscores.json"


def load_highscores():

    if not os.path.exists(HIGHSCORE_FILE):

        return {
            "easy": None,
            "medium": None,
            "hard": None
        }

    try:
        with open(HIGHSCORE_FILE, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):

        return {
            "easy": None,
            "medium": None,
            "hard": None
        }


    for level in ("easy", "medium", "hard"):
        if level not in data:
            data[level] = None

    return data


def save_highscores(highscores):

    try:
        with open(HIGHSCORE_FILE, "w") as f:
            json.dump(highscores, f, indent=4)
    except OSError:
        pass


def get_best_time(highscores, difficulty):
    return highscores.get(difficulty, None)


def update_highscore(highscores, difficulty, new_time):
    if difficulty not in highscores:
        return False

    current_best = highscores[difficulty]
    
    if current_best is None or new_time < current_best:
        highscores[difficulty] = new_time
        return True

    return False
