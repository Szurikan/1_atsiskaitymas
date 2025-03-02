# import pickle
import sqlite3
import datetime
from config import MOVIE_LIST_PATH
from models.film import Movie
from models.reservations import Reservation

def create_movie_table():
    conn = sqlite3.connect(MOVIE_LIST_PATH)
    with conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS festivalis (
                name TEXT PRIMARY KEY,
                duration INTEGER,
                genre TEXT,
                director TEXT,
                year INTEGER,
                age_rating TEXT DEFAULT '',
                session_time TEXT,
                tickets INTEGER DEFAULT 10,
                ranking_points INTEGER DEFAULT 0,
                user_ranking_count INTEGER DEFAULT 0,
                ranking REAL DEFAULT 0,
                ticket_price REAL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS reservations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                user TEXT,
                seats INTEGER,
                FOREIGN KEY (movie_name) REFERENCES festivalis(name) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ranking_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                user TEXT,
                FOREIGN KEY (movie_name) REFERENCES festivalis(name) ON DELETE CASCADE
            )
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS ranking_comment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                movie_name TEXT,
                comment TEXT,
                FOREIGN KEY (movie_name) REFERENCES festivalis(name) ON DELETE CASCADE
            )
        """)
    print("Lentelės sukurtos arba jau egzistuoja.")


# def load_movie_list():
#     try:
#         with open(MOVIE_LIST_PATH, "rb") as file:
#             movie_list = pickle.load(file)
#     except FileNotFoundError:
#         movie_list = {}
#     return movie_list


# def save_movie_list(movie_list):
#     with open(MOVIE_LIST_PATH, "wb") as file:
#         pickle.dump(movie_list, file)

def load_movie_list():
    movie_list = {}

    try:
        conn = sqlite3.connect(MOVIE_LIST_PATH)
        with conn:
            cur = conn.cursor()
            cur.execute("""
        SELECT name, duration, genre, director, year, age_rating, session_time, tickets, 
        ranking_points, user_ranking_count, ranking, ticket_price FROM festivalis
                        """)
            print("Operacija sekminga")
            movies = cur.fetchall()

            for movie in movies:
                name, duration, genre, director, year, age_rating, session_time, tickets, ranking_points, user_ranking_count, ranking, ticket_price = movie

                session_time = datetime.datetime.strptime(session_time, "%Y-%m-%d %H:%M") if session_time else None

                movie = Movie(name, duration, genre, director, year, age_rating, session_time, tickets, ranking_points, user_ranking_count, ranking, ticket_price)
                movie_list[name] = movie

                cur.execute("""
                    SELECT user, seats FROM reservations WHERE movie_name = ?
                """, (name,))
                reservations = cur.fetchall()

                movie.reservations = [
                    Reservation(user, name, seats, seats * (ticket_price if ticket_price else 0)) 
                    for user, seats in reservations
                ]

                cur.execute("""
                        SELECT user FROM ranking_users WHERE movie_name = ?
                    """, (name,))
                rankings = cur.fetchall()
                movie.ranking_users = [user[0] for user in rankings]

                cur.execute("""
                        SELECT comment FROM ranking_comment WHERE movie_name = ?
                    """, (name,))
                rankings = cur.fetchall()
                movie.ranking_comment = [comment[0] for comment in rankings]


    
    except sqlite3.Error:
        print("Klaida jungiantis prie duomenu bazes")

    return movie_list


def save_movie_list(movie_list):
    conn = sqlite3.connect(MOVIE_LIST_PATH)
    with conn:
        cur = conn.cursor()

        for movie in movie_list.values():

            session_time_str = movie.session_time.strftime("%Y-%m-%d %H:%M") if movie.session_time else None
            # Įterpiamas arba atnaujinamas filmo įrašas
            cur.execute("""
                INSERT OR REPLACE INTO festivalis(name, duration, genre, 
                    director, year, age_rating, session_time, tickets, ranking_points, 
                    user_ranking_count, ranking, ticket_price) 
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (movie.name, movie.duration, movie.genre, 
                  movie.director, movie.year, movie.age_rating, session_time_str, 
                  movie.tickets, movie.ranking_points, movie.user_ranking_count, 
                  movie.ranking, movie.ticket_price))

            # Ištrinti senas rezervacijas, reitingus ir komentarus (kad nebūtų dubliuojami)
            cur.execute("DELETE FROM reservations WHERE movie_name = ?", (movie.name,))
            cur.execute("DELETE FROM ranking_users WHERE movie_name = ?", (movie.name,))
            cur.execute("DELETE FROM ranking_comment WHERE movie_name = ?", (movie.name,))

            # Įrašyti naujas rezervacijas
            for reservation in movie.reservations:
                cur.execute("""
                    INSERT INTO reservations(movie_name, user, seats) 
                    VALUES(?, ?, ?)
                """, (reservation.movie_name, reservation.username, reservation.ticket_count))

            # Įrašyti naujus vartotojų reitingų vartotojus (be reitingų)
            for user in movie.ranking_users:
                cur.execute("""
                    INSERT INTO ranking_users(movie_name, user) 
                    VALUES(?, ?)
                """, (movie.name, user))

            # Įrašyti naujus komentarus
            for comment in movie.ranking_comment:
                cur.execute("""
                    INSERT INTO ranking_comment(movie_name, comment) 
                    VALUES(?, ?)
                """, (movie.name, comment))

    print("Duomenys išsaugoti sėkmingai.")


