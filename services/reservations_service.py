from models.film import Movie
from models.festival import Festival
from models.reservations import Reservation
from services.film_service import show_movies
from services.data_handler import save_movie_list
import datetime
from colorama import Fore, Back, Style

def add_session_time(festival):
    show_movies(festival)
    movie_session = input("\nĮveskite kuriam filmui norite pridėti seanso laiką: ").strip()
    found_movie = festival.movie_dict.get(movie_session)

    if not found_movie:
        print(Fore.RED + "Tokio filmo nėra." + Style.RESET_ALL)
        return
    if found_movie.session_time:
        print(Fore.RED + f"Šis filmas jau turi seanso laiką: {found_movie.session_time.strftime('%Y-%m-%d %H:%M')}" + Style.RESET_ALL)
        return

    while True:
        session_time_str = input("Įveskite seanso laiką (YYYY-MM-DD HH:MM): ").strip()
        try:
            session_time = datetime.datetime.strptime(session_time_str, "%Y-%m-%d %H:%M")
            if session_time < datetime.datetime.now():
                print(Fore.RED + "Įvestas laikas jau praėjo. Bandykite kitą laiką." + Style.RESET_ALL)
                continue

            if any(time.session_time == session_time for time in festival.movie_dict.values()):
                print(Fore.RED + "Šis seanso laikas užimtas. Bandykite kitą laiką." + Style.RESET_ALL)
                continue

        except ValueError:
            print(Fore.RED + "Netinkamas laiko formatas. Naudokite YYYY-MM-DD HH:MM." + Style.RESET_ALL)
            continue

        try:
            ticket_price = float(input("Įvestkite bilieto kaina Eurais: "))
            if ticket_price < 0:
                print(Fore.RED + "Kaina negali būti mažesnė už 0." + Style.RESET_ALL)

            found_movie.session_time = session_time
            found_movie.ticket_price = ticket_price
            save_movie_list(festival.movie_dict)
            print(f"Pridėtas seanso laikas: {session_time.strftime('%Y-%m-%d %H:%M')}. Bilieto kaina: {ticket_price} EUR.")
            break
        
        except ValueError:
            print(Fore.RED + "Netinkamas formatas." + Style.RESET_ALL)

def show_sessions(festival, username):
    sessions_found = False
    for i, movie in enumerate(festival.movie_dict.values(), start=1):
        if movie.session_time:
            print(f"{i}. {movie.name} - {movie.session_time.strftime('%Y-%m-%d %H:%M')} - Liko bilietų: {movie.tickets} - Bilieto kaina {movie.ticket_price} EUR")
            sessions_found = True
    if not sessions_found:
        print(Fore.RED + "Seansų nėra." + Style.RESET_ALL)
        return

    book_or_not = input("\nJeigu norite rezervuoti bilietą, įveskite filmo pavadinimą. Jei ne, spauskite Enter: ").strip()
    if book_or_not:
        book_ticket(book_or_not, username, festival)

def book_ticket(movie_name, username, festival):
    movie = festival.movie_dict.get(movie_name)
    if not movie:
        print(Fore.RED + "Tokio filmo nerasta." + Style.RESET_ALL)
        return
    if not movie.session_time:
        print(Fore.RED + "Šiam filmui seansas dar nenustatytas." + Style.RESET_ALL)
        return
    
    
    while True:
        try:
            ticket_count = int(input(f"Vieno bilieto kaina - {movie.ticket_price} EUR. Įveskite norimą bilietų kiekį (arba 0, jei norite išeiti): "))
            if ticket_count == 0:
                print(Fore.RED + "Bilietų rezervacija atšaukta." + Style.RESET_ALL)
                return
            if ticket_count < 0:
                print(Fore.RED + "Bilietų kiekis turi būti teigiamas skaičius." + Style.RESET_ALL)
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
                print(Fore.RED + f"Nepakanka bilietų. Liko tik {movie.tickets} bilietai." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Įvedėte bilietų kiekį neteisingu formatu. Bandykite dar kartą." + Style.RESET_ALL)

def show_reservations(festival):
    reservation_count = 0

    if not festival.movie_dict:
        print(Fore.RED + "Nėra filmų." + Style.RESET_ALL)
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