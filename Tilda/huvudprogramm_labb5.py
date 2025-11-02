from linkedQFile2 import *
from SolutionFound import SolutionFound

# Läser in orden från en fil och returnerar "ordlista".
def las_in_ordlista(filnamn):
    ordlista = []
    with open(filnamn, 'r') as fil:
        for rad in fil:
            ord = rad.strip()  # Tar bort newline och eventuella extra mellanslag
            ordlista.append(ord)  # Lägg till ordet i listan
    return ordlista

# Byter en bokstav i ett ord vid ett specifikt index
def byt_bokstav(strang, ny_bokstav, index):
    if index < 0 or index >= len(strang):  # Kontrollera att indexet är giltigt
        raise ValueError("Indexet är utanför strängens längd")
    
    return strang[:index] + ny_bokstav + strang[index+1:]  # Skapar nytt ord genom att byta ut bokstaven vid det givna indexet

# Skriver ut kedjan av ord från start till slut genom rekursion
def writechain(node):
    if node.parent is not None:
        writechain(node.parent)  # Funktionen anropas igen i funktionen (rekursion) 
    print(node.word)

# Genererar alla möjliga barn genom att byta ut en bokstav i taget
def make_children(current_node, ordlista, letters='abcdefghijklmnopqrstuvxyzåäö'):
    children = []
    for j in range(len(current_node.word)):
        for letter in letters:
            tempord = byt_bokstav(current_node.word, letter, j)  # Byter bokstav på påsitionen j i ordet
            if tempord in ordlista and tempord != current_node.word:  # Kontrollera om det nya ordet finns i ordlista  
                children.append(ParentNode(tempord, current_node))  # Skapa nytt ParentNode med det nya ordet 
    return children  # Returnerar lsitan med alla giltiga barn

# Funktion som använder en kö för att hitta en väg från ett startord till ett slutord
def add_to_queue(start_word, target_word, ordlista):
    try:
        start_node = ParentNode(start_word)  # Skapa ParentNode för startordet
        q = LinkedQ()
        visited = []  # Lista som lagrar alla besökta ord
        visited.append(start_word)
        q.enqueue(start_node)  # Lägg till startordet i kön

        while not q.is_empty():
            current_node = q.dequeue()  # Ta ut ett ord ur kön

            if current_node.word == target_word:
                writechain(current_node)
                raise SolutionFound()  # Avbryt och signalera att vi hittat en lösning

            children = make_children(current_node, ordlista)
            for child in children:
                if child.word not in visited:
                    visited.append(child.word)  # Markera barnet som besökt(läggs till i visited listan)
                    q.enqueue(child)

        print('Det finns ingen väg')
    except SolutionFound:
        print('Det finns en väg')

# Läser in ordlistan från filen och kör programmet
ordlista = las_in_ordlista('C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\word3.txt')
add_to_queue('blå', 'röd', ordlista)