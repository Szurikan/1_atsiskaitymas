import pickle
from config import MOVIE_LIST_PATH


def load_movie_list():
    try:
        with open(MOVIE_LIST_PATH, "rb") as file:
            movie_list = pickle.load(file)
    except FileNotFoundError:
        movie_list = {}
    return movie_list


def save_movie_list(movie_list):
    with open(MOVIE_LIST_PATH, "wb") as file:
        pickle.dump(movie_list, file)