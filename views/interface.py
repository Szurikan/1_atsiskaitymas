from services.data_handler import save_movie_list, load_movie_list
from models.festival import Festival
from models.reservations import Reservation
import colorama
from colorama import Fore, Back, Style

colorama.init() # sitas dalykas kazkodel padaro kad man normaliai rodo spalvas terminale paleidus exe faila, o ne skaicius kazkokius

def start_program(): # paleidzia pirmine programa, kurioje vartotojas iveda duomenis kad galime butu paziureti kas jis toks
    festival = Festival()
    festival.movie_dict = load_movie_list()

    print(Fore.RED + Back.BLUE +'Sveiki atvykę į festivalį! Jeigu esate organizatorius, rašykite "org".' + Style.RESET_ALL)
    username = input(Fore.CYAN +  "Įrašykite vartotojo vardą: " + Style.RESET_ALL).strip()
    if username == "org":
        show_menu_org(festival)
    else:
        show_menu_user(festival, username)

    return username

def show_menu_org(festival): # cia yra organizatoriaus meniu
    while True:
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
            festival.add_movie()
        elif choice == "2":
            festival.show_movies()
        elif choice == "3":
            festival.delete_movie()
        elif choice == "4":
            festival.update_movie()
        elif choice == "5":
            festival.show_movies_extended()
        elif choice == "6":
            festival.search_movie()
        elif choice == "7":
            festival.add_session_time()
        elif choice == "8":
            festival.show_most_popular_movies()
        elif choice == "9":
            festival.show_reservations()
        elif choice == "10":
            festival.show_income()
        elif choice == "11":
            break
        else:
            print("Neteisingas pasirinkimas.")


def show_menu_user(festival, username): # cia yra paprasta vartotojo meniu
    print(f"\nSveiki, {username}!")
    while True:
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
            festival.show_movies()
        elif choice == "2":
            festival.show_movies_extended()
        elif choice == "3":
            festival.search_movie()
        elif choice == "4":
            festival.show_sessions(username)
        elif choice == "5":
            festival.rank_movie(username)
        elif choice == "6":
            festival.show_most_popular_movies()
        elif choice == "7":
            break
        else:
            print("Neteisingas pasirinkimas.")