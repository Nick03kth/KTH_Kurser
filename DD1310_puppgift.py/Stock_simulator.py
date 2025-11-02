import yfinance as yf
import matplotlib.pyplot as plt
import tkinter as tk

def fundamental_analysis():
    ticker = ticker_entry_fundamental.get()
    stock = yf.Ticker(ticker)
    info = stock.info
    result_text.set(f"\n-------------Fundamental analys för {info['longName']}-------------\n"
                    f"Soliditet: {'Data ej tillgänglig'}\n"  # Soliditet might need a custom calculation
                    f"P/E-tal: {info.get('trailingPE', 'Data ej tillgänglig')}\n"
                    f"P/S-tal: {info.get('priceToSalesTrailing12Months', 'Data ej tillgänglig')}\n"
                    f"Beta-värde: {info.get('beta', 'Data ej tillgänglig')}")

def technical_analysis():
    ticker = ticker_entry_technical.get()
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
    plt.show()  # Visa plotten

def rank_stocks_by_beta():
    tickers = ticker_entry_beta.get().strip().split(',')[:3]
    beta_values = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.info
        beta = info.get('beta', 'Data ej tillgänglig')
        beta_values[ticker] = beta
    
    # Sort the stocks by beta value in descending order
    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1] if isinstance(item[1], float) else 0, reverse=True)
    
    # Extracting tickers and betas
    tickers, betas = zip(*sorted_stocks)
    
    # Plot ranking of beta values
    plt.figure(figsize=(10, 6))
    plt.bar(tickers, betas, color='skyblue')
    plt.xlabel('Ticker')
    plt.ylabel('Beta-värde')
    plt.title('Rangordning av aktier med avseende på betavärde')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def show_fundamental_analysis():
    hide_inputs()
    result_label.pack()
    ticker_label_fundamental.pack()
    ticker_entry_fundamental.pack()
    analyze_button_fundamental.pack()

def show_technical_analysis():
    hide_inputs()
    result_label.pack()
    ticker_label_technical.pack()
    ticker_entry_technical.pack()
    analyze_button_technical.pack()

def show_beta_ranking():
    hide_inputs()
    result_label.pack()
    ticker_label_beta.pack()
    ticker_entry_beta.pack()
    rank_button_beta.pack()

def hide_inputs():
    ticker_label_fundamental.pack_forget()
    ticker_label_technical.pack_forget()
    ticker_label_beta.pack_forget()
    ticker_entry_fundamental.pack_forget()
    ticker_entry_technical.pack_forget()
    ticker_entry_beta.pack_forget()
    analyze_button_fundamental.pack_forget()
    analyze_button_technical.pack_forget()
    rank_button_beta.pack_forget()

def close_program():
    root.destroy()

root = tk.Tk()
root.title("Aktieanalys")

# Skapa huvudmeny
menu_label = tk.Label(root, text="Välkommen till Aktieanalys", font=("Helvetica", 16, "bold"))
menu_label.pack(pady=10)

# Text och knappar för fundamental analys
fundamental_label = tk.Label(root, text="Välj analysform:", font=("Helvetica", 14))
fundamental_label.pack()

fundamental_button = tk.Button(root, text="Fundamental analys", command=show_fundamental_analysis, font=("Helvetica", 14))
fundamental_button.pack(pady=5)

# Text och knappar för teknisk analys
technical_label = tk.Label(root, text="Välj analysform:", font=("Helvetica", 14))
technical_label.pack()

technical_button = tk.Button(root, text="Teknisk analys", command=show_technical_analysis, font=("Helvetica", 14))
technical_button.pack(pady=5)

# Text och knapp för betavärde ranking
beta_label = tk.Label(root, text="Välj analysform:", font=("Helvetica", 14))
beta_label.pack()

beta_button = tk.Button(root, text="Betavärde ranking", command=show_beta_ranking, font=("Helvetica", 14))
beta_button.pack(pady=5)

# Skapa ett textfält för tickersymbol (för fundamental analys)
ticker_label_fundamental = tk.Label(root, text="Ange aktiens tickersymbol (t.ex. 'AAPL' för Apple):", font=("Helvetica", 14))
ticker_entry_fundamental = tk.Entry(root, font=("Helvetica", 14))
analyze_button_fundamental = tk.Button(root, text="Analysera", command=fundamental_analysis, font=("Helvetica", 14))

# Skapa ett textfält för tickersymbol (för teknisk analys)
ticker_label_technical = tk.Label(root, text="Ange aktiens tickersymbol (t.ex. 'AAPL' för Apple):", font=("Helvetica", 14))
ticker_entry_technical = tk.Entry(root, font=("Helvetica", 14))
analyze_button_technical = tk.Button(root, text="Analysera", command=technical_analysis, font=("Helvetica", 14))

# Skapa ett textfält för tickersymbol (för betavärde ranking)
ticker_label_beta = tk.Label(root, text="Ange aktietickersymboler för de tre aktierna (separerade med kommatecken):", font=("Helvetica", 14))
ticker_entry_beta = tk.Entry(root, font=("Helvetica", 14))
rank_button_beta = tk.Button(root, text="Rangordna", command=rank_stocks_by_beta, font=("Helvetica", 14))

# Skapa ett textfält för resultatet av analysen
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, wraplength=400, justify="left", font=("Helvetica", 14))

# Avslutningsknapp
exit_button = tk.Button(root, text="Avsluta", command=close_program, font=("Helvetica", 14))
exit_button.pack(pady=20, side="bottom")

root.mainloop()
