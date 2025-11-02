import requests
import tkinter as tk
from tkinter import ttk, messagebox

# Din API-nyckel för FinancialModelingPrep
api_key = '70xcvZzSqorh01dv2Osg9fEimvs01VFr'

# Funktion för att hämta data från FMP
def get_fmp_data(endpoint, params=None):
    base_url = f'https://financialmodelingprep.com/api/v3/{endpoint}'
    if not params:
        params = {}
    params['apikey'] = api_key
    response = requests.get(base_url, params=params)
    return response.json()

def fundamental_analysis(ticker):
    try:
        profile = get_fmp_data(f'profile/{ticker}')
        if not profile:
            return "Data ej tillgänglig"

        result = f"-------------Fundamental analys för {profile[0]['companyName']}-------------\n\n"

        # P/E-tal
        pe_tal = profile[0].get('priceEarningsRatio', 'Data ej tillgänglig')
        result += f"P/E-tal: {pe_tal}\n"

        # P/S-tal
        ps_tal = profile[0].get('priceToSalesRatioTTM', 'Data ej tillgänglig')
        result += f"P/S-tal: {ps_tal}\n"

        # Soliditet
        soliditet = calculate_soliditet(ticker)
        result += f"Soliditet: {soliditet} %\n"

        return result
    except Exception as e:
        return f"Ett fel uppstod vid hämtning av data: {str(e)}"

def calculate_soliditet(ticker):
    try:
        balance_sheet = get_fmp_data(f'balance-sheet-statement/{ticker}', {'limit': 1})
        if not balance_sheet:
            return 'Data ej tillgänglig'

        total_assets = balance_sheet[0].get('totalAssets', 0)
        total_equity = balance_sheet[0].get('totalStockholdersEquity', 0)

        if total_assets != 0:
            soliditet = (total_equity / total_assets) * 100
            return round(soliditet, 2)
        else:
            return 'Data ej tillgänglig'
    except Exception as e:
        return f"Ett fel uppstod vid beräkning av soliditet: {str(e)}"

def technical_analysis(ticker):
    try:
        historical_data = get_fmp_data(f'historical-price-full/{ticker}', {'timeseries': 30})
        if not historical_data or 'historical' not in historical_data:
            return "Data ej tillgänglig"

        hist = historical_data['historical']
        result = f"-------------Teknisk analys för {ticker}-------------\n\n"
        result += f"Kursutveckling (30 senaste dagarna): {((hist[0]['close'] - hist[-1]['close']) / hist[-1]['close']) * 100:.2f} %\n"
        result += f"Lägsta kurs (30 senaste dagarna): {min(day['low'] for day in hist)}\n"
        result += f"Högsta kurs (30 senaste dagarna): {max(day['high'] for day in hist)}\n"

        # Hämta företagets profil för beta
        profile = get_fmp_data(f'profile/{ticker}')
        beta = profile[0].get('beta', 'Data ej tillgänglig')
        result += f"Betavärde: {beta}\n"

        return result
    except Exception as e:
        return f"Ett fel uppstod vid hämtning av data: {str(e)}"

def rank_stocks_by_beta(aktier):
    beta_values = {}
    for ticker in aktier.keys():
        try:
            profile = get_fmp_data(f'profile/{ticker}')
            beta = profile[0].get('beta', None)
            if beta is not None:
                stock_name = profile[0].get('companyName', 'Okänd')
                beta_values[stock_name] = beta
        except Exception as e:
            return f"Ett fel uppstod vid hämtning av data för {ticker}: {str(e)}"

    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1], reverse=True)
    result = "-------------Rangordning av aktier med avseende på betavärde-------------\n\n"
    for name, beta in sorted_stocks:
        result += f"{name}: Beta-värde = {beta}\n"

    return result

# --------------GUI-del-----------------------
class StockAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Analyzer")

        self.create_widgets()

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.grid(row=0, column=0, padx=10, pady=10)

        menu_frame = tk.Frame(main_frame)
        menu_frame.grid(row=0, column=0, padx=10, pady=10)

        self.menu_label = tk.Label(menu_frame, text="Välj analys:")
        self.menu_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.analysis_type = ttk.Combobox(menu_frame, values=["Fundamental analys", "Teknisk analys", "Rangordning av betavärde"])
        self.analysis_type.grid(row=0, column=1, padx=10, pady=5)
        self.analysis_type.current(0)

        self.stock_label = tk.Label(menu_frame, text="Välj aktie:")
        self.stock_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.stocks = {'ERIC-B.ST': 'Ericsson', 'ELUX-B.ST': 'Electrolux', 'AZN.ST': 'AstraZeneca'}
        self.stock_choice = ttk.Combobox(menu_frame, values=list(self.stocks.values()))
        self.stock_choice.grid(row=1, column=1, padx=10, pady=5)
        self.stock_choice.current(0)

        self.analyze_button = tk.Button(menu_frame, text="Analysera", command=self.perform_analysis)
        self.analyze_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.quit_button = tk.Button(menu_frame, text="Avsluta", command=self.root.quit)
        self.quit_button.grid(row=3, column=0, columnspan=2, pady=10)

        result_frame = tk.Frame(main_frame)
        result_frame.grid(row=1, column=0, padx=10, pady=10)

        self.result_text = tk.Text(result_frame, height=20, width=60, wrap='word')
        self.result_text.grid(row=0, column=0)

    def perform_analysis(self):
        analysis_type = self.analysis_type.get()
        stock_name = self.stock_choice.get()
        ticker = [key for key, value in self.stocks.items() if value == stock_name][0]

        self.result_text.delete(1.0, tk.END)
        if analysis_type == "Fundamental analys":
            result = fundamental_analysis(ticker)
        elif analysis_type == "Teknisk analys":
            result = technical_analysis(ticker)
        elif analysis_type == "Rangordning av betavärde":
            result = rank_stocks_by_beta(self.stocks)

        self.result_text.insert(tk.END, result)

if __name__ == "__main__":
    root = tk.Tk()
    app = StockAnalyzerApp(root)
    root.mainloop()
