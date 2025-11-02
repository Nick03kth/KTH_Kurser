from linkedQFile import LinkedQ

# Hårdkodad lista med tillåtna atomer
ATOM_LIST = """
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr
Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd
In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf
Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm
Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Fl Lv
"""
ATOMS = set(ATOM_LIST.split())

class Syntaxfel(Exception):
    """Specialiserat undantag för syntaxfel"""
    def __init__(self, message):
        super().__init__(message)

def read_formula(queue):
    """Huvudfunktion för att kontrollera hela molekylen."""
    read_mol(queue)

def read_mol(queue):
    """Kontrollerar flera grupper av molekyler."""
    read_group(queue)
    while not queue.is_empty():
        read_group(queue)  # Fortsätt kontrollera fler grupper

def read_group(queue):
    # Läser en grupp och hanterar parenteser samt eventuella nummer.
    if queue.peek() == "(":
        print("Första villkoret")
        queue.dequeue() 
        read_mol(queue)  # Läser en hel grupp rekursivt.
        print("Kollat genom hela gruppen rekursivt")
        print(queue.rest()+"hej")
        
        
        
    if queue.peek() == ")":
        print("Andra villkorssatsen")
        queue.dequeue() #Ta bort ")"
        print(queue.rest())
        if not queue.is_empty() and queue.peek().isdigit():
            print("Nummer efter slutparantesen")
            read_number(queue)  # Läs numret om det finns
            print(queue.rest())
        else:
            raise Syntaxfel()
        
    #else:
           # raise SyntaxError("Saknad högerparentes vid radslutet " + queue.rest())
    
    
        
    else:
        
        read_atom(queue)  # Läs en atom
        print("Vi läste in en atom, resten: " + str(queue.rest()))
        # Kontrollera om det finns ett nummer efter atomen
        if not queue.is_empty() and queue.peek().isdigit():
            print("Atomen hade nummer efter sig...")
            read_number(queue)  # Läs numret om det finns
"""
    """ """Kontrollerar en atom eller en gruppering med parenteser.""" """
    if queue.is_empty():
        raise Syntaxfel("Felaktig gruppstart vid radslutet " + queue.rest())

    if queue.peek() == '(':
        queue.dequeue()  # Ta bort '('
        read_mol(queue)  # Kontrollera innehållet i parenteserna
        
       
        # Kontrollera om det finns ett nummer efter stängningsparentesen
        if not queue.is_empty() and queue.peek().isdigit():
            read_number(queue)  # Läs numret om det finns
    
    elif queue.peek()==")":
        queue.dequeue()
         #Gå vidare nu när vi tagit bort slutparantesen

    else:
        read_atom(queue)  # Läs en atom

        # Kontrollera om det finns ett nummer efter atomen
        if not queue.is_empty() and queue.peek().isdigit():
            read_number(queue)  # Läs numret om det finns
"""

def read_atom(queue):
    """Kontrollerar att atomen följer syntaxen för <atom>."""
    read_capital_letter(queue)  # Första tecknet måste vara stor bokstav
    if not queue.is_empty() and queue.peek().islower():
        read_lowercase_letter(queue)  # Tillåt liten bokstav efter

def read_capital_letter(queue):
    """Kontrollerar att det första tecknet är en stor bokstav."""
    if queue.is_empty() or not queue.peek().isupper():
        raise Syntaxfel("Saknad stor bokstav vid radslutet " + queue.rest())
    
    atom = queue.dequeue()  # Ta bort den stora bokstaven
    if atom not in ATOMS:
        raise Syntaxfel("Okänd atom vid radslutet " + queue.rest())
    

def read_lowercase_letter(queue):
    """Kontrollerar att det andra tecknet, om det finns, är en liten bokstav."""
    if not queue.is_empty() and queue.peek().islower():
        queue.dequeue()  # Ta bort liten bokstav om den finns
    
def read_number(queue):
    """Kontrollerar att numret är >= 2 enligt <num> och inte är ett tal som börjar med en nolla, t.ex. 010."""
    number_str = ""
    first_digit = queue.dequeue()

    if first_digit == '0':  # Kolla första talet
        raise Syntaxfel("För litet tal vid radslutet " + queue.rest())
    
    number_str += first_digit
    while not queue.is_empty() and queue.peek().isdigit():
        number_str += queue.dequeue()  # Gå igenom talet och ta bort varje kollad siffra

    # Kontrollera att hela talet är minst 2
    if int(number_str) < 2:
        raise Syntaxfel("För litet tal vid radslutet " + queue.rest())

def main():
    """Läser in flera rader från standard input och kontrollerar molekylsyntaxen."""
    import sys
    for line in sys.stdin:
        line = line.strip()
        if line == "#":
            break
        queue = LinkedQ()
        for char in line:
            queue.enqueue(char)
        try:
            read_formula(queue)  # Kontrollera formeln
            print("Formeln är syntaktiskt korrekt")
        except Syntaxfel as error:
            print(error)

if __name__ == "__main__":
    main()
