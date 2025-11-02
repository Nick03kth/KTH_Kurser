  # OBS!!!Vi importerar ArrayQFile ifall vi ska köra uppgift 1-4 

"""
#UPG 2: Vi kan testa vår klass direkt här under:
q = ArrayQ()
q.enqueue(1)
q.enqueue(2)
x = q.dequeue()
y = q.dequeue()
if (x == 1 and y == 2):
    print("OK")
else:
    print("FAILED")
"""

# UPG 3/7: Trollkarlsprogrammet
import sys
from linkedQFile import LinkedQ



# Kortvärden, vi värdesätter de enligt sample input/outputen. Kn ska vara högre än 10 men lägre än dam. D<K<E
card_values = {
    "Kn": 11,    # Knäckt
    "D": 12,   # Dam
    "K": 13,  # Kung
    "E": 14    # Ess vi sätter värdet 14 för att markera att detta kort är mest värdefullt i kortleken.
}
# OBS!!! Onödig funktion har vi insett endast användbar om vi ville sortera 
def get_card_value(card):
    # Returnera kortets värde baserat på om det är en siffra eller ett ansikte
    if card.isdigit():
        return int(card)
    elif card in card_values:
        return card_values[card] 
    else:
        raise ValueError(f"Okänt kort: {card}")








def perform_card_trick(sequence):
    # Skapa en kö och fyll den med kort i den angivna ordningen
    queue = LinkedQ()
    for card in sequence:
        queue.enqueue(card) 
    
    output = []  # För att lagra korten som tas ut i ordning
    
    # Simulera korttricket
    turn = True
    while not queue.is_empty():
        if turn:
            # Flytta det översta kortet till slutet av kön
            queue.enqueue(queue.dequeue())
        else:
            # Ta nästa kort och lägg det i resultatet
            output.append(queue.dequeue())
        turn = not turn  # Byt mellan att flytta och ta bort kort
    
    return output

if __name__ == "__main__":
   # print("Skriv in dina kort (separera kort med mellanslag)")
    input_data = sys.stdin.readline().strip()
    
    # Konvertera indata till en lista (siffror eller ansikten)
    sequence = input_data.split()
    
    # Utför korttricket
    trick_result = perform_card_trick(sequence)

    print(" ".join(trick_result))

"""
    if trick_result == correct_face_order or trick_result == correct_number_order:
        print("Magiskt!")
    else:
        print("Det där var inte magi.")
        """
