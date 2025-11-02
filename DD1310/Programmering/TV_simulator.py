from TV import TV
alla_tv=[]
def read_file(filnamn):
    #try:
    alla_tv=[]
    with open(filnamn,"r") as fil:
        for rad in fil:
            tv_info = rad.strip().split(",")
            tv= TV(tv_info[0],int(tv_info[1]),int(tv_info[2]),int(tv_info[3]),int(tv_info[4]))
            alla_tv.append(tv)
    return alla_tv
#tv_lista = read_file("C:\\Users\\nick0\\.vscode\\Labb5.py\\Programmering\\allatv.txt")


 

def write_file(alla_tv,filnamn):
    with open(filnamn, "w") as skriv:
        for tv in alla_tv:
            skriv.write(str(tv.str_for_file())+ "\n")

        
      
#Här returnerar vi inget, skriver endast i filen "filnamn"



def change_channel(tv_objekt):
    try:
        new_channel = int(input("Vilken kanal vill du byta till?"))
        if tv_objekt.change_channel(new_channel) == True:
            tv_objekt.current_channel = new_channel
        else:
            print("Det går inte att byta kanal")
    except ValueError:
        print("felaktig inmatning")

    

def increase_volume(tv_objekt):
    tv_objekt.increase_volume() 
    

def decrease_volume(tv_objekt):
    tv_objekt.decrease_volume()
           
def adjust_TV_menu():
    while True:
        try:
            choice = int(input(""" 
            TV Meny:                  
            1. byt kanal
            2. höj volym
            3. sänk volym
            4. återgå till huvudmenyn.
            Välj en av funktionerna:"""))
            if choice in [1,2,3,4]:
                return choice
            else:
                continue
        
        except ValueError:
            print("Vänligen ange en siffra")
        
       




def select_TV_menu(alla_tv):
    while True:
        print("""*** Välkommen till Tv-simulator***""")
        i = 1
        for tv in alla_tv:
            print("{}.{}".format(i, tv.tv_name))
            i += 1
        print("{}.Avsluta".format(i))
        try:
            val = int(input("Välj en av tv-apparaterna eller avsluta:"))
            if val == 3:
                print("Avslutar")
                return None
            elif val not in [1, 2, 3]:
                print("Skriv vänligen en siffra mellan 1 och 3")
            else:
                return alla_tv[val - 1]
        except ValueError:
            print("Felaktig inmatning, var vänlig försök igen")

 

def main():
    alla_tv = read_file("C:\\Users\\nick0\\.vscode\\Labb5.py\\Programmering\\allatv.txt")
    
    while True:
        try:
            selected_tv = select_TV_menu(alla_tv)
            if selected_tv == None:
                
                break

            else:
                justering = int(adjust_TV_menu())
            
            if justering == 1:
                change_channel(selected_tv)
            elif justering == 2:
                increase_volume(selected_tv)
            elif justering == 3:
                decrease_volume(selected_tv)
            elif justering == 4:
                continue #Select menyn kommer att printas ut i nästa varv enligt användarens val
            else:
                print("Välj ett befintligt alternativ")
        except ValueError:
            print("Fel typ av inmatning, vänligen ange ett giltigt val")
        write_file(alla_tv, "C:\\Users\\nick0\\.vscode\\Labb5.py\\Programmering\\allatv.txt")

print(main())