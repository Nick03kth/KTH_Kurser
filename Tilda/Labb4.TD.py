from linkedQFile import LinkedQ
def las_in_ordlista(filnamn):
    ordlista = []
    with open(filnamn, 'r') as fil:
        for rad in fil:
            ord = rad.strip()  # Tar bort newline och eventuella extra mellanslag
            ordlista.append(ord)  # Lägg till ordet i listan
    return ordlista

def byt_bokstav(strang, ny_bokstav, index):
    # Kontrollera att indexet är giltigt
    if index < 0 or index >= len(strang):
        raise ValueError("Indexet är utanför strängens längd")
    
    nytt_ord = strang[:index] + ny_bokstav + strang[index+1:]
    print(f"Byter bokstav i '{strang}' på position {index} med '{ny_bokstav}': {nytt_ord}")  # Utskrift för att se bytet
    return nytt_ord

def make_children(ord, ordlista, letters='abcdefghijklmnopqrstuvxyzåäö'):
    gamla = []
    freq = 0
    print(f"Genererar barn för: {ord}")  # Lägg till utskrift
    for j in range(len(ord)):
        for letter in letters:
            tempord = byt_bokstav(ord, letter, j)
            if tempord in ordlista:
                if tempord != ord:
                    if tempord not in gamla:
                        freq += 1
                        gamla.append(tempord)
                        print(f"Nytt barn hittat: {tempord} (från {ord})")  # Utskrift för varje nytt barn

    return freq, gamla

def add_to_queue(startord, slutord, ordlista):
    visited = set()  # Använd en mängd för snabbare sökning och undvik duplicerade besökta ord
    q = LinkedQ()
    q.enqueue(startord)
    visited.add(startord)  # Markera startordet som besökt direkt

    print(f"Startar sökningen från {startord} till {slutord}")
    
    while not q.is_empty():
        value = q.dequeue()
        print(f"Dequeue: {value}, Kvar i kön: {q}")  # Utskrift vid dequeue
        
        freq, gamla = make_children(value, ordlista)
        print(f"Barn för {value}: {gamla}")

        for barnord in gamla:
            if barnord not in visited:  # Kontrollera om barnet har besökts
                q.enqueue(barnord)
                visited.add(barnord)  # Markera barnet som besökt direkt när det läggs i kön
                print(f"Lägger till {barnord} i kön")
                if barnord == slutord:
                    print(f"Det finns en väg till {slutord}")
                    while not q.is_empty():
                        q.dequeue()  # Töm kön
                    return

    print(f"Finns inte väg till {slutord}")

ordlista = las_in_ordlista('C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\word3.txt')
#freq, gamla = make_children('hit', ordlista)
#print(freq)
#print(gamla)
add_to_queue('blå', 'röd', ordlista)
