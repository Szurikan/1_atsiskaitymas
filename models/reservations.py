class Reservation:
    def __init__(self, user_name, movie_name, ticket_count):
        self.user_name = user_name
        self.movie_name = movie_name
        self.ticket_count = ticket_count

    def __str__(self):
        return f"{self.user} filmui {self.movie_name} rezervavo {self.ticket_count} bilietus."