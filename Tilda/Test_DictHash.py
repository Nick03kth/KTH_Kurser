import csv
from Drama import Drama
from hashtable import Hashtable #Om deluppgift 1 importerar vi Hashdict 

#Skapa drama obj:
def read_dramas_from_file(filename):
    dramas = Hashtable()
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
            dramas.store(drama.name,drama)
    return dramas

dramas = read_dramas_from_file("C:\\Users\\nick0\\Downloads\\kdramaMini.txt")

print(dramas.search("Legend of the Blue Sea"))

dramas.count_max_collisions()