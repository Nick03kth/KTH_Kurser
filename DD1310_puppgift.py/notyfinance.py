import yfinance as yf

# Definiera aktierna
aktier = {
    'Ericsson': 'ERIC-B.ST',
    'Electrolux': 'ELUX-B.ST',
    'AstraZeneca': 'AZN.ST'
}

# Skapa en funktion för att hämta och visa fundamentala/tekniska data
def hamta_data(aktie_symbol):
    aktie = yf.Ticker(aktie_symbol)
    info = aktie.info
    
    # Grundläggande finansiell information
    print(f"\n{info['longName']}")
    print(f"Marknadsvärde: {info.get('marketCap')}")
    print(f"P/E-tal: {info.get('trailingPE')}")
    print(f"P/S-tal: {info.get('priceToSalesTrailing12Months')}")
    print(f"Beta-värde: {info.get('beta')}")
    
    # Teknisk information - Exempel: 52 veckors högsta och lägsta
    print(f"52 veckors högsta: {info.get('fiftyTwoWeekHigh')}")
    print(f"52 veckors lägsta: {info.get('fiftyTwoWeekLow')}")

# Loopa genom aktierna och hämta data
for namn, symbol in aktier.items():
    hamta_data(symbol)
