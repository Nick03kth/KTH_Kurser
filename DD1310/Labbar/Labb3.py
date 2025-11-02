#Upg 1
"""
print("Tabell:")
print("C", "F")
for i in range(20):
    F=(i*9+160)/5
    print(i,F)

#Upg 2
"""
"""
antal_rader = int(input("Ange antal rader:"))
antal_kolumner = int(input("Ange antal kolumner:"))

rader= 1
kolumner = 1
#Kod för kolumn rubrik
print("  ", end = "")
while kolumner<=antal_kolumner:
    print("{0:<3d}".format(kolumner), end = "")
    kolumner+=1
print()

#kod för multiplikationstbell
kolumner=1
while rader<=antal_rader:
    kolumner=1
    print("{0:<2d}".format(rader), end ="")
    
    while kolumner<=antal_kolumner:
        result = rader*kolumner
        print("{0:<3d}".format(result), end = "")
        kolumner+=1
    print() #hoppa till nästa rad
    rader+=1
"""


#upg 3
import random
antal_tärningar = int(input("Hur många tärningar behövs i spelet? "))
antal_kast = int(input("Hur många kast en spelare får?"))

while True:
    resultat = []
    starta = input("Genom att trycka på enter kan du börja kasta, om du vill avsluta spelet skriv A:")
    counter = 0
    if starta == "A" or starta=="a":
        print("Tack och hej!")
        break
        
    for i in range(antal_kast):
        resultat = []
        for j in range(antal_tärningar):
            tärning_utfall = random.randint(1,6)
            print("Tärning {}:".format(i+1),tärning_utfall)
            resultat.append(tärning_utfall)
        counter +=1
        if antal_kast>1 and counter<antal_kast :
            svar = input("Är du inte nöjd kan du kasta igen, vill du kasta igen?(j/n)")
            if svar == "n":
                print("Tack och hej!")
                break
    print("Du fick:", resultat,".")

        
  
        

       


        
        
    