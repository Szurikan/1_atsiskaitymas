import datetime
from models.film import Movie
from services.data_handler import save_movie_list
from models.reservations import Reservation

class Festival:
    def __init__(self):
        self.movie_dict = {}


    # def add_session_time(self):
    #     self.show_movies()
    #     movie_session = input("\nĮveskite kuriam filmui norite pridėti seanso laiką: ").strip()
    #     found_movie = self.movie_dict.get(movie_session)

    #     if not found_movie:
    #         print("Tokio filmo nėra.")
    #         return
    #     if found_movie.session_time:
    #         print(f"Šis filmas jau turi seanso laiką: {found_movie.session_time.strftime('%Y-%m-%d %H:%M')}")
    #         return

    #     while True:
    #         session_time_str = input("Įveskite seanso laiką (YYYY-MM-DD HH:MM): ").strip()
    #         try:
    #             session_time = datetime.datetime.strptime(session_time_str, "%Y-%m-%d %H:%M")
    #             if session_time < datetime.datetime.now():
    #                 print("Įvestas laikas jau praėjo. Bandykite kitą laiką.")
    #                 continue

    #             if any(time.session_time == session_time for time in self.movie_dict.values()):
    #                 print("Šis seanso laikas užimtas. Bandykite kitą laiką.")
    #                 continue

    #         except ValueError:
    #             print("Netinkamas laiko formatas. Naudokite YYYY-MM-DD HH:MM.")

    #         try:
    #             ticket_price = float(input("Įvestkite bilieto kaina Eurais: "))
    #             if ticket_price < 0:
    #                 print("Kaina negali būti mažesnė už 0.")

    #             found_movie.session_time = session_time
    #             found_movie.ticket_price = ticket_price
    #             save_movie_list(self.movie_dict)
    #             print(f"Pridėtas seanso laikas: {session_time.strftime('%Y-%m-%d %H:%M')}. Bilieto kaina: {ticket_price} EUR.")
    #             break
            
    #         except ValueError:
    #             print("Netinkamas formatas.")

    # def show_sessions(self, username):
    #     sessions_found = False
    #     for i, movie in enumerate(self.movie_dict.values(), start=1):
    #         if movie.session_time:
    #             print(f"{i}. {movie.name} - {movie.session_time.strftime('%Y-%m-%d %H:%M')} - Liko bilietų: {movie.tickets} - Bilieto kaina {movie.ticket_price} EUR")
    #             sessions_found = True
    #     if not sessions_found:
    #         print("Seansų nėra.")
    #         return

    #     book_or_not = input("\nJeigu norite rezervuoti bilietą, įveskite filmo pavadinimą. Jei ne, spauskite Enter: ").strip()
    #     if book_or_not:
    #         self.book_ticket(book_or_not, username)

    # def book_ticket(self, movie_name, username):
    #     movie = self.movie_dict.get(movie_name)
    #     if not movie:
    #         print("Tokio filmo nerasta.")
    #         return
    #     if not movie.session_time:
    #         print("Šiam filmui seansas dar nenustatytas.")
    #         return
        
        
    #     while True:
    #         try:
    #             ticket_count = int(input(f"Vieno bilieto kaina - {movie.ticket_price} EUR. Įveskite norimą bilietų kiekį (arba 0, jei norite išeiti): "))
    #             if ticket_count == 0:
    #                 print("Bilietų rezervacija atšaukta.")
    #                 return
    #             if ticket_count < 0:
    #                 print("Bilietų kiekis turi būti teigiamas skaičius.")
    #                 continue
    #             total_price = ticket_count * movie.ticket_price

    #             reservation = Reservation(username, movie_name, ticket_count, total_price)

    #             if movie.tickets >= reservation.ticket_count:
    #                 movie.tickets -= reservation.ticket_count
    #                 movie.reservations.append(reservation)
    #                 save_movie_list(self.movie_dict)
    #                 print(f"Jūs rezervavote {ticket_count} bilietų. Atsiėmimo metu turėsite sumoketi {total_price} EUR.")
    #                 break
    #             else:
    #                 print(f"Nepakanka bilietų. Liko tik {movie.tickets} bilietai.")
    #         except ValueError:
    #             print("Įvedėte bilietų kiekį neteisingu formatu. Bandykite dar kartą.")


    # def get_movie_reservation_count(self, movie):
    #     reservations = 0
    #     for reservation in movie.reservations:
    #         reservations += reservation.ticket_count
    #     return reservations

    # def show_most_popular_movies(self):
    #     if not self.movie_dict:
    #         print("Filmų nėra.")
    #         return
        
    #     movie_ranking = sorted(self.movie_dict.values(), key=self.get_movie_reservation_count, reverse=True)

    #     print("Populiariausi filmai:")
    #     for i, movie in enumerate(movie_ranking, start=1):
    #         print(f"{i}. {movie.name} - {self.get_movie_reservation_count(movie)} rezervacijų.")

    # def show_reservations(self):
    #     if not self.movie_dict:
    #         print("Nėra filmų.")
    #         return

    #     for movie in self.movie_dict.values():
    #         if movie.reservations:
    #             for i, reservation in enumerate(movie.reservations, start=1):
    #                 print(f"{i}. {reservation}")

    # def show_income(self):
    #     income_amount = 0
    #     for movie in self.movie_dict.values():
    #         for reservation in movie.reservations:
    #             income_amount += reservation.total_price
    #     print(f"Jūsų uždirbtos pajamos: {income_amount} EUR")
