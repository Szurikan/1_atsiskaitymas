class Movie:
    def __init__(self,name,duration,genre,director,year,age_rating="",session_time=None,tickets=10,ranking_points=0,user_ranking_count=0,ranking=0, reservations=0
    ):
        self.name = name
        self.duration = duration
        self.genre = genre
        self.director = director
        self.year = year
        self.age_rating = age_rating
        self.session_time = session_time
        self.tickets = tickets
        self.ranking_points = ranking_points
        self.user_ranking_count = user_ranking_count
        self.ranking = ranking
        self.reservations = reservations

    def __str__(self):
        return (
            f"\nPavadinimas: {self.name}\n"
            f"Trukmė: {self.duration}\n"
            f"Žanras: {self.genre}\n"
            f"Režisierius: {self.director}\n"
            f"Metai: {self.year}\n"
            f"Amžiaus cenzas: {self.age_rating}\n"
            f"Įvertinimų skaičius: {self.user_ranking_count}\n"
            f"Bendras reitingas: {self.ranking:.1f}\n"
        )

    def __repr__(self):
        return f"{self.name} ({self.year})"