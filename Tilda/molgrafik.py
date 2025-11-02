def version():
    # Kontrollera vilken Python-version som används
    import sys
    datatyp = type(sys.version_info)
    if datatyp == type(()):
        version = sys.version_info[0]
    else:
        version = sys.version_info.major
    return version

# Importera Tkinter baserat på Python-versionen
if version() == 3:
    from tkinter import *
else:
    from tkinter import *

class Ruta:
    # Klass för att representera en atomruta med en viss atom, antal och kopplingar
    def __init__(self, atom="()", num=1):
        self.atom = atom
        self.num = num
        self.next = None
        self.down = None

class Molgrafik:
    # Klass för att hantera grafisk visning av molekylstrukturen
    def __init__(self):
        self.root = None
        self.stor = ("Courier", 18, "bold")  # Font för större text
        self.liten = ("Courier", 14, "bold") # Font för mindre text

    def ram(self, master, sidan):
        """ Skapar en ram (frame) placerad på angiven sida. """
        ramen = Frame(master, bg="white")
        ramen.pack(side=sidan, fill=BOTH)
        return ramen

    def atomruta(self, master, namn, num):
        """ Rita en ruta för en atom med dess namn och antal. """
        ruta = Frame(master, bg="yellow", borderwidth=2, relief=GROOVE)
        ruta.pack(side=LEFT)
        atom = Frame(ruta, bg="yellow")
        atom.pack(side=LEFT)
        Label(atom, text=namn, font=self.stor, bg="yellow", fg="black").pack()
        Frame(atom, height=5, bg="yellow").pack()
        if num > 1:
            Label(ruta, text=str(num), font=self.liten, bg="yellow", fg="black").pack(side=BOTTOM)

    def streck(self, master):
        """ Rita ett streck (linje) mellan atomer. """
        strecket = Frame(master)
        strecket.pack(side=LEFT, fill=BOTH, expand=True)
        Frame(strecket, bg="white", height=20).pack(fill=X)
        Frame(strecket, bg="red", height=4, width=25).pack(fill=X)
        Frame(strecket, bg="white").pack(fill=BOTH, expand=1)

    def stolpe(self, master):
        """ Rita en stolpe mellan atomer på olika nivåer. """
        hela = self.ram(master, TOP)
        stolpen = self.ram(hela, LEFT)
        Frame(stolpen, bg="white", width=15).pack(side=LEFT)
        Frame(stolpen, bg="red", width=4, height=25).pack(side=LEFT)
        Frame(hela, bg="white").pack(fill=BOTH, expand=1)

    def picture(self, master, p):
        """ Rita molekylstrukturen rekursivt utifrån den givna strukturen. """
        if p is None:
            return
        storruta = self.ram(master, LEFT)
        rest = self.ram(master, LEFT)
        uppruta = self.ram(storruta, TOP)
        nerruta = self.ram(storruta, TOP)
        self.atomruta(uppruta, p.atom, p.num)
        if p.down:
            self.stolpe(nerruta)
            self.picture(nerruta, p.down)
            self.ram(nerruta, TOP)
        if p.next:
            self.streck(uppruta)
            self.picture(rest, p.next)

    def show(self, p):
        """ Display the complete structure. """
        if self.root is not None:
            self.root.destroy()
        
        self.root = Tk()
        self.root.title("Molekylstruktur")  # Optional: set a window title
        Label(self.root, text="  ", font=self.stor, bg="white", fg="black").pack(side=LEFT, fill=Y)
        
        # Draw the molecular structure starting from the root node p
        self.picture(self.root, p)
        
        # Start the Tkinter event loop
        self.root.mainloop()  # This mainloop call is enough; no need for another