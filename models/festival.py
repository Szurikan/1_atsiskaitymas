import datetime
from models.film import Movie
from services.data_handler import save_movie_list
from models.reservations import Reservation

class Festival:
    def __init__(self):
        self.movie_dict = {}

    def add_movie(self):

        while True:
            name = input("Įrašykite filmo pavadinimą: ").strip()
            if not name:
                print("Filmo pavadinimas negali būti tuščias. Bandykite dar kartą")
                continue
            if name in self.movie_dict:
                print("Filmas tokiu pavadinimu jau egzistuoja.")
                continue
            break
    
        while True:   
            try:
                duration = int(input("Įrašykite filmo trukmę (minutėmis): "))
                if duration <= 0:
                    print("Įrašykite teisingą filmo trukmę")
                    continue
                break
            except ValueError:
                print("Įvedėtė neteisingą formatą. Veskite dar kartą")
                continue

        genre = input("Įrašykite filmo žanrą: ").strip()
        
        while True:
            director = input("Įrašykite filmo režisierių: ").strip()
            if not director:
                print("Privalote įvestį filmo režisierių")
                continue
            break

        while True:
            try:
                year = int(input("Įrašykite filmo sukūrimo metus: "))
                if year < 1900 or year > 2025:
                    print("Neteisingi metai. Veskite dar kartą")
                    continue
                break
            except ValueError:
                print("Įvedėtė neteisingą formatą. Veskite dar kartą")
                continue

        age_rating = input("Įrašykite filmo amžiaus reitingą (jeigu yra): ").strip()

        new_movie = Movie(name, duration, genre, director, year, age_rating)
        self.movie_dict[name] = new_movie
        save_movie_list(self.movie_dict)
        print("Filmas pridėtas sėkmingai.")


    def show_movies(self):
        if not self.movie_dict:
            print("Filmų sąrašas tuščias.")
        else:
            print("\nFilmų sąrašas:")
            for i, movie in enumerate(self.movie_dict.values(), start=1):
                print(f"{i}. {movie.__repr__()}")

    def show_movies_extended(self):
        if not self.movie_dict:
            print("Filmų sąrašas tuščias.")
        else:
            print("\nDetali filmų peržiūra:")
            for i, movie in enumerate(self.movie_dict.values(), start=1):
                print(f"{i}. {movie}")

    def delete_movie(self):
        if not self.movie_dict:
            print("Nėra filmų, kuriuos būtų galima pašalinti.")
            return

        self.show_movies()
        movie_to_delete = input("Įveskite filmo pavadinimą, kurį norėtumėte pašalinti: ").strip()
        if self.movie_dict.pop(movie_to_delete, None):
            save_movie_list(self.movie_dict)
            print(f"Filmas '{movie_to_delete}' pašalintas.")
        else:
            print("Filmas neegzistuoja.")

    def update_movie(self):
        if not self.movie_dict:
            print("Nėra filmų, kuriuos būtų galima redaguoti.")
            return

        self.show_movies()
        movie_to_change = input("Įveskite filmo pavadinimą, kurį norite redaguoti: ").strip()
        movie = self.movie_dict.get(movie_to_change)

        if not movie:
            print("Toks filmas nerastas!")
            return

        print("\nRedaguojate:")
        print(movie)
        print("1. Pakeisti pavadinimą\n2. Pakeisti trukmę\n3. Pakeisti žanrą\n"
              "4. Pakeisti režisierių\n5. Pakeisti metus\n6. Pakeisti amžiaus reitingą")

        choice = input("Įveskite pasirinkimą: ").strip()

        if choice == "1":
            while True:
                new_name = input("Įveskite naują pavadinimą: ").strip()
                if not new_name:
                    print("Pavadinimas negali būtu tuščias.")
                    continue
                if new_name in self.movie_dict:
                    print("Pavadinimas jau egzistuoja")
                    continue
                if new_name == movie_to_change:
                    print("Pavadinimas negali būti toks pats kaip ir senasis.")
                    continue
                self.movie_dict[new_name] = self.movie_dict.pop(movie_to_change)
                self.movie_dict[new_name].name = new_name
                break

        elif choice == "2":
            while True:
                try:
                    new_duration = int(input("Įveskite naują trukmę (minutėmis): "))
                    if new_duration < 1:
                        print("Mažiausia filmo trukmė yra 1 minutė")
                        continue
                    else:
                        new_duration = movie.duration
                        break
                except ValueError:
                    print("Neteisingas skaičių formatas.")
                    continue

        elif choice == "3":
            movie.genre = input("Įveskite naują žanrą: ").strip()

        elif choice == "4":
            while True:
                new_director = input("Įveskite naują režisierių: ").strip()
                if new_director:
                    movie.director = new_director
                    break
                elif new_director == movie.director:
                    print("Režisierius jau turi tokį vardą.")
                    break
                else:
                    print("Privalote įvesti režisierių")
                    continue


        elif choice == "5":
            while True:
                try:
                    new_year = int(input("Įveskite naujus metus: "))
                    if new_year < 1900 or new_year > 2025:
                        print("Ivesti neteisingi metai.")
                        continue
                    else:
                        new_year = movie.year
                        break
                except ValueError:
                    print("Neteisingas skaičių formatas.")
                    continue
        
        elif choice == "6":
            movie.age_rating = input("Įveskite naują amžiaus reitingą: ").strip()
        else:
            print("Neteisingas pasirinkimas.")
            return

        save_movie_list(self.movie_dict)
        print(f"Filmas '{movie.name}' paredaguotas sėkmingai.")

    def search_movie(self):
        if not self.movie_dict:
            print("Filmų sąrašas tuščias.")
            return

        print("\nPaieška pagal:\n1. Pavadinimą\n2. Režisierių")
        choice = input("Įveskite pasirinkimą: ").strip()

        if choice == "1":
            movie_name_part = input("Įveskite filmo pavadinimą: ").strip().lower()
            found_movies = [movie for movie in self.movie_dict.values() if movie_name_part in movie.name.lower()]
            if found_movies:
                print("Rasti filmai:")
                for movie in found_movies:
                    print(movie)
            else:
                print("Filmai nerasti.")

        elif choice == "2":
            director_name = input("Įveskite režisieriaus vardą: ").strip().lower()
            director_movies = [movie for movie in self.movie_dict.values() if movie.director.lower() == director_name]
            if director_movies:
                print("Rasti filmai:")
                for movie in director_movies:
                    print(movie)
            else:
                print("Toks režisierius festivalyje nedalyvauja.")
        else:
            print("Neteisingas pasirinkimas.")

    def add_session_time(self):
        self.show_movies()
        movie_session = input("\nĮveskite kuriam filmui norite pridėti seanso laiką: ").strip()
        found_movie = self.movie_dict.get(movie_session)

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

                if any(time.session_time == session_time for time in self.movie_dict.values()):
                    print("Šis seanso laikas užimtas. Bandykite kitą laiką.")
                    continue

                found_movie.session_time = session_time
                save_movie_list(self.movie_dict)
                print(f"Pridėtas seanso laikas: {session_time.strftime('%Y-%m-%d %H:%M')}")
                break

            except ValueError:
                print("Netinkamas laiko formatas. Naudokite YYYY-MM-DD HH:MM.")

    def show_sessions(self, username):
        sessions_found = False
        for i, movie in enumerate(self.movie_dict.values(), start=1):
            if movie.session_time:
                print(f"{i}. {movie.name} - {movie.session_time.strftime('%Y-%m-%d %H:%M')} | Liko bilietų: {movie.tickets}")
                sessions_found = True
        if not sessions_found:
            print("Nėra numatytų seansų.")
            return

        book_or_not = input("\nJeigu norite rezervuoti bilietą, įveskite filmo pavadinimą. Jei ne, spauskite Enter: ").strip()
        if book_or_not:
            self.book_ticket(book_or_not, username)

    def book_ticket(self, movie_name, username):
        movie = self.movie_dict.get(movie_name)
        if not movie:
            print("Tokio filmo nerasta.")
            return
        if not movie.session_time:
            print("Šiam filmui seansas dar nenustatytas.")
            return
        
        
        while True:
            try:
                ticket_count = int(input("Įveskite norimą bilietų kiekį (arba 0, jei norite išeiti): "))
                if ticket_count == 0:
                    print("Bilietų rezervacija atšaukta.")
                    return
                if ticket_count < 0:
                    print("Bilietų kiekis turi būti teigiamas skaičius.")
                    continue

                reservation = Reservation(username, movie_name, ticket_count)

                if movie.add_reservation(reservation):
                    save_movie_list(self.movie_dict)
                    print(f"Jūs rezervavote {ticket_count} bilietų")
                    break
                else:
                    print(f"Nepakanka bilietų. Liko tik {movie.tickets} bilietai.")
            except ValueError:
                print("Įvedėte bilietų kiekį neteisingu formatu. Bandykite dar kartą.")


    def rank_movie(self):
        self.show_movies()
        to_rank = input("Įrašykite filmo pavadinimą, kuriam norite suteikti reitingą: ").strip()
        movie = self.movie_dict.get(to_rank)

        if not movie:
            print("Filmas nerastas.")
            return

        while True:
            try:
                user_ranking = int(input("Įrašykite reitingą (1–10): "))
                if 1 <= user_ranking <= 10:
                    movie.ranking_points += user_ranking
                    movie.user_ranking_count += 1
                    movie.ranking = movie.ranking_points / movie.user_ranking_count
                    save_movie_list(self.movie_dict)
                    print("Ačiū, Jūsų reitingas išsaugotas.")
                    break
                else:
                    print("Reitingas turi būti tarp 1 ir 10.")
            except ValueError:
                print("Neteisingas reitingo formatas.")


    def get_movie_reservation_count(self, movie):
        return movie.reservation_count()

    def show_most_popular_movies(self):
        if not self.movie_dict:
            print("Filmų nėra.")
            return
        
        movie_ranking = sorted(self.movie_dict.values(), key=self.get_movie_reservation_count, reverse=True)

        print("Populiariausi filmai:")
        for i, movie in enumerate(movie_ranking, start=1):
            print(f"{i}. {movie.name} - {movie.reservation_count()} rezervacijų.")

