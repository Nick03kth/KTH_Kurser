import timeit

# Funktion som laddar artistnamn från en given fil
def load_artists(filename, encoding="utf-8"):
    artists = []
    with open(filename, 'r', encoding=encoding) as file:
        for line in file:
            columns = line.strip().split('<SEP>')
            if len(columns) >= 4:
                artists.append(columns[2])
    return artists

# Insertion Sort - En O(n^2) algoritm som sorterar stegvis

def insertion_sort(array):
    for idx in range(1, len(array)):
        current_value = array[idx]
        position = idx - 1
        while position >= 0 and current_value < array[position]:
            array[position + 1] = array[position]
            position -= 1
        array[position + 1] = current_value
    return array
#Varje el sätts in på rätt plats i redan sorterad lista. Algoritmen går genom listan fr början till slut.Flyttar större el tills rätt plats hittat.
#O(n^2)
def merge_sort(array):
    if len(array) > 1: #Basfall
        mid_point = len(array) // 2
        left_half = array[:mid_point]
        right_half = array[mid_point:]

        merge_sort(left_half)
        merge_sort(right_half)
        #Fortsätter tills varje del består av 1 el.
        
        left_idx = right_idx = merged_idx = 0

        #Om el mindre läggs till sammanslagnaa list på rätt position (array[merged_idx])
        while left_idx < len(left_half) and right_idx < len(right_half):
            if left_half[left_idx] < right_half[right_idx]:
                array[merged_idx] = left_half[left_idx]
                left_idx += 1 #Flyttar index fram
            else:
                array[merged_idx] = right_half[right_idx]
                right_idx += 1
            merged_idx += 1
            
        while left_idx < len(left_half): #Om el. finns kvar placeras resteni rätt ordn
            array[merged_idx] = left_half[left_idx]
            left_idx += 1
            merged_idx += 1

        while right_idx < len(right_half): #P.S.S om finns el kvar på högersidan
            array[merged_idx] = right_half[right_idx]
            right_idx += 1
            merged_idx += 1
    return array #Sammanslagna listan tbx.

# Merge Sort - En O(n log n) algoritm som rekursivt delar och sorterar listan tills varje del =strl 1(basfall)
#Bra för 1M element jmft insertfkn 
def main():
    filename = "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\unique_tracks.txt"
    artists = load_artists(filename)
    print(f"Totalt antal artister: {len(artists)}")

    # Listor av olika storlekar (n=1000, 10 000, 100 000, 1 000 000)
    data_sizes = [1000, 10000, 100000, 1000000]
    subsets = [artists[:n] for n in data_sizes]

    # Benchmark av Merge Sort
    print("Merge Sort - Tidsmätning:")
    for subset, size in zip(subsets, data_sizes):
        if len(subset) == 0:
            break
        elapsed_time = timeit.timeit(stmt=lambda: merge_sort(subset[:]), number=1)
        print(f"n = {size}: {round(elapsed_time, 4)} sekunder")

    # Benchmark av Insertion Sort
    print("Insertion Sort - Tidsmätning:")
    for subset, size in zip(subsets, data_sizes):
        if len(subset) == 0:
            break
        elapsed_time = timeit.timeit(stmt=lambda: insertion_sort(subset[:]), number=1)
        print(f"n = {size}: {round(elapsed_time, 4)} sekunder")

if __name__ == "__main__":
    main()


# Notering: Merge Sort bör vara snabbare än Insertion Sort vid större dataset på grund av dess lägre tidskomplexitet, speciellt när n växer.
# Insertion Sort fungerar bättre på mindre dataset eftersom overheaden är lägre, men blir ineffektiv snabbt vid större dataset.
#ANALYS: 
#SÖKNIN
#SORTERING