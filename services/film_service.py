from models.film import Movie
from models.festival import Festival
from models.reservations import Reservation
from services.data_handler import save_movie_list
from colorama import Fore, Back, Style

def add_movie(festival):

    while True:
        name = input("Įrašykite filmo pavadinimą: ").strip()
        if not name:
            print(Fore.RED + "Filmo pavadinimas negali būti tuščias. Bandykite dar kartą" + Style.RESET_ALL)
            continue
        if name in festival.movie_dict:
            print(Fore.RED + "Filmas tokiu pavadinimu jau egzistuoja." + Style.RESET_ALL)
            continue
        break

    while True:   
        try:
            duration = int(input("Įrašykite filmo trukmę (minutėmis): "))
            if duration <= 0:
                print(Fore.RED + "Įrašykite teisingą filmo trukmę" + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + "Įvedėtė neteisingą formatą. Veskite dar kartą" + Style.RESET_ALL)
            continue

    genre = input("Įrašykite filmo žanrą: ").strip()
    
    while True:
        director = input("Įrašykite filmo režisierių: ").strip()
        if not director:
            print(Fore.RED + "Privalote įvestį filmo režisierių" + Style.RESET_ALL)
            continue
        break

    while True:
        try:
            year = int(input("Įrašykite filmo sukūrimo metus: "))
            if year < 1900 or year > 2025:
                print(Fore.RED + "Neteisingi metai. Veskite dar kartą" + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + "Įvedėtė neteisingą formatą. Veskite dar kartą" + Style.RESET_ALL)
            continue

    age_rating = input("Įrašykite filmo amžiaus reitingą (jeigu yra): ").strip()

    new_movie = Movie(name, duration, genre, director, year, age_rating)
    festival.movie_dict[name] = new_movie
    save_movie_list(festival.movie_dict)
    print("Filmas pridėtas sėkmingai.")

def show_movies(festival):
    if not festival.movie_dict:
        print(Fore.RED + "Filmų sąrašas tuščias." + Style.RESET_ALL)
    else:
        print("\nFilmų sąrašas:")
        for i, movie in enumerate(festival.movie_dict.values(), start=1):
            print(f"{i}. {movie.__repr__()}")

def show_movies_extended(festival):
    if not festival.movie_dict:
        print(Fore.RED + "Filmų sąrašas tuščias." + Style.RESET_ALL)
    else:
        print("\nDetali filmų peržiūra:")
        for i, movie in enumerate(festival.movie_dict.values(), start=1):
            print(f"{i}. {movie}")

def delete_movie(festival):
    if not festival.movie_dict:
        print(Fore.RED + "Nėra filmų, kuriuos būtų galima pašalinti." + Style.RESET_ALL)
        return

    show_movies(festival)
    movie_to_delete = input("Įveskite filmo pavadinimą, kurį norėtumėte pašalinti: ").strip()
    if festival.movie_dict.pop(movie_to_delete, None):
        save_movie_list(festival.movie_dict)
        print(f"Filmas '{movie_to_delete}' pašalintas.")
    else:
        print(Fore.RED + "Filmas neegzistuoja." + Style.RESET_ALL)

def update_movie(festival):
    if not festival.movie_dict:
        print(Fore.RED + "Nėra filmų, kuriuos būtų galima redaguoti." + Style.RESET_ALL)
        return

    show_movies(festival)
    movie_to_change = input("Įveskite filmo pavadinimą, kurį norite redaguoti: ").strip()
    movie = festival.movie_dict.get(movie_to_change)

    if not movie:
        print(Fore.RED + "Toks filmas nerastas!" + Style.RESET_ALL)
        return

    print("Redaguojate:")
    print(movie)
    print("1. Pakeisti pavadinimą\n2. Pakeisti trukmę\n3. Pakeisti žanrą\n"
            "4. Pakeisti režisierių\n5. Pakeisti metus\n6. Pakeisti amžiaus reitingą")

    choice = input("Įveskite pasirinkimą: ").strip()

    if choice == "1":
        while True:
            new_name = input("Įveskite naują pavadinimą: ").strip()
            if not new_name:
                print(Fore.RED + "Pavadinimas negali būtu tuščias." + Style.RESET_ALL)
                continue
            if new_name in festival.movie_dict:
                print(Fore.RED + "Pavadinimas jau egzistuoja" + Style.RESET_ALL)
                continue
            if new_name == movie_to_change:
                print(Fore.RED + "Pavadinimas negali būti toks pats kaip ir senasis." + Style.RESET_ALL)
                continue
            festival.movie_dict[new_name] = festival.movie_dict.pop(movie_to_change)
            festival.movie_dict[new_name].name = new_name
            break

    elif choice == "2":
        while True:
            try:
                new_duration = int(input("Įveskite naują trukmę (minutėmis): "))
                if new_duration < 1:
                    print(Fore.RED + "Mažiausia filmo trukmė yra 1 minutė" + Style.RESET_ALL)
                    continue
                else:
                    new_duration = movie.duration
                    break
            except ValueError:
                print(Fore.RED + "Neteisingas skaičių formatas." + Style.RESET_ALL)
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
                print(Fore.RED + "Režisierius jau turi tokį vardą." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Privalote įvesti režisierių" + Style.RESET_ALL)
                continue


    elif choice == "5":
        while True:
            try:
                new_year = int(input("Įveskite naujus metus: "))
                if new_year < 1900 or new_year > 2025:
                    print(Fore.RED + "Ivesti neteisingi metai." + Style.RESET_ALL)
                    continue
                else:
                    new_year = movie.year
                    break
            except ValueError:
                print(Fore.RED + "Neteisingas skaičių formatas." + Style.RESET_ALL)
                continue
    
    elif choice == "6":
        movie.age_rating = input("Įveskite naują amžiaus reitingą: ").strip()
    else:
        print(Fore.RED + "Neteisingas pasirinkimas." + Style.RESET_ALL)
        return

    save_movie_list(festival.movie_dict)
    print(f"Filmas '{movie.name}' paredaguotas sėkmingai.")

def search_movie(festival):
    if not festival.movie_dict:
        print(Fore.RED + "Filmų sąrašas tuščias." + Style.RESET_ALL)
        return

    print("\nPaieška pagal:\n1. Pavadinimą\n2. Režisierių")
    choice = input("Įveskite pasirinkimą: ").strip()

    if choice == "1":
        movie_name_part = input("Įveskite filmo pavadinimą: ").strip().lower()
        found_movies = [movie for movie in festival.movie_dict.values() if movie_name_part in movie.name.lower()]
        if found_movies:
            print("Rasti filmai:")
            for movie in found_movies:
                print(movie)
        else:
            print(Fore.RED + "Filmai nerasti." + Style.RESET_ALL)

    elif choice == "2":
        director_name = input("Įveskite režisieriaus vardą: ").strip().lower()
        director_movies = [movie for movie in festival.movie_dict.values() if movie.director.lower() == director_name]
        if director_movies:
            print("Rasti filmai:")
            for movie in director_movies:
                print(movie)
        else:
            print(Fore.RED + "Toks režisierius festivalyje nedalyvauja." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Neteisingas pasirinkimas." + Style.RESET_ALL)

def rank_movie(festival, username):
    show_movies(festival)
    to_rank = input("Įrašykite filmo pavadinimą, kuriam norite suteikti reitingą: ").strip()
    movie = festival.movie_dict.get(to_rank)

    if not movie:
        print(Fore.RED + "Filmas nerastas." + Style.RESET_ALL)
        return
    
    if username in movie.ranking_users:
        print(Fore.RED + "Jūs jau reitingavote šį filmą." + Style.RESET_ALL)
        return

    while True:
        try:
            user_ranking = int(input("Įrašykite reitingą (1-10): "))
            if 1 <= user_ranking <= 10:
                movie.ranking_points += user_ranking
                movie.user_ranking_count += 1
                movie.ranking = movie.ranking_points / movie.user_ranking_count
                movie.ranking_users.append(username)
            else:
                print(Fore.RED + "Reitingas turi būti tarp 1 ir 10." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "Neteisingas reitingo formatas." + Style.RESET_ALL)

        comment = input("Įrašykite komentarą: ")
        movie.ranking_comment.append(comment)
        save_movie_list(festival.movie_dict)
        print("Ačiū, Jūsų reitingas išsaugotas.")
        break

def get_movie_reservation_count(movie):
    reservations = 0
    for reservation in movie.reservations:
        reservations += reservation.ticket_count
    return reservations

def show_most_popular_movies(festival):
    if not festival.movie_dict:
        print(Fore.RED + "Filmų nėra." + Style.RESET_ALL)
        return

    movie_ranking = sorted(festival.movie_dict.values(), key=get_movie_reservation_count, reverse=True)

    print("Populiariausi filmai:")
    for i, movie in enumerate(movie_ranking, start=1):
        print(f"{i}. {movie.name} - {get_movie_reservation_count(movie)} rezervacijų.")