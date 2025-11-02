from linkedQFile import LinkedQ

class Syntaxfel(Exception):
    """Specialiserat undantag för syntaxfel"""
    def __init__(self, message):
        super().__init__(message)

def read_atom(queue):
    """Kontrollerar att atomen följer syntaxen för <atom>"""
    read_capital_letter(queue)  # Kolla att första tecknet är en stor bokstav
    if not queue.is_empty() and queue.peek().islower():
        read_lowercase_letter(queue)  # Om nästa tecken är en liten bokstav, tillåt det

def read_capital_letter(queue):
    """Kontrollerar att det första tecknet är en stor bokstav enligt <LETTER>"""
    if queue.is_empty() or not queue.peek().isupper():
        raise Syntaxfel("Saknad stor bokstav vid radslutet " + queue.rest())
    queue.dequeue()  # Ta bort det behandlade tecknet

def read_lowercase_letter(queue):
    """Kontrollerar att det andra tecknet, om det finns, är en liten bokstav enligt <letter>"""
    if not queue.is_empty() and queue.peek().islower():
        queue.dequeue()  # Ta bort liten bokstav om den finns

def read_number(queue):
    """Kontrollerar att numret är >= 2 enligt <num> och inte är ett tal som börjar med en nolla, t.ex. 010."""
    number_str = ""
    first_digit= queue.dequeue()

    if first_digit== "0":  #Kolla första talet
        raise Syntaxfel("För litet tal vid radslutet " + queue.rest())
    
    #Om första siffran gilgit lägg tillbaka den och undersök hela talet
    number_str += first_digit
    while not queue.is_empty() and queue.peek().isdigit():
        number_str += queue.dequeue() # Gå igenom talet och ta bort varje kollad siffra

    # Kontrollera att hela talet är minst 2
    if int(number_str) < 2:
        raise Syntaxfel("För litet tal vid radslutet " + queue.rest())

def check_molecule(molecule):
    """Funktion för att kontrollera en molekylsträng"""
    queue = LinkedQ()  # Skapa en ny kö
    for char in molecule:
        queue.enqueue(char)  # Lägg till varje tecken i kön
    try:
        read_atom(queue)  # Kolla att molekylen börjar med ett giltigt atomnamn
        if not queue.is_empty():  # Om det finns fler tecken, kontrollera om det är ett rätt nummer
            read_number(queue)

        if queue.is_empty():
            return "Formeln är syntaktiskt korrekt"
        else:
            return "Ogiltigt tecken vid radslutet " + queue.rest()
    except Syntaxfel as error:
        return str(error)

def main():
    """Läser in flera rader från standard input och kontrollerar molekylsyntaxen"""
    import sys
    for line in sys.stdin:
        line = line.strip()
        if line == "#":
            break
        result = check_molecule(line)
        print(result)

if __name__ == "__main__":
    main()
