import yfinance as yf
import tkinter as tk
from tkinter import ttk, messagebox

def fundamental_analysis(ticker):
    try:
        stock = yf.Ticker(ticker)  # Create a Ticker object
        info = stock.info  # Info is a dictionary with stock data
        result = f"-------------Fundamental analys för {info.get('longName', ticker)}-------------\n\n"
        
        pe_tal = info.get('trailingPE', info.get('forwardPE', 'Data ej tillgänglig'))
        result += f"P/E-tal: {pe_tal}\n"
        
        ps_tal = info.get('priceToSalesTrailing12Months', 'Data ej tillgänglig')
        result += f"P/S-tal: {ps_tal}\n"
        
        # Solvency calculation: Assets minus liabilities
        total_assets = info.get('totalAssets', 'Data ej tillgänglig')
        total_liabilities = info.get('totalLiab', 'Data ej tillgänglig')
        if total_assets != 'Data ej tillgänglig' and total_liabilities != 'Data ej tillgänglig':
            solvency = total_assets - total_liabilities
        else:
            solvency = 'Data ej tillgänglig'
        result += f"Soliditet (Solvency): {solvency}\n"
        
        # Print data to console for verification
        print(f"Data for {ticker}:")
        print(f"PE Ratio: {pe_tal}")
        print(f"PS Ratio: {ps_tal}")
        print(f"Total Assets: {total_assets}")
        print(f"Total Liabilities: {total_liabilities}")
        print(f"Solvency: {solvency}")
        
        return result
    except Exception as e:
        return f"Ett fel uppstod vid hämtning av data: {str(e)}"

def technical_analysis(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        result = f"-------------Teknisk analys för {stock.info.get('longName', ticker)}-------------\n\n"
        result += f"Kursutveckling (30 senaste dagarna): {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100:.2f} %\n"  # Iloc helps navigate and fetch data from specific rows in columns
        result += f"Betavärde: {stock.info.get('beta', 'Data ej tillgänglig')}\n"
        result += f"Lägsta kurs (30 senaste dagarna): {hist['Low'].min()}\n"
        result += f"Högsta kurs (30 senaste dagarna): {hist['High'].max()}\n"
        
        # Print data to console for verification
        print(f"Data for {ticker}:")
        print(f"Price Change: {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100:.2f} %")
        print(f"Beta Value: {stock.info.get('beta', 'Data ej tillgänglig')}")
        print(f"Lowest Price: {hist['Low'].min()}")
        print(f"Highest Price: {hist['High'].max()}")
        
        return result
    except Exception as e:
        return f"Ett fel uppstod vid hämtning av data: {str(e)}"

def rank_stocks_by_beta(aktier):
    beta_values = {}
    for ticker in aktier.keys():
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            beta = info.get('beta', None)  # None is the default value if nothing is found
            if beta is not None:
                stock_name = info.get('longName', 'Okänd') 
                beta_values[stock_name] = beta  # Create a dictionary with beta values
        except Exception as e:
            return f"Ett fel uppstod vid hämtning av data för {ticker}: {str(e)}"

    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1], reverse=True)  # Sort beta values from the list above
    result = "-------------Rangordning av aktier med avseende på betavärde-------------\n\n"
    for name, beta in sorted_stocks:
        result += f"{name}: Beta-värde = {beta}\n"  # Format the result nicely
        
        # Print data to console for verification
        print(f"Stock: {name}, Beta: {beta}")
    
    return result

# --------------GUI part-----------------------
class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root 
        self.root.title("Stock Analyzer")  # Window title

        self.create_widgets()  # Create GUI components; like buttons etc.

    def create_widgets(self):
        main_frame = tk.Frame(self.root)  # Create main frame widget where other widgets can be placed
        main_frame.grid(row=0, column=0, padx=10, pady=10)  # Create padding around main frame (10 pixels)

        menu_frame = tk.Frame(main_frame)  # Menu frame
        menu_frame.grid(row=0, column=0, padx=10, pady=10)  # Place menu frame in row 0, column 0

        self.menu_label = tk.Label(menu_frame, text="Välj analys:")  # Menu label widget where the user will choose options
        self.menu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')  # Place in row 0, column 0, align to west (left)

        self.analysis_type = ttk.Combobox(menu_frame, values=["Fundamental analys", "Teknisk analys", "Rangordning av betavärde"])  # Create a dropdown menu with options for the user to click
        self.analysis_type.grid(row=0, column=1, padx=10, pady=5)
        self.analysis_type.current(0)  # Default to "Fundamental analys"

        self.stock_label = tk.Label(menu_frame, text="Välj aktie:")  # Create label "Välj aktie"
        self.stock_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')  # One row below "Välj analys"

        self.stocks = {'ERIC-B.ST': 'Ericsson', 'ELUX-B.ST': 'Electrolux', 'AZN.ST': 'AstraZeneca'}  # Dictionary mapping their ticker symbols
        self.stock_choice = ttk.Combobox(menu_frame, values=list(self.stocks.values()))  # Dropdown menu with stocks to choose from
        self.stock_choice.grid(row=1, column=1, padx=10, pady=5)
        self.stock_choice.current(0)  # Default value = Ericsson

        self.analyze_button = tk.Button(menu_frame, text="Analysera", command=self.perform_analysis)  # Create an analyze button; when clicked, it will execute the method perform_analysis
        self.analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.quit_button = tk.Button(menu_frame, text="Avsluta", command=self.root.quit)  # Create a quit button; when clicked, it will close the program
        self.quit_button.grid(row=3, column=0, columnspan=2, pady=10)  # Place the quit button below the analyze button

        result_frame = tk.Frame(main_frame)  # Create a result frame within the main frame
        result_frame.grid(row=1, column=0, padx=10, pady=10)

        self.result_text = tk.Text(result_frame, height=20,)
