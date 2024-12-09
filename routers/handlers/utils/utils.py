import json
import os

from src.core import BASE_DIR

file = os.path.join(BASE_DIR, "questions_to_states.txt")


def get_questions_to_states():
    data = load_data(file)
    return data


def load_data(file_):
    with open(file_, "r", encoding="utf-8") as doc:
        data = json.load(doc)
        return data
