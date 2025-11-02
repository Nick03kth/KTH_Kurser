#Uppgift 1
"""
körsträcka = input("Ange körsträcka i km:  ")
förbrukad_bränsle = input("Ange förbrukat bränsle i liter: ")
bf = (100 * float(förbrukad_bränsle))/float(körsträcka)
print("Bränsle förbrukningen för bilen är ", round(bf,3), " l/100 km.")
"""

#uppgift 2
"""

vikt = float(input("Hur mycket väger paketet: "))
price_rate = 0
if vikt<2:
    price_rate = 30
elif 2<=vikt and vikt <6:
    price_rate = 28
elif 6 <= vikt and vikt < 12:
    price_rate = 25
else:
    price_rate = 23
    
pris = float(vikt) * round(float(price_rate),1)
print("Det kommer att kosta:", pris, "Kr")
"""
"""

#Uppgift 3:
"""
number_of_packages = int(input("Hur många paket vill du skicka? "))
total = 0
i=1
while i<= number_of_packages:
    
    weight = float(input("Ange vikt för paket {}:".format(i)))
    if (weight)<2:
        price_rate = 30
    elif 2<=(weight) and weight <6:
        price_rate = 28
    elif 6 <= (weight) and (weight) < 12:
        price_rate = 25
    else:
        price_rate = 23
    price = price_rate * float(weight)
    total += (price)
    i+=1


print("Det kommer att kosta", round(total,2),"kr")
                                   

