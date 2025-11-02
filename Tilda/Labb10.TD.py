from linkedQFile3 import LinkedQ
from molgrafik import *

#Lista över alla godkända atomnamn
atoms_list = """
H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg Bh Hs Mt Ds Rg Cn Fl Lv
""".split()

atomic_weights = {
    "H": 1.00794, "He": 4.002602, "Li": 6.941, "Be": 9.012182, "B": 10.811,
    "C": 12.0107, "N": 14.0067, "O": 15.9994, "F": 18.9984032, "Ne": 20.1797,
    "Na": 22.98976928, "Mg": 24.3050, "Al": 26.9815386, "Si": 28.0855,
    "P": 30.973762, "S": 32.065, "Cl": 35.453, "K": 39.0983, "Ar": 39.948,
    "Ca": 40.078, "Sc": 44.955912, "Ti": 47.867, "V": 50.9415, "Cr": 51.9961,
    "Mn": 54.938045, "Fe": 55.845, "Ni": 58.6934, "Co": 58.933195, "Cu": 63.546,
    "Zn": 65.38, "Ga": 69.723, "Ge": 72.64, "As": 74.92160, "Se": 78.96,
    "Br": 79.904, "Kr": 83.798, "Rb": 85.4678, "Sr": 87.62, "Y": 88.90585,
    "Zr": 91.224, "Nb": 92.90638, "Mo": 95.96, "Tc": 98, "Ru": 101.07,
    "Rh": 102.90550, "Pd": 106.42, "Ag": 107.8682, "Cd": 112.411, "In": 114.818,
    "Sn": 118.710, "Sb": 121.760, "I": 126.90447, "Te": 127.60, "Xe": 131.293,
    "Cs": 132.9054519, "Ba": 137.327, "La": 138.90547, "Ce": 140.116, "Pr": 140.90765,
    "Nd": 144.242, "Pm": 145, "Sm": 150.36, "Eu": 151.964, "Gd": 157.25,
    "Tb": 158.92535, "Dy": 162.500, "Ho": 164.93032, "Er": 167.259, "Tm": 168.93421,
    "Yb": 173.054, "Lu": 174.9668, "Hf": 178.49, "Ta": 180.94788, "W": 183.84,
    "Re": 186.207, "Os": 190.23, "Ir": 192.217, "Pt": 195.084, "Au": 196.966569,
    "Hg": 200.59, "Tl": 204.3833, "Pb": 207.2, "Bi": 208.98040, "Po": 209,
    "At": 210, "Rn": 222, "Fr": 223, "Ra": 226, "Ac": 227, "Pa": 231.03588,
    "Th": 232.03806, "Np": 237, "U": 238.02891, "Am": 243, "Pu": 244,
    "Cm": 247, "Bk": 247, "Cf": 251, "Es": 252, "Fm": 257, "Md": 258,
    "No": 259, "Lr": 262, "Rf": 265, "Db": 268, "Hs": 270, "Sg": 271,
    "Bh": 272, "Mt": 276, "Rg": 280, "Ds": 281, "Cn": 285
}

#Klass för att hantera syntaktiska fel i molekylen
class MoleculeError(Exception):
    pass

#skapar en ruta i molekylträdet
class Ruta:
    def __init__(self, atom="()", num=1):
        self.atom = atom  #atommens namn eller grupp
        self.num = num    #antalet av denna atom eller grupp
        self.next = None  #pekare till nästa ruta i samma grupp
        self.down = None  #pekare till första rutan i en undergrupp

#skapapr en kö av tecken från en molekylsträng
def create_queue(input_string):
    q = LinkedQ()
    for char in input_string:
        q.enqueue(char)
    return q

#läser in en grupp och skapar motsvarande trädstruktur
def readgroup(queue):
    ruta = Ruta()  #Skapar en tom ruta
    if queue.peek() == "(":
        queue.dequeue()  #Tar bort "("
        ruta.down = readmolecule(queue)  #Skapar ett subträd för gruppen 
        if queue.is_empty() or queue.peek() != ")": #Output från read_mol funktionen ger current.next som vi kontrollerar har ")" i slutet
            raise MoleculeError("Saknad högerparentes vid radslutet")
        queue.dequeue()  #Tar bort ")"
        ruta.num = readnumber(queue)  #Läs antalet
    else:
        ruta.atom = readatom(queue)  #Läs atommens namn
        ruta.num = readnumber(queue)  #Läs antalet
    return ruta

#läser en molekyl och skapar motsvarande trädstruktur
def readmolecule(queue):
    start_ruta = readgroup(queue)
    current = start_ruta
    while not queue.is_empty() and queue.peek() not in ")":
        current.next = readgroup(queue)
        current = current.next
    return start_ruta

#läser in ett atomnamn och kontrollerarr dess giltighet
def readatom(queue):
    if queue.is_empty():
        raise MoleculeError("Saknad atom vid radslutet")
    first_char = queue.dequeue()
    if not first_char.isupper():
        raise MoleculeError(f"Saknad stor bokstav vid radslutet {first_char}")
    second_char = ""
    if not queue.is_empty() and queue.peek().islower():
        second_char = queue.dequeue()
    atom_name = first_char + second_char
    if atom_name not in atoms_list:
        raise MoleculeError(f"Okänd atom vid radslutet {atom_name}")
    return atom_name

#läser nummer efter en atom eller grupp
def readnumber(queue):
    if queue.is_empty() or not queue.peek().isdigit():
        return 1
    num_str = ""
    while not queue.is_empty() and queue.peek().isdigit():
        num_str += queue.dequeue()
    num = int(num_str)
    if num == 0:
        raise MoleculeError("För litet tal vid radslutet")
    return num

#Validerar molekylsträngen och skapa molekylträdet
def validate_and_build_tree(molecule):
    queue = create_queue(molecule)
    full_formula = molecule
    try:
        mol_tree = readmolecule(queue)
        if not queue.is_empty():
            remaining_str = full_formula[len(full_formula) - queue.size():]
            raise MoleculeError(f"Felaktig gruppstart vid radslutet {remaining_str}")
        return mol_tree, "Formeln är syntaktiskt korrekt"
    except MoleculeError as e:
        return None, str(e)

#funktion för att räkna ut molekylens vikt rekursivt
def weight(mol):
    if mol is None:
        return 0
    if mol.down is None:
        #hämtar atomvikten från atomic_weights
        atom_weight = atomic_weights.get(mol.atom, 0)
        if atom_weight == 0:
            print(f"Vikt för atom saknas: {mol.atom}")
        #Multiplicera atomvikten med antalet atomer i rutan (default är 1)
        total_weight = atom_weight * mol.num
        return total_weight + weight(mol.next)
    else:
        #Beräkna vikten för gruppen rekursivt
        group_weight = weight(mol.down) * mol.num
        print(f"Gruppvikt för {mol.atom} med faktor {mol.num}: {group_weight}")  #Felsökning
        return group_weight + weight(mol.next)
#Huvudprogramet som validerar formeln, skapar trädet, ritar det och beräknar vikten
def main():
    while True:
        formula_input = input("Ange molekylformel (# för att avsluta): ").strip()
        if formula_input == "#":
            break
        mol_tree, result = validate_and_build_tree(formula_input)
        print(result)
        if mol_tree:
            #beräknar och skriver ut molekylvikten först
            print("Molekylvikten är:", weight(mol_tree))
            #Visa ett meddelande till användaren att stänga fönstret efter visning
            print("Fönstret för molekylstrukturen kommer att öppnas. Stäng det för att fortsätta med nästa molekyl.")
            #Visa molekylträddet
            molgrafik = Molgrafik()
            molgrafik.show(mol_tree)
            #Efter att fönstret stängs kommer programmet att återgå till inmatningspromten

if __name__ == "__main__":
    main()