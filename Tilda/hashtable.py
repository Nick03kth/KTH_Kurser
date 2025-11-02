class HashNode:
    """Noder till klassen Hashtable """

    def __init__(self, key="", data=None):
        """
        key är nyckeln som används vid hashningen
        data är det objekt som ska hashas in
        """
        self.key = key
        self.data = data

class Hashtable:

    def __init__(self, size=11):
        """
        size: hashtabellens storlek
        """
        self.size = size
        self.table = [[] for _ in range(size)]  # Skapar en lista med listor (krocklistor)
        self.count = 0  # Håller koll på antalet element

    def store(self, key, data):
        """
        key är nyckeln
        data är objektet som ska lagras
        Stoppar in "data" med nyckeln "key" i tabellen.
        """
        if self.count / self.size > 0.5:
            self.resize()  # Om beläggningsfaktorn är över 50 %, ändra storleken på tabellen

        hashvalue = self.hashfunction(key)
        # Kolla om nyckeln redan finns, och uppdatera data om så är fallet
        for node in self.table[hashvalue]:
            if node.key == key:
                node.data = data
                return
        # Om nyckeln inte finns, lägg till en ny nod
        self.table[hashvalue].append(HashNode(key, data))
        self.count += 1

    def search(self, key):
        """
        key är nyckeln
        Hämtar det objekt som finns lagrat med nyckeln "key" och returnerar det.
        Om "key" inte finns ska det bli KeyError
        """
        hashvalue = self.hashfunction(key)
        # Gå igenom alla noder på det beräknade indexet
        for node in self.table[hashvalue]:
            if node.key == key:
                return node.data
        # Om vi inte hittar nyckeln, kastar vi ett KeyError
        raise KeyError(f"Nyckeln '{key}' finns inte i hashtabellen")

    def hashfunction(self, key):
        """
        key är nyckeln
        Beräknar hashfunktionen för key
        """
        #Multiplicerar med 32; fördelaktigt för binärar datorer => Bättre hashfunktion
        result = 0
        for char in key:
            result = result * 32 + ord(char)
        return result % self.size

    def resize(self):
        """
        Ändrar storleken på hashtabellen genom att dubbla storleken och omfördela alla element
        """
        old_table = self.table
        self.size = self._next_prime(self.size * 2)  # Dubbla storleken till närmaste primtal
        self.table = [[] for _ in range(self.size)]
        self.count = 0

        for chain in old_table:
            for node in chain:
                self.store(node.key, node.data)

    def _next_prime(self, n):
        """
        Hjälpmetod för att hitta närmaste primtal större än n
        """
        def is_prime(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        while not is_prime(n):
            n += 1
        return n
    
    def count_max_collisions(self):
        """
        Räknar det maximala antalet krockar vid en specifik indexplats
        """
        max_collisions = 0
        for chain in self.table:
            chain_length = len(chain)
            if chain_length > max_collisions:
                max_collisions = chain_length
        print(f"Maximalt antal krockar vid en indexplats: {max_collisions}")

        
#Fördelen med krocklistor är att:
#1. Vi inte behöver oroa oss om oändliga loops och hantering av olika former av rehashning
#2. Inte behöver ändra storleken på hashtabellen. Men i regel kommer krocklistorna bli mycket korta om vi ser till att det är 50% luft i hashtabellen! Vilket gör sökningen ännu fortare då vi letar efter en särskild key inuti en krocklista; traverserar snabbt
#3. Dessutom undviker vi kluster problem.