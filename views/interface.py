from services.data_handler import save_movie_list, load_movie_list
from models.festival import Festival
from models.reservations import Reservation
from services.film_service import add_movie, show_movies, show_movies_extended, delete_movie, update_movie,search_movie, rank_movie, show_most_popular_movies
from services.reservations_service import add_session_time, show_sessions, show_reservations, show_income
import colorama
from colorama import Fore, Back, Style
import os

colorama.init() # sitas dalykas kazkodel padaro kad man normaliai rodo spalvas terminale paleidus exe faila, o ne skaicius kazkokius

def start_program(): # paleidzia pirmine programa, kurioje vartotojas iveda duomenis kad galime butu paziureti kas jis toks
    festival = Festival()
    festival.movie_dict = load_movie_list()

    print(Fore.RED + Back.BLUE +'Sveiki atvykę į festivalį! Jeigu esate organizatorius, rašykite "org".' + Style.RESET_ALL)
    
    while True:
        username = input(Fore.CYAN +  "Įrašykite vartotojo vardą: " + Style.RESET_ALL).strip()
        if username == "org":
            password = input("Įveskite slaptažodį: ")
            if password == "org":
                show_menu_org(festival)
                break
            else:
                print(Fore.RED + "Įvedėte neteisingą slaptažodį." + Style.RESET_ALL)
        else:
            show_menu_user(festival, username)
            break

    return username

def show_menu_org(festival): # cia yra organizatoriaus meniu
    while True:
        os.system("cls")
        print(Fore.YELLOW +
            "\nOrganizatoriaus MENIU:\n" +
            Fore.CYAN + "1. Pridėti filmą\n"
            "2. Parodyti filmų sąrašą\n"
            "3. Pašalinti filmą\n"
            "4. Redaguoti filmą\n"
            "5. Detali filmų peržiūra\n"
            "6. Filmų paieška\n"
            "7. Pridėti seanso laiką\n"
            "8. Rodyti populiariausius festivalio filmus\n"
            "9. Rodyti rezervacijų sąrašą\n"
            "10. Rodyti uždirbtas pajamas\n"
            "11. Uždaryti programą\n"+ Style.RESET_ALL
        )
        choice = input("Įveskite veiksmo numerį: ").strip()
        if choice == "1":
            add_movie(festival)
        elif choice == "2":
            show_movies(festival)
        elif choice == "3":
            delete_movie(festival)
        elif choice == "4":
            update_movie(festival)
        elif choice == "5":
            show_movies_extended(festival)
        elif choice == "6":
            search_movie(festival)
        elif choice == "7":
            add_session_time(festival)
        elif choice == "8":
            show_most_popular_movies(festival)
        elif choice == "9":
            show_reservations(festival)
        elif choice == "10":
            show_income(festival)
        elif choice == "11":
            print("Ačiū. VIso gero.")
            break
        else:
            print(Fore.RED + "Neteisingas pasirinkimas." + Style.RESET_ALL)
        input("\nSpauskite Enter, jeigu norite tęsti.")


def show_menu_user(festival, username): # cia yra paprasta vartotojo meniu
    print(f"\nSveiki, {username}!")
    while True:
        os.system("cls")
        print(
            Fore.YELLOW + "\nVartotojo MENIU:\n" +
            Fore. CYAN + "1. Parodyti filmų sąrašą\n"
            "2. Detali filmų peržiūra\n"
            "3. Filmų paieška\n"
            "4. Rodyti seansus ir rezervuoti bilietus\n"
            "5. Reitinguoti filmą\n"
            "6. Populiariausių festivalio filmų sąrašas.\n"
            "7. Uždaryti programą\n" + Style.RESET_ALL
        )
        choice = input("Įveskite veiksmo numerį: ").strip()
        if choice == "1":
            show_movies(festival)
        elif choice == "2":
            show_movies_extended(festival)
        elif choice == "3":
            search_movie(festival)
        elif choice == "4":
            show_sessions(festival, username)
        elif choice == "5":
            rank_movie(festival, username)
        elif choice == "6":
            show_most_popular_movies(festival)
        elif choice == "7":
            print("Ačiū. VIso gero.")
            break
        else:
            print(Fore.RED + "Neteisingas pasirinkimas." + Style.RESET_ALL)
        input("\nSpauskite Enter, jeigu norite tęsti.")