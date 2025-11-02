class Syntaxfel(Exception):
    """Specialanpassat undantag för att hantera syntaxfel med specifika meddelanden."""
    pass

class Node:
    def __init__(self, value=None):
        # Initierar en nod med ett värde och en referens till nästa nod.
        self.value = value
        self.next = None

class LinkedQueue:
    def __init__(self):
        # Initierar en tom kö.
        self.first = None
        self.last = None

    def is_empty(self):
        # Kontrollerar om kön är tom.
        return self.first is None

    def enqueue(self, value):
        # Lägger till ett nytt värde i kön.
        new_node = Node(value)
        if self.is_empty():
            self.first = self.last = new_node
        else:
            self.last.next = new_node
            self.last = new_node

    def dequeue(self):
        # Tar bort och returnerar det första värdet i kön.
        if self.is_empty():
            raise IndexError("Queue is empty")
        value = self.first.value
        self.first = self.first.next
        if self.first is None:
            self.last = None
        return value

    def peek(self):
        # Tittar på det första värdet i kön utan att ta bort det.
        if not self.is_empty():
            return self.first.value
        return None

    def to_string(self):
        # Returnerar alla element i kön som en sträng.
        result = ""
        current = self.first
        while current:
            result += current.value
            current = current.next
        return result

# Lista över alla kända atomnamn.
atomlist = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
            'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
            'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs',
            'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
            'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
            'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
            'Ds', 'Rg', 'Cn', 'Fl', 'Lv']

class SyntaxError(Exception):
    # Specialanpassat undantag för att hantera syntaxfel.
    pass

def FixQ(atom):
    # Skapar en kö från en sträng och lägger till ett sluttecken.
    q = LinkedQueue()
    for element in atom:
        q.enqueue(element)
    q.enqueue("-")  # Indikerar slutet av kön.
    return q

def check(atom):
    # Kontrollerar om formeln är korrekt genom att starta analysen.
    try:
        UseRead(atom)
        return "Formeln är syntaktiskt korrekt"
    except SyntaxError as error:
        return str(error)

def Readmolyekyl(atom):
    # Läser en molekyl och kontrollerar dess struktur rekursivt.
    readgroup(atom)
    if atom.peek() == "(" or atom.peek().isupper(): 
        Readmolyekyl(atom)  # Rekursivt anrop om det finns fler grupper eller molekyler.

def UseRead(atom):
    # Huvudmetoden som körs tills kön når sluttecknet.
    while atom.peek() != "-": 
        Readmolyekyl(atom)

def ReadAtom(atom):
    # Läser en atom och kontrollerar dess giltighet.
    upper = ReadUpper(atom)
    lower = None 
    if atom.peek().islower():
        lower = ReadLower(atom)
        if (upper + lower) not in atomlist:
            end_print = printname(atom)
            raise SyntaxError("Okänd atom vid radslutet " + end_print)
    else:
        if upper not in atomlist:
            end_print = printname(atom)
            raise SyntaxError("Okänd atom vid radslutet " + end_print)

def ReadUpper(atom):
    # Läser en stor bokstav (början av en atom).
    if atom.peek().isupper():
        big = atom.dequeue()
        return big 
    else:
        end_print = printname(atom)
        raise SyntaxError("Saknad stor bokstav vid radslutet " + end_print)

def ReadLower(atom):
    # Läser en liten bokstav om den finns.
    small = atom.dequeue()
    return small 

def readnumber(atom):
    # Läser ett tal och kontrollerar om det är giltigt.
    partial_number = ""
    if atom.peek() == "0":
        atom.dequeue()  
        end_print = printname(atom)
        raise SyntaxError("För litet tal vid radslutet " + end_print)
    elif atom.peek().isdigit():
        partial_number = atom.dequeue()
        while atom.peek().isdigit() and (not atom.is_empty()):  
            partial_number += atom.dequeue()
        if int(partial_number) < 2:
            end_print = printname(atom)
            raise SyntaxError("För litet tal vid radslutet " + end_print)
    else:
        end_print = printname(atom)
        raise SyntaxError("Saknad siffra vid radslutet " + end_print)

def readgroup(atom):
    # Läser en grupp och hanterar parenteser samt eventuella nummer.
    if atom.peek() == "(":
        atom.dequeue() 
        Readmolyekyl(atom)  # Läser en hel grupp rekursivt.
        if atom.peek() == ")":
            atom.dequeue()
            if atom.peek().isnumeric(): 
                readnumber(atom)
            else:
                end_print = printname(atom)
                raise SyntaxError("Saknad siffra vid radslutet " + end_print)
        else:
            end_print = printname(atom)
            raise SyntaxError("Saknad högerparentes vid radslutet " + end_print)
    elif atom.peek().isupper() or atom.peek().islower():
        ReadAtom(atom)
        if atom.peek().isnumeric():
            readnumber(atom)
    else:
        end_print = printname(atom)
        raise SyntaxError("Felaktig gruppstart vid radslutet " + end_print)

def printname(atom):
    # Returnerar resterande tecken i kön som en sträng.
    original_namn = ""
    while not atom.is_empty() and atom.peek() != "-":
        tecken = atom.dequeue()
        original_namn += tecken
    return original_namn

def main():
    # Huvudfunktionen som tar användarens input och kontrollerar formeln.
    atom = input()
    while atom != "#":
        try:
            atom1 = FixQ(atom)
            resultat = check(atom1)
            print(resultat)
            atom = input()
        except SyntaxError:
            atom1 = input()

if __name__ == "__main__":
    main()
