from tkinter import *
def reaktion(knapp_text): #1 parameter
    print("knappen")

p=Tk()
p.geometry("100x100") #ger 100 pixel 
b= Button(p, text="click 1")#, command = lambda:x reaktion("click1")
b.pack()
b2 = Button(p, text="Knapp2")# command = lambda:x reaktion("click2")
b2.bind()


#bind skickar automatiskt info om evente till reaktion funktionen
#lambda är en annony funktion som struntar i informationen den anropar bara reaktion med parametern tex kan man säga x.y eller bar ax eller något annat

#Hur vet programmet vilken knapp som blivit tryckt?
""" vi dekalrerar knappen med command eller med bind. Man kan lägga till flera bind till ett command. Bind ger större möjlighet till att styra programmet beroend epå användaren
    """

""" .pack_forget döljer istället för att visa tillskillnad från .pack

"""
"""
När används frame?
Det är en rektangulär region i fönstret. används för att gruppera andra widgets
när vi assignar en fram tex:
b3=Button = (f, text = "4") här ser man att f är ägaren av b3
b3.pack()
"""

    """
    Layouten används för att placera 

    vi har 3 exempel:
    grid() = delar upp platser som en tabell
    pack()
    place() = man behver själv skriva kod för att anpassa tabell storlek vilket finns inbyggt i de andra. Kan finnas exempel där vissa celler ska behålla sin storlek i de andra kan man se tabellerna som tupler som egentligen inte ska ändras individuellt men med place kan man göra det.
    det är viktigt att endast använda en av dessa i ett program och inte blanda , det kan leda till e.v buggar
    """

    """Label:
    Det är en widget för att kunna 
    En rad text som förklarar vad ett textfält ska användas till
    """

""" Entry:
Input fält där användaren kan skriva 
"""

    """StringVar, IntVar, DoubleVar, BooleanVar:
tex 
from tkinter import*
def byt():
    n.set("Förlåt...")
    master=Tk()
    n= stringvar():
    n.set("skriv ditt namn")
    l = label(master,text=n)
    l.pack()
    b=Button(master,command=byt)
    """

"""Undvik att ha print och input i funktionerna för då kommer textbaserade stoppa grafiken. 
Gör det grafiska delen av programmet först

    """
    """
Exempelvis chomp labben
"""


"""CheckButton:
SOm att man kryssar av en checklista av knappar. De är som knappar i en to do list som när man klicka rpå de gör en checkmark


    """

"""On value och offvalue:
Vi kör ett program och kan anpassa parametrar i funktioner beroende på om det är onvalue eller offvalue.


    """

"""RadioButton:
Man kan endast välja 1 i detta fall tillskillnad från onvalue och offvalue. Check ska anropas på alla.

    """

    """self.get
    tror det är det värde som används för self
Om vi endast har en variabel för samma klickning kan det vara så att det sker buggar där de tinte skrivs ut som man vill. Vill du att de ska vara med i samma grupp ska de använda samma variabel. Då kommer man endast kunna välja en kanpp och det är varaibeln som specifierar grupptillhörighet.
"""