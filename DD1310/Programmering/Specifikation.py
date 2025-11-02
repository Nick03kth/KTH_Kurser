# Spec av P-uppgift

# Namn: Nick Heidarian
# Personnummer: 2003-04-08-9295
# P-uppgift nr: 187
# Titel: Aktieköp

"""
Inledande tankar:

Till att börja med behöver vi hantera data i tre filer, därför anser jag det relevant att skapa en klass som kan hantera filerna och dess information samt ordna de på ett användbart sätt. 

Vi vill dela upp koden i funktioner för att undvika kodupprepning. Vi vill använda klasser och metoder för representationen och sorteringen av datan. Med hjälp av detta kan vi således använda funktioner för att utföra operationer med väldisponerad data nära till hands. 

Vi vill ta häsyn till eventuella fel som kan uppstå och implementera try/except satser i vår felhantering så att små fel fångas upp tidigt. Exempelvis i algoritmen som använder olika formler och funktioner för att undersöka olika mätvärden där det kan uppstå eventuella Valueerrors. Dessa vill vi plocka upp direkt i sjäva funktionen med hjälp av ovanstående felhantering. Annars kommer det bli svårt att felsöka programmet i efterhand.

Slutligen vill vi skapa ett huvudprogramm som anropar dessa funktioner och som fortsätter tills att användaren väljer att avsluta.

Vi kommer behöva huvudsakligen 3 filer:
“Kurser.txt” 
“Fundamenta.txt”
“Omx.txt”

Vi kommer skapa metoder som läser dessa filer och ordnar informationen för att tilldela det till respektive klassinstans.

Vi skapar en dictionry med varje aktienamn som key och deras attrbut blir deras values. Från inläsningen av fundamenta.txt skapar vi denna dictionary som vi successivt fyller på i och emd att vi läst in tekniks eller räknat ut betavärdet för respektive aktie.
Under tiden kommer varje aktie ha default värden, vilket har assignerats i klassen som "=0".



# *************** Användargränssnitt **************************

# Vid körning ska programmet se ut som nedan:
#Användarens inmatning är markerad med rött och datorns utmatning i svart.
Meny:
1.Fundamental analys (Vid långsiktigt aktieinnehav) 
2.Teknisk analys (Vid kort aktieinnehav) 
3.Rangordning av aktier med avseende p˚a dess betav¨arde 
4.Avsluta 
Vilket alternativ vill du välja? : 1
En fundamental analys kan utf¨oras för följande aktier: 
1.Ericsson 
2.Electrolux 
3.AstraZeneca 
Vilken aktie vill du g¨ora fundamental analys på?: 1 
—————Fundamental analys för Ericsson————– 
företaget soliditet ¨ar 36 % 
företagets p/e-tal ¨ar negativt 
företagets p/s- tal ¨ar 0.23 
Vilket alternativ vill du välja? 2 
En teknisk analys kan utf¨oras f¨or f¨oljande aktier: 
1.Ericsson osv... 



# ******************** Minne / Datastruktur ************************
Varje aktie representeras med en aktieinstans som har namn(String),soliditet(float),p/e-tal(float),p/s-tal(float),betavärde(float),lägsta kurs ,senaste 30 dagarna,(float)och högsta kurs,senaste 30 dagarna,(float).

Varje klassinstans lagras i en lista. 

Klassattributen som varje klassinstans tilldelas med hämtas från filerna: fundamenta.txt, Omx.txt, Kurser.txt.






# ************************ Algoritm *******************************

Programmet läser in information om en aktie från filen
Aktieobjekt skapas och läggs till i en lista
Detta upprepas tills alla filer är inlästa och informationen tilldelad till respektive aktieobjekt
Ber användaren välja vad den vill göra
Ber användaren välja aktie
Relevanta funktioner anropas och skriver ut det valda aktieobjektets attribut utifrån önskad information
Alternativt skriver ut aktieobjekten och dess betavärde i ordning från högsta till lägsta betavärde.
Ber användaren välja vad den vill göra 
Avslutar programmet om användaren matar in 4
… osv






# *********************** Programskelett ***************************


     #****************** Funktioner ****************************
"""


#Läser in fundamenta filen och skapar aktieinstanser med fundamental information
#Funktionen öppnar  fil, läser rad för rad och skapar eller uppdaterar aktieobjekt i aktiedictionary
#Parameter: fundamenta.txt
#returnerar: uppdaterar/skapar aktieinstanser som tilldelas data från respektive fil, ordnade enligt klassdefinitionen med [namn,soliditet,p/e-tal,p/s-tal,betavärde,kursutveckling, lägsta_kurs, högsta_kurs] i en dictionary
# =>aktier_dict

aktier_dict = {}

def las_fundamenta(filnamn1):
	pass

#Öppnar filen kurser.txt och läser in kurser från respective aktie
#Om aktien finns med i aktiedictionaryn kommer värdet tilldelas till respektive aktie med teknisk information. Här hämtas info om högsta/lägsta kurs, kursutveckling, och vi räknar även ut avkastningen för aktien.
#Returnerar avkastningen för respektive aktie i dictionarin: avk_aktie_dict vilket är det enda som behövs för vidare uträkning av betavärdet. Resterande inläst data uppdateras och används direkt genom att adderas som attribut.
def las_kurser(filnamn2):
    
	pass

 #Marknadens avkastning har ett värde, så räcker att bara räkna en gång och uppdatera. 
#Avk för aktierna behövde organiseras(anledningen till dictionary) pga vi hanterar flera olika värden
#Här räknas avkastningen för k´marknaden för att kunna sedan räkna betavärdet
#Returnerar: avk_marknad (float)
def avk_marknad(filnamn3):
	pass

#Räknar ut betavärdet med hjälp av avk_marknad och respektive avkastning för aktierna i avk_aktie_dict
#Betavärdet för varje aktie adderas som attribut i deras klassinstans. 
#Returnerar: None
def calc_betavärde():
	pass




#Skapar en tupel av betavärden med respektive aktie ur aktier_dict
#Parameter: aktier_dict
#Returnerar: Betalista vilket är en lista med sorterade aktiernas betavärden

def sortera_beta(aktier_dict):
	pass


#En funktion som frågar användaren vad den vill göra, och ser till att endast acceptera siffororna 1-4 som svar och frågar igen ifall något annat inmatas
#Returerar en siffra 1-4 (användarens input)(int)
#Ingen parameter
def vald_handling():
	pass

#En funktion som skriver ut alternativ texten
#Returnerar: Alternativ text
def alternativ():
	pass


#En funktion för att visa olika analystyper beroende på användarens inmatning
#Parameter: Analystyp(str), aktienamn_list(str) vilket är en lista med de inlästa och skapade aktieobjektens namn
#returnerar: None 
def visa_analys(analystyp, aktienamn_lista):
	pass


#En funktion som visar de sorterade betavärdena på ett snyggt sätt

def visa_sorterade_beta():
	pass


#En meny display som visas till användaren i början
#Parametrar: Inga
#returnerar: strängrepresentation av menyn

def meny_display():
	pass


#Huvudprogrammet till koden
#anropar funktionerna
#parametrar: inga
def meny():
	pass
    #*************** Klasser och dess metoder******************

#klassen har klassnamnet Aktier
#Attribut: namn, soliditet, p/e-tal, p/s-tal, betavärde, lägsta_kurs, högsta_kurs
#Observera default värde på betavärde,kursutveckling,lägsta/högsta kurs, undviker problem när vi läser in data från fil som inte innehåller detta
class Aktie:
    def __init__(self,namn,soliditet,pe_tal,ps_tal,betavärde=0,kursutveckling=0, lägsta_kurs=0, högsta_kurs=0):
        self.namn = namn
        self.soliditet = soliditet
        self.pe_tal = pe_tal
        self.ps_tal = ps_tal
        self.betavärde = betavärde
        self.kursutveckling = kursutveckling
        self.lägsta_kurs = lägsta_kurs
        self.högsta_kurs = högsta_kurs
        
   
#Parameter: self
#Returnerar strängrepresentation av den fundamentala analysen

def fundamental_analys(self):
	pass   

#Parameter: Self
#Returnerar en strängrepresentation av den tekniska analysen     
          
def teknisk_analys(self):
	pass      


            
	
#bra metod för att kunna sortera
#Parameter: aktielista med aktieinstanser för att jämföra olika attribut och således kunna sortera dessa utifårn givna villkor
#Returnerar: True/False
def __gt__(self,other):
	pass
     #************ Huvudprogrammet ********************

#Läs in data från filerna och skapa aktieinstanser
#Låt användaren ange sitt val
#Låt användaren ange vilken aktie/ alternativt sortera och skriv ut
#Skriv ut analys för vald aktie
#repitera förlopp tills användaren väljer att avsluta

