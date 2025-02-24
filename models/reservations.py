class Reservation:
    def __init__(self, username, movie_name, ticket_count, total_price):
        self.username = username
        self.movie_name = movie_name
        self.ticket_count = ticket_count
        self.total_price = total_price
        
    def __str__(self):
        return f"{self.username} filmui {self.movie_name} rezervavo {self.ticket_count} bilietus. Bendra užsakymo kaina: {self.total_price} EUR"