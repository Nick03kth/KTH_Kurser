from linkedQFile3 import LinkedQ
from molgrafik import Molgrafik

# Elementlista och atomvikter
element_list = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K',
                'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb',
                'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs',
                'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta',
                'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa',
                'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt',
                'Ds', 'Rg', 'Cn', 'Fl', 'Lv']

atom_weights = {
    "H": 1.0079, "C": 12.011, "O": 15.999, "Si": 28.085, # Fler atomvikter kan läggas till efter behov
}

class FormulaSyntaxError(Exception):
    pass

class Ruta:
    def __init__(self, atom="( )", num=1):
        self.atom = atom
        self.num = num
        self.next = None
        self.down = None

def create_queue(formula):
    queue = LinkedQ()
    for symbol in formula:
        queue.enqueue(symbol)
    return queue

def validate_formula(molecule):
    queue = create_queue(molecule)
    full_formula = molecule
    try:
        mol_tree = parse_molecule(queue, full_formula)
        if not queue.is_empty():
            remaining_str = full_formula[len(full_formula) - queue.size():]
            raise FormulaSyntaxError(f"Felaktig gruppstart vid radslutet {remaining_str}")
        return mol_tree  # Returnera molekylträdet om det är korrekt
    except FormulaSyntaxError as error:
        return str(error)

def parse_molecule(queue, formula):
    first_group = parse_group(queue, formula)
    current = first_group
    while not queue.is_empty() and queue.peek() not in ")":
        next_group = parse_group(queue, formula)
        current.next = next_group
        current = next_group
    return first_group

def parse_group(queue, formula):
    if queue.peek() == "(":
        queue.dequeue()
        mol = parse_molecule(queue, formula)
        if queue.is_empty() or queue.peek() != ")":
            raise FormulaSyntaxError("Saknad högerparentes vid radslutet")
        queue.dequeue()
        num = parse_number(queue, formula)
        rutan = Ruta(num=num)
        rutan.down = mol
    else:
        atom = parse_element(queue, formula)
        num = parse_number(queue, formula) if not queue.is_empty() and queue.peek().isdigit() else 1
        rutan = Ruta(atom, num)
    return rutan

def parse_element(queue, formula):
    if queue.is_empty():
        raise FormulaSyntaxError(f"För litet tal vid radslutet {formula}")
    first_char = queue.dequeue()
    if not first_char.isupper():
        remaining_str = formula[len(formula) - queue.size() - 1:]
        raise FormulaSyntaxError(f"Saknad stor bokstav vid radslutet {remaining_str}")
    second_char = ""
    if not queue.is_empty() and queue.peek().islower():
        second_char = queue.dequeue()
    atom_name = first_char + second_char
    if atom_name not in element_list:
        remaining_str = formula[len(formula) - queue.size():]
        raise FormulaSyntaxError(f"Okänd atom vid radslutet {remaining_str}")
    return atom_name

def parse_number(queue, formula):
    if queue.is_empty():
        remaining_str = formula[len(formula) - queue.size():]
        raise FormulaSyntaxError(f"Saknad siffra vid radslutet {remaining_str}")
    num = int(queue.dequeue())
    remaining_str = formula[len(formula) - queue.size():]
    if num == 0:
        raise FormulaSyntaxError(f"För litet tal vid radslutet {remaining_str}")
    elif num == 1 and (queue.is_empty() or not queue.peek().isdigit()):
        raise FormulaSyntaxError(f"För litet tal vid radslutet {remaining_str}")
    while not queue.is_empty() and queue.peek().isdigit():
        num = num * 10 + int(queue.dequeue())
    return num

def weight(mol):
    if mol is None:
        return 0
    total_weight = 0
    if mol.atom in atom_weights:
        total_weight += atom_weights[mol.atom] * mol.num
    total_weight += weight(mol.down) * mol.num
    total_weight += weight(mol.next)
    return total_weight

def main():
    mg = Molgrafik()
    while True:
        user_input = input("Ange molekylformel (# för att avsluta): ").strip()
        if user_input == "#":
            break
        result = validate_formula(user_input)
        if isinstance(result, Ruta):
            mol = result
            mg.show(mol)
            print(f"Molekylvikten är: {weight(mol)}")
        else:
            print(f"Fel: {result}")

if __name__ == "__main__":
    main()
