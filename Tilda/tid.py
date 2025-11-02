"""
import timeit
from song import Song

def linsok(lista, testartist):
    for element in lista:
        if element.artist_name == testartist:
            return element
    return None #Går genom varje el. i listan fr. början t. slut. tills hittat match
#O(n) värsta fall. Bra för små listor. 

def binsok(lista, testartist):
    low = 0
    high = len(lista) - 1
    while low <= high:
        mid = (low + high) // 2
        if lista[mid].artist_name == testartist:
            return lista[mid]
        elif lista[mid].artist_name < testartist:
            low = mid + 1
        else:
            high = mid - 1
    return None 
#Tar in sorterad lista. Delar upp i två delar. Fokus bara på den halva som har obj. 
#O(log(n)), mycket snabbare än linj soknin. Men måste sortera i förväg

def build_dict(lista): 
    return {song.artist_name: song for song in lista} #Varje nyckel är artistnamn. varje värde är själva song-obj. Sedan itererar.

def hashtabell_search(song_dict, testartist):
    return song_dict.get(testartist, None)
    #O(1); anv hash-värde (=artistnamn) vi kan DIREKt slå upp värdet i dictionary.
#.get metoden hämtar värdet associerad med nyckeln testartist. Om finns kmr returnera.

def readfile(file_path):
    songs = []
    with open(file_path, encoding='latin1') as file:
        for line in file:
            # OBS varje rad har format: trackid<SEP>låt-id<SEP>artistnamn<SEP>låt-titel
            parts = line.strip().split('<SEP>')
            if len(parts) == 4:
                track_id, song_id, artist_name, song_title = parts
                song = Song(track_id, song_id, artist_name, song_title)
                songs.append(song)
    return songs

def main():

    filename = "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\unique_tracks.txt"

    lista = readfile(filename)
    n = len(lista[0:250000])

    print("Antal element =", n)

    sista = lista[n-1]
    testartist = sista.artist_name

    # Linjärsökning
    linjtid = timeit.timeit(stmt = lambda: linsok(lista, testartist), number = 250000)
    print("Linjärsökningen tog", round(linjtid, 4) , "sekunder")

    # Binärsökning (sortera listan först)
    lista.sort(key=lambda song: song.artist_name)
    bintid = timeit.timeit(stmt=lambda: binsok(lista, testartist), number=250000)
    print("Binärsökningen tog", round(bintid, 4), "sekunder")

    # Hashtabellssökning (bygg dictionary och sök)
    song_dict = build_dict(lista)
    hashtid = timeit.timeit(stmt=lambda: hashtabell_search(song_dict, testartist), number=250000)
    print("Hashtabellssökningen tog", round(hashtid, 4), "sekunder")

main()
"""
import timeit
from song import Song

def linsok(lista, testartist):
    for element in lista:
        if element.artist_name == testartist:
            return element
    return None

def binsok(lista, testartist):
    low = 0
    high = len(lista) - 1
    while low <= high:
        mid = (low + high) // 2
        if lista[mid].artist_name == testartist:
            return lista[mid]
        elif lista[mid].artist_name < testartist:
            low = mid + 1
        else:
            high = mid - 1
    return None

def build_dict(lista):
    return {song.artist_name: song for song in lista}

def hashtabell_search(song_dict, testartist):
    return song_dict.get(testartist, None)

def readfile(file_path):
    songs = []
    with open(file_path, encoding='latin1') as file:
        for line in file:
            # Each line has the format: trackid<SEP>låt-id<SEP>artistnamn<SEP>låt-titel
            parts = line.strip().split('<SEP>')
            if len(parts) == 4:
                track_id, song_id, artist_name, song_title = parts
                song = Song(track_id, song_id, artist_name, song_title)
                songs.append(song)
    return songs

def run_tests_for_list_size(lista, testartist, n):
    print(f"Testar för {n} element...")

    # Slicing för att ta mindre del av listan
    mindreLista = lista[:n]

    # Linjärsökning
    linjtid = timeit.timeit(stmt=lambda: linsok(mindreLista, testartist), number=1000)
    print(f"Linjärsökningen tog {round(linjtid, 4)} sekunder")

    # Binärsökning (sortera listan först)
    mindreLista.sort(key=lambda song: song.artist_name)
    bintid = timeit.timeit(stmt=lambda: binsok(mindreLista, testartist), number=1000)
    print(f"Binärsökningen tog {round(bintid, 4)} sekunder")

    # Hashtabellssökning (bygg dictionary och sök)
    song_dict = build_dict(mindreLista)
    hashtid = timeit.timeit(stmt=lambda: hashtabell_search(song_dict, testartist), number=1000)
    print(f"Hashtabellssökningen tog {round(hashtid, 4)} sekunder")

def main():
    filename = "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\unique_tracks.txt"

    # Läs in hela filen
    lista = readfile(filename)
    n = len(lista)
    print("Antal element =", n)

    # Använd sista artisten som testartist
    sista = lista[n-1]
    testartist = sista.artist_name

    # Testa för olika storlekar av listor
    run_tests_for_list_size(lista, testartist, 250000)
    run_tests_for_list_size(lista, testartist, 500000)
    run_tests_for_list_size(lista, testartist, 1000000)

main()