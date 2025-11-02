class Node:
    def __init__(self, value):
        # Initialiserar noden med ett givet värde och sätter pekaren till nästa nod till None
        self.data = value  # Lagrar datan i noden
        self.next = None  # Pekare till nästa nod i kön

    def getData(self):
        return self.data
    
    def getNext(self):  
        # Returnerar nästa nod som denna nod pekar på 
        return self.next
    
    def setData(self, newdata):
        # Sätter nytt värde för nodens data
        self.data = newdata

    def setNext(self, newnext):
        # Ställer in nästa nod som denna nod pekar på
        self.next = newnext
    
class LinkedQ:
    def __init__(self):
        self._first = None  # Pekare till den första noden i kön
        self._last = None  # Pekare till den sista noden o kön

    def is_empty(self):
        # Returnerar True om kön är tom
        return self._first is None
    
    def enqueue(self, item):
        # Skapa en ny nod med värdet 'item'
        new_node = Node(item)

        if self.is_empty():
            # Om kön är tom, kommer både first och last peka på den nya noden
            self._first = self._last = new_node
        else:
            # Om kön inte är tom, läggs den nya noden till i slutet och den senaste pekaren uppdateras
            self._last.setNext(new_node)
            self._last = new_node

    def dequeue(self):
        # Ta bort och returnera värdet längst fram i kön
        if self.is_empty():
            raise IndexError('Kön är tom')
        
        # Få värdet av den första noden
        value = self._first.getData()   

        # Flytta första pekaren till nästa nod
        self._first = self._first.getNext()

        # Om kön blir tom efter dequeue, återställ den sista pekaren
        if self._first is None:
            self._last = None

        return value
    
    def size(self):
        # Traverse the linked list to count the number of nodes
        count = 0
        current_node = self._first
        while current_node is not None:
            count += 1
            current_node = current_node.getNext()
        return count
    
class ParentNode:
    def __init__(self, word, parent=None):
        self.word = word
        self.parent = parent