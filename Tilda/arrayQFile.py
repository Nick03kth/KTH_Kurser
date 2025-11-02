from array import array

class IntQueue:
    def __init__(self):
        # Skapa en privat array för att lagra heltal
        self._elements = array('i')

    def add(self, item):
        # Lägg till ett element längst bak i kön
        self._elements.append(item)

    def remove(self):
        # Ta bort och returnera det första elementet i kön
        if not self.is_empty():
            return self._elements.pop(0) #OBS Tar bort och returnerar första värdet vilket gör att alla element flyttar ett steg. Som dequeueu, och är långsammare än länkad liste då endast pekare ebhöver flyttas vid borttag av element.
        else:
            raise IndexError("Kön är tom")
#B remove har ordoklass O(n) eftersom det sker n antal operationer när alla element flyttar på sig
#O(n) eftersom remove() kollar genom alla element i värsta fall för att hitta det första 
    def is_empty(self):
        # Kontrollera om kön är tom
        return len(self._elements) == 0

    def count(self):
        # Returnera antalet element i kön
        return len(self._elements) 

    def first(self):
        # Returnera det första elementet utan att ta bort det
        if not self.is_empty():
            return self._elements[0]
        else:
            raise IndexError("Kön är tom")
