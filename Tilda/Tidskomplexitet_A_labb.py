import time
import matplotlib.pyplot as plt
import math
from A_labb import hitta_tot_min_bits

# Testvärden
värden_av_N = [10, 20, 40, 80, 160, 320]

# Generera fasta listor
testdata = {N: list(range(N)) for N in värden_av_N}

def mäta_tidskomplexitet():
    resultat = []
    c = 10  # Konstant headerkostnad

    for N in värden_av_N:
        arr = testdata[N]
        start_time = time.time()
        hitta_tot_min_bits(arr, c)
        end_time = time.time()
        elapsed_time = end_time - start_time
        resultat.append((N, elapsed_time))  # Logga N och tid

    return resultat

def visualisera_jämförelser(resultat):
    """Plotta en log-log representation av tidskomplexitet och jämför med teoretiska komplexiteter."""
    N = [punkt[0] for punkt in resultat]
    tid = [punkt[1] for punkt in resultat]

    # Kontrollera och ta bort eventuella ogiltiga tider
    giltiga_data = [(n, t) for n, t in zip(N, tid) if t > 0]
    N = [n for n, t in giltiga_data]
    tid = [t for n, t in giltiga_data]

    log_N = [math.log(n) for n in N]
    log_tid = [math.log(t) for t in tid]

    plt.figure(figsize=(10, 6))

    # Plotta experimentella mätpunkter
    plt.plot(log_N, log_tid, marker='o', label="Mätpunkter (log-log)")

    # Skapa teoretiska referenskurvor baserat på första mätpunkten
    k = tid[0] / (N[0]**3)  # Konstant k baserat på första punkten och O(n^3)
    for p, färg in [(2, 'r'), (3, 'g'), (4, 'b')]:  # p = 2, 3, 4
        referens_tid = [math.log(k * (n**p)) for n in N]
        plt.plot(log_N, referens_tid, linestyle='--', label=f"O(n^{p})")

    # Plotinställningar
    plt.title("Jämförelse av komplexiteter (log-log-skala)")
    plt.xlabel("log(N)")
    plt.ylabel("log(T(N))")
    plt.legend()
    plt.grid(True)
    plt.show()



if __name__ == "__main__":
    resultat = mäta_tidskomplexitet()
    visualisera_jämförelser(resultat)
