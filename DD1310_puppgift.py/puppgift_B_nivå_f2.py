import yfinance as yf


def fundamental_analysis(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        print(f"\n-------------Fundamental analys för {info.get('longName', ticker)}-------------")
        
        # Handling for P/E-tal
        pe_tal = info.get('trailingPE')
        if pe_tal is None:  # If P/E-tal is None
            pe_tal = info.get('forwardPE', 'Data ej tillgänglig')
        print(f"P/E-tal: {pe_tal if pe_tal != 'Data ej tillgänglig' else 'Data ej tillgänglig'}")
        
        # Handling for P/S-tal
        ps_tal = info.get('priceToSalesTrailing12Months', 'Data ej tillgänglig')
        print(f"P/S-tal: {ps_tal}")
        
        # Assuming 'returnOnAssets' as a placeholder for Soliditet since actual solidity calculation may vary
        soliditet = info.get('returnOnAssets', 'Data ej tillgänglig')  
        print(f"Soliditet: {soliditet}")
        
    except Exception as e:
        print("Ett fel uppstod vid hämtning av data: ", str(e))


# This function retrieves and prints the technical analysis of a chosen stock.
def technical_analysis(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="1mo")
    print(f"\n-------------Teknisk analys för {stock.info['longName']}-------------")
    print(f"Kursutveckling (30 senaste dagarna): {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100:.2f} %")
    print(f"Betavärde: {stock.info.get('beta', 'Data ej tillgänglig')}")
    print(f"Lägsta kurs (30 senaste dagarna): {hist['Low'].min()}")
    print(f"Högsta kurs (30 senaste dagarna): {hist['High'].max()}")

# This function displays the menu and handles user interaction.
def show_menu():
    aktier = {'1': 'ERIC-B.ST', '2': 'ELUX-B.ST', '3': 'AZN.ST'}
    print("""
        ------------------------Meny--------------------------
        1. Fundamental analys (Vid långsiktigt aktieinnehav)
        2. Teknisk analys (Vid kort aktieinnehav)
        3. Rangordning av aktier med avseende på dess betavärde
        4. Avsluta
        """)
    choice = input("Vilket alternativ vill du välja? ")
    handle_choice(choice, aktier)

# This function processes the user's choice.
def handle_choice(choice, aktier):
    if choice in ['1', '2']:
        print("\nEn analys kan utföras för följande aktier:")
        for key, value in aktier.items():
            print(f"{key}. {value}")
        stock_choice = input("\nVilken aktie vill du analysera? ")
        if stock_choice in aktier:
            if choice == '1':
                fundamental_analysis(aktier[stock_choice])
            elif choice == '2':
                technical_analysis(aktier[stock_choice])
        else:
            print("Ogiltigt val, försök igen.")
    elif choice == '3':
        rank_stocks_by_beta(aktier)
    elif choice == '4':
        print("Avslutar programmet.")
        return
    else:
        print("Ogiltigt val, försök igen.")
    show_menu()  # Show the menu again for next operations

# This function ranks the stocks by their beta value.
def rank_stocks_by_beta(aktier):
    beta_values = {}
    for key, ticker in aktier.items():
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            beta = info.get('beta', None)
            if beta is not None:  # Ensure beta value exists before adding
                stock_name = info.get('longName', 'Okänd')
                beta_values[stock_name] = beta
        except Exception as e:
            print(f"Ett fel uppstod vid hämtning av data för {ticker}: ", str(e))

    # Sort the stocks by beta value in descending order
    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1], reverse=True)
    
    print("\n-------------Rangordning av aktier med avseende på betavärde-------------")
    for name, beta in sorted_stocks:
        print(f"{name}: Beta-värde = {beta}")


if __name__ == "__main__":
    show_menu()
