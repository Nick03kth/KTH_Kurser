# Demonstrerar lzw

class Table:
    # Enkel kodning med en lista - strängar kodas som index i listan
    def __init__(self):
        self.t = []

    def add(self, x):
        self.t.append(x)

    def exists(self, x):
        return x in self.t

    def code(self, x):
        if not x in self.t:
            return ""
        else:
            return self.t.index(x)
        

def lzw(text):
    table = Table()
    # iterator för att enkelt kunna gå igenom strängen.
    # vi sätter # som stopptecken i iteratorn
    q = iter(text + "#") 
    s = ""
    kodtext = ""
    c = next(q)
    while not (c == "#"):
        if table.exists(s+c):
            s = s + c
        else:
            kodtext += str(table.code(s)) + c
            table.add(s+c)
            s = ""
        c = next(q)
            
    if not s == "":
        kodtext += str(table.code(s))

    return kodtext


z = lzw("NÄSSNUVSNORSNOK")
print(z)