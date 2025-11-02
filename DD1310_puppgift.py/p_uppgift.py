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
        if self.pe_tal < 0:
            pe_tal_str = "negativt"
        else:
            pe_tal_str = str(self.pe_tal)

        return (
            f"""\n 
-------------Fundamental analys för {self.namn}-------------
Soliditet: {self.soliditet} %,
P/E-tal: {pe_tal_str}, 
P/S-tal: {self.ps_tal}"""
        )

#Parameter: Self
#Returnerar en strängrepresentation av den tekniska analysen     
          
    def teknisk_analys(self):
        return (
            f"""\n
-------------Teknisk analys för {self.namn}-------------    
Kursutveckling (30 senaste  dagarna): {self.kursutveckling} %
Betavärde:{self.betavärde}
Lägsta kurs (30 senaste dagarna): {self.lägsta_kurs} 
Högsta kurs (30 senaste dagarna): {self.högsta_kurs}"""
        )            


            
	
#bra metod för att kunna sortera
#Parameter: aktielista med aktieinstanser för att jämföra olika attribut och således kunna sortera dessa utifårn givna villkor
#Returnerar: True/False
    def __gt__(self):
        if self.betavärde > self.betavärde:
            return True
        else:
            return False


     #************ Huvudprogrammet ********************

#Läs in data från filerna och skapa aktieinstanser
#Låt användaren ange sitt val
#Låt användaren ange vilken aktie/ alternativt sortera och skriv ut
#Skriv ut analys för vald aktie
#repitera förlopp tills användaren väljer att avsluta



    
    
     #****************** Funktioner ****************************

#Läser in fundamenta filen och skapar aktieinstanser med fundamental information
#Funktionen öppnar varje fil, läser rad för rad och skapar eller uppdaterar aktieobjekt i aktielista
#Parameter: namnet på filen som ska läsas(fundamenta.txt,kurser.txt,omx.txt)
#returnerar: uppdaterar/skapar aktieinstanser som tilldelas data från respektive fil, ordnade enligt klassdefinitionen med [namn,soliditet,p/e-tal,p/s-tal,betavärde,kursutveckling, lägsta_kurs, högsta_kurs]

aktier_dict = {}

def las_fundamenta(filnamn1):
    with open(filnamn1,"r") as file:
        for line in file:
            namn,soliditet,pe_tal,ps_tal = line.strip().split(",")
            aktier_dict[namn] = Aktie(namn,float(soliditet),float(pe_tal),float(ps_tal))
            


    return aktier_dict





def las_kurser(filnamn2):
    #En tom dictionary som det ska finnas betavärden i
    #Referensvärden för första respektive sista kursen sätts till None
    avk_aktie_dict = {}
    lista_kurser = []
    aktie_lista = []
    forsta_kursen= None
    sista_kursen = None
    current_stock = None


    with open(filnamn2,"r") as file:
        for line in file:
            #Om if satsen stämmer uppdateras current_stock till den nya identifierade aktien och första_kursen återställs till None samt listan med inlästa kursen töms
            if line.strip().isalpha()==True:
                current_stock = line.strip()
                lista_kurser = []
                forsta_kursen=None
                sista_kursen = None
                continue
            if current_stock in aktier_dict:
                parts = line.strip().split()
                #För att kunna indentifiera och formatera delar av filen där vi plockar kurser och lägger till i en lista av alla kurser som vi läst in för en specifik aktieinstans
                if len(parts)==2:
                    datum,kurs = parts
                    kurs = float(kurs)
                    lista_kurser.append(kurs)
            #För att undvika indexError undersöker vi endast det första och sista kursen först när vi läst in minst 30 kurser
            #Vi kan indentifiera högsta respektive lägsta kurs under denna period
            #Vi har definerat aktie till att vara den aktuella aktien och attributen för denna aktie adderas
            #Samt kursutveckling med hjälp av den inlästa datan uttryck i procent enligt nedan
            if len(lista_kurser)>30:
                forsta_kursen = float(lista_kurser[-30])
                sista_kursen = float(lista_kurser[-1])
                if forsta_kursen and sista_kursen !=0:
                    aktie = aktier_dict[current_stock]
                    aktie.lägsta_kurs = min(lista_kurser[-30:])
                    aktie.högsta_kurs = max(lista_kurser[-30:])
                    aktie.kursutveckling = round(((sista_kursen - forsta_kursen) / forsta_kursen) * 100, 2)
                    avk_aktie_dict[current_stock] = round(sista_kursen/forsta_kursen,2)
               
             #Uppdaterar nuvarande aktie och återställer referensvärdet
    return avk_aktie_dict



def avk_marknad(filnamn3):
    forsta_index= None
    sista_index = None
    lista_index = []
    try:
        with open(filnamn3, "r") as file:
            for line in file:
                    parts = line.strip().split()
                    if len(parts)==2:
                        datum,index = parts
                        index = float(index)
                        lista_index.append(index)

                    if len(lista_index)>30:
                        forsta_index = float(lista_index[-30])
                        sista_index = float(lista_index[-1])
                    if forsta_index and sista_index !=0:
                        avk_marknad = round(sista_index/forsta_index,2)
    except FileNotFoundError:
        print("Filen hittades inte")
        
    return avk_marknad




def calc_betavärde():
    try:
        marknadens_avkastning = avk_marknad("C:\\Users\\nick0\\.vscode\\puppgift.py\\omx.txt")  # Hämta marknadens avkastning
        avk_aktie_dict = las_kurser("C:\\Users\\nick0\\.vscode\\puppgift.py\\kurser.txt")  # Hämta avkastning för varje aktie

        for aktie_namn, aktie_obj in aktier_dict.items():
            if aktie_namn in avk_aktie_dict:
                aktie_avkastning = avk_aktie_dict[aktie_namn]
                if marknadens_avkastning != 0:
                    aktie_obj.betavärde = round(aktie_avkastning / marknadens_avkastning,2)
                else:
                    aktie_obj.betavärde = 0  # För att undvika division med noll
    except FileNotFoundError:
        print("En eller fler av filerna hittades inte")

    return None








#Sorterar aktieinstansernas betavärde i en aktielista med deras betavärden
#använder sig av sorterings metoder definerade i klassen Aktier
#parameter: En lista med aktieinstanserna och deras betavärden
#returnerar betavärdet och aktierna från högsta till lägsta betavärde

def sortera_beta(aktier_dict):
    # Skapa en lista med aktieobjekt och deras betavärden
    beta_lista = [(namn, aktie.betavärde) for namn, aktie in aktier_dict.items()]

    # Sortera listan baserat på betavärde i fallande ordning dvs(reverse=True)
    beta_lista.sort(key=lambda x: x[1], reverse=True)

    # Returnera den sorterade listan
    return beta_lista




#En funktion som frågar användaren vad den vill göra, och ser till att endast acceptera siffororna 1-4 som svar och frågar igen ifall något annat inmatas
#Returerar en siffra 1-4 (användarens input)(int)
#Ingen parameter
def vald_handling():
    x= None
    while x!=4:

        try:
            val = input("Vilket alternativ vill du välja?")
            x= int(val)
            if x < 4 and x>=1: 
                return x
            
            elif x==4:
                print("Avslutar")
                break

            else:
                print("Ange ett tal mellan 1 och 4")
            
        except ValueError:
            print("Skriv vänligen in en siffra")
    return x


def alternativ():
    text= "\n" """En {} analys kan utföras för följande aktier: 
1.Ericsson 
2.Electrolux
3.AstraZeneca"""
    return text


#En funktion för att visa olika analystyper beroende på användarens inmatning
#Parameter: Analystyp(str), aktienamn_list(str) vilket är en lista med de inlästa och skapade aktieobjektens namn
#returnerar: None 
def visa_analys(analystyp, aktienamn_lista):
    print(alternativ().format(analystyp))
    val2 = vald_handling()

    if 1 <= val2 <= len(aktienamn_lista):
        vald_aktie = aktienamn_lista[val2 - 1]
        if analystyp == "fundamental":
            print(aktier_dict[vald_aktie].fundamental_analys())
        elif analystyp == "teknisk":
            print(aktier_dict[vald_aktie].teknisk_analys())


def visa_sorterade_beta():
    calc_betavärde() #Huvudsyftet av denna funktion är att uppdatera betavärdena. Här uppdateras  de när jag anropar, precis innan de sorteras
    betavärden = sortera_beta(aktier_dict)  
    text = "-------------Rangordning av aktier med avseende på betavärde-------------"
    i=1
    for namn, betavärde in betavärden:
        text += "\n"
        text += f"{i}: {namn}: {betavärde}"
        i+=1
        
    return text


#En meny display som visas till användaren i början
#Parametrar: Inga
#returnerar: strängrepresentation av menyn

def meny_display():
	return """
    ------------------------Meny--------------------------  
1.Fundamental analys (Vid långsiktigt aktieinnehav
2.Teknisk analys (Vid kort aktieinnehav)
3.Rangordning av aktier med avseende på dess betavärde
4.Avsluta""" 



#Huvudprogrammet till koden
#anropar funktionerna
#parametrar: inga
def meny():
    las_fundamenta("C:\\Users\\nick0\\.vscode\\puppgift.py\\fundamenta.txt") #Uppdaterar och initialiserar aktieobjekten
    fortsätt_köra = True
    val2= 0 #Sätter default värdet för val2, då val1 behöver ske först

    while fortsätt_köra==True:
        val1=val2
        if val2 not in [1,2,3]: #Vi skriver ut menyn endast vid första gången då val2 har sitt default värde
            print(meny_display())
            val1 = vald_handling()
        
        aktienamn_lista = list(aktier_dict.keys()) #Skapar en lista med aktienamnen som finns inlästa i aktier_dict
        
        if val1 == 1:
            visa_analys("fundamental", aktienamn_lista)
            
        elif val1 == 2: 
            calc_betavärde()
            visa_analys("teknisk", aktienamn_lista)
            
        elif val1==3:
            print(visa_sorterade_beta())
        
        elif val1 ==4:
            break
            

        val2= vald_handling()
        if val2 == 4:
            break
            

meny()



            
        
	
