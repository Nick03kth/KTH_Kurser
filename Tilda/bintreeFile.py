class Node:
    def __init__(self,value):
        self.value = value
        self.left = None
        self.right = None



class Bintree():
    def __init__(self):
        self.root = None #Roten pekar först mot None

    def put(self,newvalue):
        # Sorterar in newvalue i trädet
        self.root = self.putta(self.root,newvalue) 

    def __contains__(self,value):
        # True om value finns i trädet, False annars
        return self.finns(self.root,value)

    def write(self):
        # Skriver ut trädet i inorder
        self. skriv(self.root)
        print("\n")
    
    def putta(self,p, newvalue):
     # Funktion som gör själva jobbet att stoppa in en ny nod
        if p is None:
            return Node(newvalue) #Vi har en tom plats och kan skapa ny nod här
       
        elif newvalue < p.value: #Om sant går vi åt vänster, vi kallar funktionen rekursivt fast traverserar vänster för att leta vidare
            p.left = self.putta(p.left, newvalue) #Tilldelar den nya noden som ett barn till noden p
        else:
            p.right = self.putta(p.right, newvalue) #På samma sätt tilldelar nya noden som ett barn till noden p
        return p 

        
    def finns(self, p,value): #--> True/False
     # Funktion som gör själva jobbet att söka efter ett värde
        if p is None:
            return False  #Om p som refererar till aktuell nod är None vet vi att sönerna till p är None.-> hittaades ej --> return False
        if value == p.value:
            return True # Värdet är hittat!
        elif value < p.value:
            return self.finns(p.left, value) #Rekursivt anrop för att traversera vänster
        else:
            return self.finns(p.right, value) #Rekursivt anrop för att traversera höger
        

    def skriv(self,p):
     # Funktion som gör själva jobbet att skriva ut trädet
        if p != None:
            self.skriv(p.left) #travesera vänster
            print(p.value)#Skriver ut värdet på aktuell nod
            self.skriv(p.right)#Travesera höger så att vi också besöker den högra subträdet också!
   
    #Hjälpmetoder för uppgift 3. Då det inte går att iterera genom sökträd och för att kunna skriva ut de behöver vi traversera genom de olika grenarna. 
    def get_words(self):
        # Denna metod ska hjälpa oss returnera alla ord i en lista
        words = []
        self._inorder(self.root, words) 
        return words
    #OBS! Tillskillnad från skriv funktionen returnerar denna en lista i stigande ordning, något som är viktigt för vår get_words metod för att faktiskt kunna sedan returnera alla ord i vårt binära träd! Skriv fokuserar på att printa orden och itne konvertera de till något vi kan använda och tillämpbart för uppgift 3. 
    def _inorder(self, p, words):
        if p is not None:
            self._inorder(p.left, words) #Vi kallar funktione rekrusivt och traverserar vänster
            words.append(p.value) #Efter att vi kallat funktionen rekrusivt och gått ända till löven går vi tillbaka till föräldern och skriver ut den också
            self._inorder(p.right, words) #Därefter skriver vi ut högra benet av p och går därefter vidare! Processen fortsätter så för hela trädet.

    

#if ordet in engelska:
#Algoritm för lösa uppgift 3.
#Steg 1. Skapa ett trädobjekt för engelska orden och lägg till grenar för filen engelska.txt
#Steg 2 skapa ett svenska trädobjekt
#Steg 3 Jämför med svenska trädobjektet , om engelska ordet är nytt och finns i svenska skriver vi ut det. 
