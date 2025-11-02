def create_chocolate_bar(rader, kolumner):
    matris = []

    for i in range(1, rader + 1):
        rad = []
        row_counter = 10 * i

        for k in range(1, kolumner + 1):
            värde = k + row_counter
            if värde == 11:
                värde = "P "
            rad.append(str(värde))

        matris.append(rad)

    return matris

def print_chocolate_bar(matris):
    for rad in matris:
        for c in rad:
            print(c, end=" ")
        print()


def chomp(matris, rad, kol):
    for i in range(rad - 1, len(matris)):
        del matris[i][kol - 1 :] 
    return matris


def spelarens_tur(aktuell_spelare):

    if aktuell_spelare ==1:
        return "Första spelaren", "Andra spelaren"
    elif aktuell_spelare == 2:
        return "Andra spelaren", "Första spelaren"
    else:
        print("Något gick fel!")
        return None, None


"""def check_winner(matris, andra_spelaren):
    # Kollar varje element i matrisen
    for rad in matris:
        for element in rad:
            if element != "P " and element != "":  # Om något element inte är P och inte tom
                return False  # Spelet fortsätter
    #Om loopen avslutas utan att returna false, bara "P" kvar

    print("{} vinner!".format(andra_spelaren))
    return True
"""
def check_winner(matris):
    if matris[0][1] =="" and matris[1][0]=="":
         return True
    else:
        return False



def meny_instruktioner():
    return """
Instruktioner: I spelet kommer du utmanas om att välja ett blocknummer från spelplanen. 
Det valda blocket och alla block under och till högre kommer att raderas. 
Spelet går ut på att undvika välja P, den spelare som väljer P förlorar och den andra spelaren vinner.
"""


def main():
    print(meny_instruktioner())

    rader = int(input("Hur många rader ska chokladbaren bestå av: "))
    kolumner = int(input("Hur många kolumner ska chokladbaren bestå av: "))
    matrix = create_chocolate_bar(rader, kolumner)
    aktuell_spelare = 1
    while True:
        spelarens_namn, andra_spelaren = spelarens_tur(aktuell_spelare)
        print_chocolate_bar(matrix)
        
        if check_winner(matrix):
            print("{} vinner!".format(andra_spelaren))
            break
        
        välj_blocknummer = input("{}s tur, välj ett blocknummer: ".format(spelarens_namn))
        try:
            rad = int(välj_blocknummer[0])
            kol = int(välj_blocknummer[1])

            if rad <= len(matrix) and kol <= len(matrix[0]) and len(välj_blocknummer) ==2:
                matrix = chomp(matrix, rad, kol)
            else:
                print("\n Välj ett lämpligt blocknummer! \n")
        except ValueError:
            print("\n Mata vänligen in en siffra! \n")

        
      
        aktuell_spelare = 3 - aktuell_spelare

main()

