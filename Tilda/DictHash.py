class DictHash:
    
    def __init__(self):
        self.storage= {} # Skapar tom dict

    def store(self, nyckel,data):
        self.storage[nyckel]=data #Lagrar nyckel/data par i dict

    def search(self,nyckel):
        return self.storage.get(nyckel) #-->value
    
#Extra privata metoder: Gör koden mer användartillgänglig; enklare

    def __getitem__(self,nyckel):
        return self.search(nyckel) 
#Möjliggör indexering mha hakparanteser som vi gör med listor fast nu med dict
    
    def __contains__(self,nyckel):
        return nyckel in self.storage #--> True/False
    
    