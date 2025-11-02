
"""
def calc_betavärde(avk_aktie,avk_marknad):
    for aktie_namn, betavärde in betavärde_dict.items():
        if aktie_namn in aktier_dict:
            aktier_dict[aktie_namn].betavärde = avk_aktie / avk_marknad
    return None
"""
"""
def las_kurser(filnamn2):
    with open(filnamn2, "r") as file:
        for line in file:
            datum, kurs = line.strip().split(",")
            # Example logic to determine which Aktier instance to update
            aktie_namn = "Some way to determine the stock name from the line"
            kurs = float(kurs)

            if aktie_namn in aktier_dict:
                aktie = aktier_dict[aktie_namn]
                
                # Here we update the attributes that were initially set to zero
                if aktie.lägsta_kurs == 0 or kurs < aktie.lägsta_kurs:
                    aktie.lägsta_kurs = kurs
                if aktie.högsta_kurs == 0 or kurs > aktie.högsta_kurs:
                    aktie.högsta_kurs = kurs
"""
"""def las_kurser(filnamn2):
    # Skapar en lista av aktienamn i samma ordning som de förekommer i aktier_dict, samt en default värde för current_stock = None
    stock_names = list(aktier_dict.keys())
    current_stock = None
    lista_kurser = []
    with open(filnamn2, "r") as file:
        for line in file:

            if line.strip().isalpha():
                current_stock = line.strip()
                continue
                #Obs att sista villkoret nedan gör att vi inte anropar .max eller .min tills att vi har en lista med de 30 senaste kurserna

                 # Återställ kurslistan för ny aktie
            if current_stock in aktier_dict:
                parts = line.strip().split()
                if len(parts) == 2:
                    _ , kurs = parts #Obs vi är inte intresserade av datum så vi sätter "_" där för att underlätta
                    kurs = float(kurs)
                    lista_kurser.append(kurs)
                if current_stock in aktier_dict:
                    aktie = aktier_dict[current_stock]
                    aktie.lägsta_kurs = min(lista_kurser[-30:])
                    aktie.högsta_kurs = max(lista_kurser[-30:])
                    current_stock = line.strip()
                    lista_kurser = [] 
                     # Behåll endast de 30 senaste

            if current_stock in aktier_dict and len(lista_kurser) > 0:
                aktie = aktier_dict[current_stock]
                aktie.lägsta_kurs = min(lista_kurser[-30:])
                aktie.högsta_kurs = max(lista_kurser[-30:])

            """"""if current_stock in aktier_dict:
                parts = line.strip().split()
                if len(parts)==2:
                    datum,kurs = parts
                    kurs = float(kurs)
                    aktie = aktier_dict[current_stock]
                # Uppdaterar/hittar attribut av aktieobjekten
                    aktie.lägsta_kurs = min(aktie.lägsta_kurs or kurs, kurs)
                    aktie.högsta_kurs = max(aktie.högsta_kurs or kurs, kurs)"""
""""""
 #return aktier_dict

#las_kurser("C:\\Users\\nick0\\.vscode\\puppgift.py\\kurser.txt")

#Testa och kolla om avkastning för samtliga aktier räknas korrekt: 
#print(avk_aktie("C:\\Users\\nick0\\.vscode\\puppgift.py\\kurser.txt"))
#for namn, aktie_obj in aktier_dict.items():
    #print(f"{namn}: {aktie_obj}")
"""
def las_kurser(filnamn2):
    with open(filnamn2,"r") as file:
        for line in file:
            datum,index = line.strip().split(",")

   """
"""
    """"""betavärde_dict = calc_betavalue(filnamn2)
    for aktie_namn, betavärde in betavärde_dict.items():
        if aktie_namn in aktier_dict:
            aktier_dict[aktie_namn].betavärde = betavärde""""""
#("C:\\Users\\nick0\\.vscode\\puppgift.py\\kurser.txt")


"""

def hitta_aktie(x):
    pass

#Utför en teknisk analys på den valda aktien
#Parameter: aktielistan med aktieinstanserna samt den valda aktieobjektet
#returnerar en teknisk analys i form av den valda aktie instansens tekniska information

def teknisk_analys(aktielista,vald_aktie):
	pass

#Skriver ut en fundamental analys i form av den valda aktieinstansens fundamentala information
#Parameter: En aktielista med fundamental information om den valda aktieinstansen
#Returerar en strängrepresentation med fundamental information

def fundamental_analys(aktielista):
	pass

#En funktion som beräknar betavärdet av aktierna
#Parameter: En aktielista med samtliga aktieinstanser
#returnerar en lista med samtliga aktieinstanser och deras betavärde 
def räkna_betavärde(aktielista):
	pass

#print(alternativ().format("fundamental"))
            #val2 = vald_handling()
"""if 1 <= val2 <= len(aktienamn_lista):
                vald_aktie = aktienamn_lista[val2 - 1] #Aktie objektet lokaliseras utifrån index i listan och vald_aktie tilldelas detta värde
                print(aktier_dict[vald_aktie].fundamental_analys())"""
        
#print(alternativ().format("teknisk"))
"""val2 = vald_handling()
            if 1 <=val2 <= len(aktienamn_lista):
                vald_aktie = aktienamn_lista[val2 - 1]
                print(aktier_dict[vald_aktie].teknisk_analys())"""
                   