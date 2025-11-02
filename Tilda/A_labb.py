import math

def rakna_bits_mode_1(c, block):
    """
    Beräknar antalet bitar för ett block i mode 1.
    Först hittar vi det största värdet i blocket, sedan hittar vi den minsta exponenten till 2 som är större än eller lika med detta värde.
    Returnerar sedan antalet bitar som krävs enligt formeln c + s * k, där c är en konstant header-kostnad.
    """
    max_varde = max(block, key=abs)  # Hämta det största absolutvärdet för att säkerställa korrekt bitrepresentation

    # Hitta den minsta exponenten s för 2 som är större än eller lika med max_value enligt instruktionerna: xj=yj<2^s
    s = 0
    exp_av_2 = 0
    while exp_av_2 <= abs(max_varde): #Möjligtvis kan vi även begränsa så s är mindre än 30 enl instruktionerna
        s += 1
        exp_av_2 = 2 ** s

    k = len(block)  # Antal element i blocket
    
    return c + s * k

blocket =[99]
print(13+5+3+10)
def rakna_bits_mode_2(c, block, forra_block_varde=None):
    """
    Beräknar antalet bitar för ett block i mode 2
    Först gör vi om blocket till en lista med differenser, sedan hittar vi den minsta exponenten till 2 som är större än det största värdet i differenslistan.
    Om blocket är anslutet till ett tidigare block, beräknar vi differensen från sista värdet i föregående block annars behålls första värdet.
    Returnerar sedan antalet bitar som krävs enligt formeln c + s * k.
    """
    # Omvandla blocket till en lista med differenser
    diff_block = []
    if forra_block_varde is not None:
        # Första differensen beräknas från det sista värdet i föregående block
        diff_block.append(block[0] - forra_block_varde)
    else:
        # Om det inte finns något föregående block, behåll första värdet
        diff_block.append(block[0])

    for i in range(1, len(block)):
        diff_block.append(block[i] - block[i - 1])


    # Hitta det största värdet i     differenslistan
    max_diff = max(diff_block, key=abs)
    # Hitta den minsta exponenten s för 2 som är större än max_diff enligt reglerna i instruktionerna där yj< 2^(s-1) (jmf mode 1)
    s = 0
    exp_av_2 = 0
    while abs(exp_av_2 - 1) <= abs(max_diff):
        s += 1
        exp_av_2 = 2 ** s


    k = len(block)  

    return c + s * k
block=[2,2,2,2,2]
print(rakna_bits_mode_2(3,block,3))

def hitta_tot_min_bits(arr, c):
    n = len(arr) # = N
    dp = [float('inf')] * (n + 1)
    dp[0] = 0
    parent = [-1] * (n + 1)  # För att hålla reda på vilken blockindelning som användes

    # Gå igenom alla startpunkter i listan
    for i in range(n):
        # Samla alla möjliga resultat för varje blocklängd upp till hela listans längd
        for length in range(1, n - i + 1):
            block = arr[i:i + length]
            forra_block_varde = arr[i - 1] if i > 0 else None
            # Beräkna antalet bitar för mode 1 och mode 2
            bits_mode_1 = rakna_bits_mode_1(c, block)
            bits_mode_2 = rakna_bits_mode_2(c, block, forra_block_varde)
            
            current_bits = min(bits_mode_1, bits_mode_2)

            # Uppdatera dp-tabellen om vi har hittat en bättre lösning
            if dp[i] + current_bits < dp[i + length]:
                dp[i + length] = dp[i] + current_bits
                parent[i + length] = i

            

    # Särskilt fall där vi testar hela listan i mode 2, för att säkerställa att vi inte missar enkla besparingar i bit vid långa sekvenser som gynnas av differenserna
    entire_block_bits_mode_2 = rakna_bits_mode_2(c, arr)
    if entire_block_bits_mode_2 < dp[n]:
        dp[n] = entire_block_bits_mode_2
        parent[n] = 0

    return dp[n]

if __name__ == "__main__":
    # Läs in input
    N, c = map(int, input().split()) # Först N mellanslag c
    arr = [int(input()) for _ in range(N)] # sedan: Anv matar in

    # Beräkna minsta antal bitar
    result = hitta_tot_min_bits(arr, c)
    print(result)
