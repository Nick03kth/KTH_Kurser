from TV import TV
alla_tv=[]
def read_file(filnamn):
    try:
        fil = open(filnamn,"r")
        alla_tv=[]
        tv_name = fil.readline()
        while tv_name !="":
            max_channel=int(fil.readline())
            current_channel = int(fil.readline().strip())
            max_volume = int( fil.readline().strip())
            current_volume = int(fil.readline().strip())
            alla_tv.append([tv_name,max_channel,current_channel,max_volume,current_volume])
            tv_name = fil.readline().strip()
        fil.close()
    except (FileNotFoundError):
        print("Filen hittades inte eller ogiltig inmatning")
        alla_tv=[]
    
    return alla_tv
tvlista = read_file("allatv.txt")


"""tv_names = []
for i in alla_tv:
    tv_names.append(alla_tv[i])

print(tv_names)
returnerar "alla_tv", en lista med information om varje tv objekt 
"""

def write_file(alla_tv,filnamn):
    tvfil =open(filnamn, "w")
    for rad in alla_tv:
        tvfil.write(rad.tv_name + "\n")
        tvfil.write(str(rad.max_channel) + "\n")
        tvfil.write(str(rad.current_channel) + "\n")
        tvfil.write(str(rad.max_volume) + "\n")
        tvfil.write(str(rad.current_volume) + "\n")
    
    tvfil.close() 
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
    return new_channel

def increase_volume(tv_objekt):
    try:
        if tv_objekt.increase_volume == True:
            current_volume +=1
        else:
            print("Det går inte att öka volymen")
    except ValueError:
        print("Felaktig inmatnig!")

def decrease_volume(tv_objekt):
    try:
        if tv_objekt.decrese_volume==True:
            current_volume=-1
        else:
            print("Det går inte att sänka volymen!")
    except ValueError:
        print("Felaktig inmatning")

def adjust_TV_menu():
    print(
""" 

1.byt kanal
2.höj volym
3.sänk volym
4.återgå till huvudmenyn.""")
    choice = int(input("Välj:"))
    return choice





def select_TV_menu(tv_names):
    for i in range(0,len(tv_names)):
        print(i+1,".",tv_names[i])
    choice = int(input("Välj:"))
    
    if choice==4:
        chosen = None
    elif choice ==1:
        chosen = tv_names[0] 
    elif choice ==2:
        chosen = tv_names[1]
    elif choice == 3:
        chosen = tv_names[2]
    else:
        print("Felaktig inmatning, var vänlig försök igen")
    
    return chosen 
    
def main():
    print("Välkommen till TV simulatorn ")
    tv_obj_list = read_file(filnamn)
    while choice !=4:
       selected_tv= select_TV_menu(tv_names)
       if selected_tv ==None:
        break
       else:
        adjust_TV_menu()
        if choice == 1:
            change_channel(tv_objekt)
        elif choice ==2:
            increase_volume(tv_objekt)
        elif choice==3:
            decrease_volume(tv_objekt)
        else:
            break
        write_file(alla_tv,filnamn)




       

