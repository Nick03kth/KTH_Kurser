import csv
from Drama import Drama


def read_dramas_from_file(filename):
    dramas = []
    with open(filename, mode='r') as file:
        csv_reader = csv.reader(file) #Comma seperated values ger oss värdena som är separerade av kommatecken.
        next(csv_reader)  # Hoppa över första raden med rubriker
        for row in csv_reader:
            drama = Drama(
                name=row[0],
                rating=row[1],
                actors=row[2],
                viewship_rate=row[3],
                genre=row[4],
                director=row[5],
                writer=row[6],
                year=row[7],
                no_of_episodes=row[8],
                network=row[9]
            )
            dramas.append(drama)
    return dramas

def search_drama_by_name(dramas, name): #Exempel på söknings funktion som letar efter namn på ett drama, kollar om den finns.
    for drama in dramas:
        if drama.name.lower() == name.lower(): #omvandlar strängar till små bokstäver
            return drama
    return None

def display_dramas(dramas): #En funktion för att visa alla objekt fint
    """Skriver ut information om varje Drama-objekt i listan."""
    i=1 # Numrerar objekten för att hålla koll
    for drama in dramas:
        print(i, drama)
        print('-' * 40)  # Skriv ut en separator för tydlighet
        i= i+1 
#OBS ta bort kommentarsmarkörer för att testa programmet!!!
#Prova funktionen som läser in filen
#dramas = read_dramas_from_file("C:\\Users\\nick0\\Downloads\\kdramaMini.txt")
#display_dramas(Objekten)
#search_name = "Legend of the Blue Sea"  # Exempel på ett drama att söka efter
#result = search_drama_by_name(dramas, search_name)

#if result:
  #  print(f"Drama '{search_name}' found:\n{result}")
#else:
 #   print(f"Drama '{search_name}' not found.")


"""
# En funktion för att testa drama klassen
def test_drama_class():
    # Skapa två Drama-objekt med exempeldata !!!!!
    drama1 = Drama(
        name="The Great Adventure",
        rating="8.7",
        actors="John Doe, Jane Smith",
        viewship_rate="1.5",
        genre="Action",
        director="Emily Clarke",
        writer="Michael Brown",
        year="2021",
        no_of_episodes="10",
        network="ABC"
    )
    
    drama2 = Drama(
        name="Mysterious Love",
        rating="9.2",
        actors="Alice Johnson, Bob Lee",
        viewship_rate="2.1",
        genre="Romance",
        director="Sarah Williams",
        writer="David Wilson",
        year="2019",
        no_of_episodes="8",
        network="NBC"
    )
    
    # Anropa __str__-metoden
    print("Drama 1:\n", drama1)
    print("\nDrama 2:\n", drama2)
    
    # Anropa __lt__-metoden för att jämföra ratings
    print("\nIs Drama 1 rating less than Drama 2 rating? ", drama1 < drama2) #---> TRUE/FALSE
    
    # Anropa is_recent-metoden
    print("\nIs Drama 1 recent? ", drama1.is_recent())
    print("Is Drama 2 recent? ", drama2.is_recent())
    
    # Anropa rating_times_viewship-metoden
    print("\nDrama 1 rating times viewship: ", drama1.rating_times_viewship())
    print("Drama 2 rating times viewship: ", drama2.rating_times_viewship())
    
    # Anropa get_genre-metoden
    print("\nDrama 1 genre: ", drama1.get_genre())
    print("Drama 2 genre: ", drama2.get_genre())

# Kör testprogrammet
#test_drama_class()
"""