class ElementNode:
    def __init__(self, data):
        # Skapa en nod med ett värde och en referens till nästa nod
        self.data = data
        self.next_node = None

class LinkedQ:
    def __init__(self):
        # Initiera en tom kö
        self._head = None 
        self._tail = None
        self._count = 0

    def enqueue(self, data):
        # Lägg till ett nytt värde (sist)
        new_node = ElementNode(data)  # Skapa ny nod
        if self.is_empty():
            self._head = self._tail = new_node  # Om kön är tom blir head och tail samma nod
        else:
            self._tail.next_node = new_node  # Lägg till den nya noden sist och uppdatera referensen
            self._tail = new_node
        self._count += 1
    #OBS detta är motsvarigheten till arrayQs add()
    #Men dequueue och enqueueu är dock ordoklass O(1) så mer effektiv än array klassens köhantering
    
    def dequeue(self):
        # Ta bort och returnera värdet på den första noden i kön
        if self.is_empty():
            raise IndexError("Kön är tom")
        data = self._head.data  # Hämta värdet från den första noden
        self._head = self._head.next_node  # Flytta head till nästa nod
        if self._head is None:
            # Om kön blir tom, uppdatera tail
            self._tail = None
        self._count -= 1
        return data
    
    def is_empty(self):
        # Kontrollera om kön är tom
        return self._head is None
    
    def size(self):
        return self._count
    
    def peek(self):
        # Returnera värdet på den första noden utan att ta bort den
        if self.is_empty():
            return None
        return self._head.data

    def rest(self):
        # Returnera alla värden i kön som en sträng
        current = self._head
        result = []
        while current is not None:
            result.append(current.data)
            current = current.next_node
        return ''.join(result)
    
    def print_queue(self):
        # Skriv ut alla värden i kön
        current = self._head
        while current is not None:
            print(current.data, end=" ")
            current = current.next_node
        print()
    

















    #Egentligen är denna onödig metod men ifall det finns behov har vi en sorterings metod.
    def sort_queue(self):
        # Sortera köns element
        if self.is_empty():
            return

        # Steg 1: Extrahera värdena till en lista
        values = []
        current = self._head
        while current is not None:
            values.append(current.data)
            current = current.next_node

        # Steg 2: Sortera listan
        
        values.sort()

        # Steg 3: Återuppbygg kö med sorterade värden
        self._head = None
        self._tail = None
        self._count = 0

        for value in values:
            self.enqueue(value)  # Lägg till värdena i sorterad ordning
