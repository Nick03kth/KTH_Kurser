from bintreeFile import Bintree
#Uppgift 3

svenska = Bintree() #Steg 1 och 2 i algoritmen är att skapa två trädobjekt, 1 för svenska ord och ett för engelska


with open("C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\word3.txt", "r", encoding="utf-8") as svenskfil:
    for rad in svenskfil:
        ordet = rad.strip()  # Ett ord per rad
        if ordet in svenska:
            continue #Vi behöver inte skriva in svenska ord som redan finns 
        else:
            svenska.put(ordet)  # Lägg till nya ord i trädet

print("\n")

engelska = Bintree() #Steg 1 och 2 i algoritmen är att skapa två trädobjekt, 1 för svenska ord och ett för engelska

with open("C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\engelska.txt", "r", encoding="utf-8") as engelskfil:
    for rad in engelskfil:
        ord = rad.strip().split()  # Split varje rad till separata ord
        for ordet in ord:
            if ordet in engelska:
                continue #Endast nya ord läggs till i engelska
            else:
                engelska.put(ordet)  # Lägg till nya ord i trädet



#Vi har redan 2 hjälp metoder som tillsammans hjälper oss gå genom våra träd och skriva ut ord _inorder och en som hjälper oss få fram ett ord inuti trädet. .get_words()
#Vi utnyttjar dessa inom en jämförande funktion vi kallar jamforelse(trädobjekt1, trädobjekt2)

def jamforelse(tradobj1,tradobj2):
    engelska_ord = tradobj1.get_words()
    
    for ord in engelska_ord:

        if ord in tradobj2:
            print(ord, end=" ")

jamforelse(engelska, svenska)



#engelska_ord = engelska.get_words()
#print("English words in the tree:", engelska_ord)  # Debugging: Verify words in the English tree

""" Uppgift 2
from bintreeFile import Bintree

svenska = Bintree()

with open("C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\word3.txt", "r", encoding="utf-8") as svenskfil:
    for rad in svenskfil:
        ordet = rad.strip()  # Ett ord per rad
        if ordet in svenska:
            print(ordet, end=" ")  # Skriv ut dubbletter
        else:
            svenska.put(ordet)  # Lägg till nya ord i trädet

print("\n")

"""