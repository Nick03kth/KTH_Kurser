import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk

def fundamental_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    result_text.set(f"\n-------------Fundamental analys för {info['longName']}-------------\n"
                    f"Soliditet: {'Data ej tillgänglig'}\n"  # Soliditet might need a custom calculation
                    f"P/E-tal: {info.get('trailingPE', 'Data ej tillgänglig')}\n"
                    f"P/S-tal: {info.get('priceToSalesTrailing12Months', 'Data ej tillgänglig')}\n"
                    f"Beta-värde: {info.get('beta', 'Data ej tillgänglig')}")

def technical_analysis(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    result_text.set(f"\n-------------Teknisk analys för {stock.info['longName']}-------------\n"
                    f"Kursutveckling (30 senaste dagarna): {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100:.2f} %\n"
                    f"Betavärde: {stock.info.get('beta', 'Data ej tillgänglig')}\n"
                    f"Lägsta kurs (30 senaste dagarna): {hist['Low'].min()}\n"
                    f"Högsta kurs (30 senaste dagarna): {hist['High'].max()}")
    
    # Plot kursutveckling
    plt.figure(figsize=(10, 6))
    plt.plot(hist.index, hist['Close'], label='Closing Price')
    plt.title(f"Kursutveckling för {stock.info['longName']} (30 senaste dagarna)")
    plt.xlabel('Datum')
    plt.ylabel('Kurs')
    plt.legend()
    plt.grid(True)
    plt.show()

def rank_stocks_by_beta(aktier):
    beta_values = {}
    for name, ticker in aktier.items():
        stock = yf.Ticker(ticker)
        info = stock.info
        beta = info.get('beta', 'Data ej tillgänglig')
        beta_values[name] = beta
    
    # Sort the stocks by beta value in descending order; if beta is 'Data ej tillgänglig', treat it as 0 for sorting purposes
    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1] if isinstance(item[1], float) else 0, reverse=True)
    
    result_text.set("\n-------------Rangordning av aktier med avseende på betavärde-------------\n")
    for name, beta in sorted_stocks:
        result_text.set(result_text.get() + f"{name}: Beta-värde = {beta}\n")

def show_fundamental_analysis():
    ticker = ticker_entry.get()
    fundamental_analysis(ticker)

def show_technical_analysis():
    ticker = ticker_entry.get()
    technical_analysis(ticker)

def show_ranking():
    rank_stocks_by_beta(aktier)

def close_program():
    root.destroy()

root = tk.Tk()
root.title("Aktieanalys")

# Skapa knappar för olika alternativ
fundamental_button = tk.Button(root, text="Fundamental analys", command=show_fundamental_analysis)
fundamental_button.pack()

technical_button = tk.Button(root, text="Teknisk analys", command=show_technical_analysis)
technical_button.pack()

ranking_button = tk.Button(root, text="Rangordning av aktier", command=show_ranking)

def show_ranking():
    tickers = ticker_entry_ranking.get().strip().split(',')[:3]
    rank_stocks_by_beta({name: aktier[name] for name in aktier if aktier[name] in tickers})

# Skapa ett inmatningsfält för tickersymbol (för rangordning)
ticker_label_ranking = tk.Label(root, text="Ange aktietickersymboler för de tre aktierna (separerade med kommatecken):")
ticker_label_ranking.pack()
ticker_entry_ranking = tk.Entry(root)
ticker_entry_ranking.pack()
ranking_button.pack()

exit_button = tk.Button(root, text="Avsluta", command=close_program)
exit_button.pack()

# Skapa ett inmatningsfält för tickersymbol
ticker_label = tk.Label(root, text="Ange aktiens tickersymbol (t.ex. 'AAPL' för Apple):")
ticker_label.pack()
ticker_entry = tk.Entry(root)
ticker_entry.pack()

# Skapa ett textfält för resultatet av analysen
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="left")
result_label.pack()

# Lista över aktier
aktier = {
    'Ericsson': 'ERIC-B.ST',
    'Electrolux': 'ELUX-B.ST',
    'AstraZeneca': 'AZN.ST'
}

root.mainloop()
