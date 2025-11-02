class Drama:
    def __init__(self, name, rating, actors, viewship_rate, genre, director, writer, year, no_of_episodes, network):
        self.name = name
        self.rating = float(rating)
        self.actors = actors
        self.viewship_rate = float(viewship_rate)
        self.genre = genre
        self.director = director
        self.writer = writer
        self.year = int(year)
        self.no_of_episodes = int(no_of_episodes)
        self.network = network

    def __str__(self): #För varje objekt kan vi printa ut dess atribut
        return (f"Name: {self.name}, Rating: {self.rating}, Actors: {self.actors}, "
                f"Viewship Rate: {self.viewship_rate}, Genre: {self.genre}, "
                f"Director: {self.director}, Writer: {self.writer}, "
                f"Year: {self.year}, No of Episodes: {self.no_of_episodes}, Network: {self.network}")
    
    def __lt__(self, other): #Less than metod för att kunna jämföra. Sätter standard för våra .sort metoder
        return self.rating < other.rating
    
    def is_recent(self):
        """Returnerar True om dramat är skapat efter 2020."""
        return self.year > 2020 
    
    def rating_times_viewship(self):
        """Beräknar och returnerar produkten av rating och Viewship Rate."""
        return self.rating * self.viewship_rate

    def get_genre(self):
        """Returnerar dramatets genre."""
        return self.genre