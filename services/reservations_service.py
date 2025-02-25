from models.film import Movie
from models.festival import Festival
from models.reservations import Reservation
from services.film_service import show_movies
from services.data_handler import save_movie_list
import datetime

def add_session_time(festival):
    show_movies(festival)
    movie_session = input("\nĮveskite kuriam filmui norite pridėti seanso laiką: ").strip()
    found_movie = festival.movie_dict.get(movie_session)

    if not found_movie:
        print("Tokio filmo nėra.")
        return
    if found_movie.session_time:
        print(f"Šis filmas jau turi seanso laiką: {found_movie.session_time.strftime('%Y-%m-%d %H:%M')}")
        return

    while True:
        session_time_str = input("Įveskite seanso laiką (YYYY-MM-DD HH:MM): ").strip()
        try:
            session_time = datetime.datetime.strptime(session_time_str, "%Y-%m-%d %H:%M")
            if session_time < datetime.datetime.now():
                print("Įvestas laikas jau praėjo. Bandykite kitą laiką.")
                continue

            if any(time.session_time == session_time for time in festival.movie_dict.values()):
                print("Šis seanso laikas užimtas. Bandykite kitą laiką.")
                continue

        except ValueError:
            print("Netinkamas laiko formatas. Naudokite YYYY-MM-DD HH:MM.")
            continue

        try:
            ticket_price = float(input("Įvestkite bilieto kaina Eurais: "))
            if ticket_price < 0:
                print("Kaina negali būti mažesnė už 0.")

            found_movie.session_time = session_time
            found_movie.ticket_price = ticket_price
            save_movie_list(festival.movie_dict)
            print(f"Pridėtas seanso laikas: {session_time.strftime('%Y-%m-%d %H:%M')}. Bilieto kaina: {ticket_price} EUR.")
            break
        
        except ValueError:
            print("Netinkamas formatas.")

def show_sessions(festival, username):
    sessions_found = False
    for i, movie in enumerate(festival.movie_dict.values(), start=1):
        if movie.session_time:
            print(f"{i}. {movie.name} - {movie.session_time.strftime('%Y-%m-%d %H:%M')} - Liko bilietų: {movie.tickets} - Bilieto kaina {movie.ticket_price} EUR")
            sessions_found = True
    if not sessions_found:
        print("Seansų nėra.")
        return

    book_or_not = input("\nJeigu norite rezervuoti bilietą, įveskite filmo pavadinimą. Jei ne, spauskite Enter: ").strip()
    if book_or_not:
        book_ticket(book_or_not, username, festival)

def book_ticket(movie_name, username, festival):
    movie = festival.movie_dict.get(movie_name)
    if not movie:
        print("Tokio filmo nerasta.")
        return
    if not movie.session_time:
        print("Šiam filmui seansas dar nenustatytas.")
        return
    
    
    while True:
        try:
            ticket_count = int(input(f"Vieno bilieto kaina - {movie.ticket_price} EUR. Įveskite norimą bilietų kiekį (arba 0, jei norite išeiti): "))
            if ticket_count == 0:
                print("Bilietų rezervacija atšaukta.")
                return
            if ticket_count < 0:
                print("Bilietų kiekis turi būti teigiamas skaičius.")
                continue
            total_price = ticket_count * movie.ticket_price

            reservation = Reservation(username, movie_name, ticket_count, total_price)

            if movie.tickets >= reservation.ticket_count:
                movie.tickets -= reservation.ticket_count
                movie.reservations.append(reservation)
                save_movie_list(festival.movie_dict)
                print(f"Jūs rezervavote {ticket_count} bilietų. Atsiėmimo metu turėsite sumoketi {total_price} EUR.")
                break
            else:
                print(f"Nepakanka bilietų. Liko tik {movie.tickets} bilietai.")
        except ValueError:
            print("Įvedėte bilietų kiekį neteisingu formatu. Bandykite dar kartą.")

def show_reservations(festival):
    reservation_count = 0

    if not festival.movie_dict:
        print("Nėra filmų.")
        return

    for movie in festival.movie_dict.values():
        if movie.reservations:
            for reservation in movie.reservations:
                reservation_count += 1
                print(f"{reservation_count}. {reservation}")

        # if movie.reservations:
        #     for i, reservation in enumerate(movie.reservations, start={i + 1}):
        #         print(f"{i}. {reservation}")

def show_income(festival):
    income_amount = 0
    for movie in festival.movie_dict.values():
        for reservation in movie.reservations:
            income_amount += reservation.total_price
    print(f"Jūsų uždirbtos pajamos: {income_amount} EUR")