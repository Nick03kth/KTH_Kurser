import yfinance as yf

def fundamental_analysis(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    print(f"\n-------------Fundamental analys för {info['longName']}-------------")
    print(f"Soliditet: {'Data ej tillgänglig'}")  # Soliditet might need a custom calculation
    print(f"P/E-tal: {info.get('trailingPE', 'Data ej tillgänglig')}")
    print(f"P/S-tal: {info.get('priceToSalesTrailing12Months', 'Data ej tillgänglig')}")
    print(f"Beta-värde: {info.get('beta', 'Data ej tillgänglig')}")

def technical_analysis(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    print(f"\n-------------Teknisk analys för {stock.info['longName']}-------------")
    print(f"Kursutveckling (30 senaste dagarna): {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100:.2f} %")
    print(f"Betavärde: {stock.info.get('beta', 'Data ej tillgänglig')}")
    print(f"Lägsta kurs (30 senaste dagarna): {hist['Low'].min()}")
    print(f"Högsta kurs (30 senaste dagarna): {hist['High'].max()}")

def show_menu():
    aktier = {
        'Ericsson': 'ERIC-B.ST',
        'Electrolux': 'ELUX-B.ST',
        'AstraZeneca': 'AZN.ST'
    }
    print("""
        ------------------------Meny--------------------------
        1. Fundamental analys (Vid långsiktigt aktieinnehav)
        2. Teknisk analys (Vid kort aktieinnehav)
        3. Rangordning av aktier med avseende på dess betavärde
        4. Avsluta
        """)

def handle_choice(choice, aktier):
    if choice == '1':
        for index, (name, ticker) in enumerate(aktier.items(), start=1):
            print(f"{index}. {name}")
        stock_choice = int(input("Vilken aktie vill du göra fundamental analys på? "))
        chosen_stock = list(aktier.values())[stock_choice - 1]
        fundamental_analysis(chosen_stock)
    elif choice == '2':
        for index, (name, ticker) in enumerate(aktier.items(), start=1):
            print(f"{index}. {name}")
        stock_choice = int(input("Vilken aktie vill du göra teknisk analys på? "))
        chosen_stock = list(aktier.values())[stock_choice - 1]
        technical_analysis(chosen_stock)
    elif choice == '3':
        rank_stocks_by_beta(aktier)
    elif choice == '4':
        print("Avslutar programmet.")
        return False  # Return False to indicate the program should exit
    else:
        print("Ogiltigt val, försök igen.")
    return True  # Return True to continue showing the menu

def rank_stocks_by_beta(aktier):
    beta_values = {}
    for name, ticker in aktier.items():
        stock = yf.Ticker(ticker)
        info = stock.info
        beta = info.get('beta', 'Data ej tillgänglig')
        beta_values[name] = beta
    
    # Sort the stocks by beta value in descending order; if beta is 'Data ej tillgänglig', treat it as 0 for sorting purposes
    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1] if isinstance(item[1], float) else 0, reverse=True)
    
    print("\n-------------Rangordning av aktier med avseende på betavärde-------------")
    for name, beta in sorted_stocks:
        print(f"{name}: Beta-värde = {beta}")
    
def main():
    aktier = {
        'Ericsson': 'ERIC-B.ST',
        'Electrolux': 'ELUX-B.ST',
        'AstraZeneca': 'AZN.ST'
    }

    continue_program = True
    while continue_program:
        show_menu()
        choice = input("Vilket alternativ vill du välja? ")
        continue_program = handle_choice(choice, aktier)

if __name__ == "__main__":
    main()