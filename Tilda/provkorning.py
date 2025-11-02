def utskrift(lista):
    if len(lista) > 0:
        utskrift(lista[1:])
        print(lista[0])


utskrift([1,2,3,4,5])