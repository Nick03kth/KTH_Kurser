def create_chocolate_bar(rader,kolumner):
    matris = []


    for i in range(1,rader+1):
        rad=[]
        row_counter = 10*i

        for k in range(1,kolumner+1):
            värde= k+row_counter
            if värde == 11:
                värde = "P "
            rad.append(str(värde))

        matris.append(rad)
        
    return matris


def print_chocolate_bar(matris):
    for row in matris:
        for c in row:
            print(c, end=" ")
        print()
    return ""

def chomp(matris,rad,kol):
    for i in range(int(rad) - 1,len(matris)):
        matris[i][int(kol)-1:] = " "
    return matris

def check_winner(matris):
    if matris[1][0]==" " and matris[0][1]==" ":
        print("{} VINNER!".format(spelarens_namn))
        return True
    else: 
        return False

def ask_cell_number(matris, rad,kol):
    try:
        rad = int(välj_blocknummer[0])
        kol = int(välj_blocknummer[1])
        
        if rad>=0 and rad<=rader and kol>=0 and kol<=kolumner:
            matris = chomp(matris,rad,kol)
            print_chocolate_bar(matris)
        else:
            print("Ogiltig inmatning, välj ett nummer inom spelplanen")
    except ValueError:
            print("Ogiltig inmatning, försök igen")
    return rad, kol




#HUVUDPROGRAM:

print("Instruktioner:\nI spelet kommer du utmanas om att välja ett blocknummer från spelplanen. Det valda blocket och alla block under och till höger kommer att raderas. Spelet går ut på att undvika välja P, den spelare som väljer P förlorar och den andra spelaren vinner.")
rader = int(input("Hur många rader ska chokladbaren bestå av: "))
kolumner = int(input("Hur många kolumner ska chokladbaren bestå av: "))


spelarens_tur = 1
spelarens_namn= "Första spelaren"
matris = create_chocolate_bar(rader,kolumner)
while check_winner(matris)== False:
    print(print_chocolate_bar(matris))
    if spelarens_tur==1:
        spelarens_namn= "Första spelaren"
        
        
    if spelarens_tur ==2:
        spelarens_namn = "Andra spelaren"

    välj_blocknummer = input("{}s tur, välj ett blocknummer: ".format(spelarens_namn))
    rad = välj_blocknummer[0]
    kol = välj_blocknummer[1]
    
        
        
    matris = chomp(matris,rad,kol)
    
    spelarens_tur = 3 - spelarens_tur
   

    
    
#För att hamna mellan 1 och 2 kan vi ta 3 - antingen 1 eller 2. 3-2=1 och 3-1=2 så det koommer alltid växla
    
    
    

