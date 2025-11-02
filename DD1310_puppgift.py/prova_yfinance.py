import requests
from bs4 import BeautifulSoup
import yfinance as yf
import tkinter as tk
from tkinter import ttk, messagebox

def get_data_from_yahoo(ticker):
    url = f"https://finance.yahoo.com/quote/{ticker}/key-statistics/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = {
        "Forward P/E": "Data ej tillgänglig",
        "P/S Ratio": "Data ej tillgänglig"
    }

    try:
        forward_pe_section = soup.find(text="Forward P/E")
        if forward_pe_section:
            forward_pe = forward_pe_section.find_next("td").text.strip()
            data["Forward P/E"] = forward_pe

        ps_ratio_section = soup.find(text="Price/Sales")
        if ps_ratio_section:
            ps_ratio = ps_ratio_section.find_next("td").text.strip()
            data["P/S Ratio"] = ps_ratio

    except Exception as e:
        print(f"Error scraping data from Yahoo Finance: {str(e)}")

    print(f"Fetched data from Yahoo Finance: {data}")
    return data

def fundamental_analysis(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        result = f"-------------Fundamental analys för {info.get('longName', ticker)}-------------\n\n"

        # Use the get_data_from_yahoo function to fetch data
        yahoo_data = get_data_from_yahoo(ticker)
        forward_pe = yahoo_data.get("Forward P/E", "Data ej tillgänglig")
        ps_tal = yahoo_data.get("P/S Ratio", "Data ej tillgänglig")
        
        result += f"Forward P/E-tal: {forward_pe}\n"
        result += f"P/S-tal: {ps_tal}\n"

        # Calculating Solvency Ratio
        equity = info.get('totalStockholderEquity', None)
        total_assets = info.get('totalAssets', None)
        untaxed_reserves = info.get('undistributedReserve', 0)  # If available, otherwise use 0
        tax_rate = 0.22  # Assuming a 22% tax rate

        if equity is not None and total_assets is not None:
            adjusted_equity = equity + (untaxed_reserves * (1 - tax_rate))
            solvency_ratio = (adjusted_equity / total_assets) * 100
            result += f"Soliditet: {solvency_ratio:.2f}%\n"
        else:
            result += "Soliditet: Data ej tillgänglig\n"

        return result
    except Exception as e:
        return f"Ett fel uppstod vid hämtning av data: {str(e)}"

def technical_analysis(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period="1mo")
        result = f"-------------Teknisk analys för {stock.info.get('longName', ticker)}-------------\n\n"
        result += f"Kursutveckling (30 senaste dagarna): {((hist['Close'].iloc[-1] - hist['Close'].iloc[0]) / hist['Close'].iloc[0]) * 100:.2f} %\n"
        result += f"Betavärde: {stock.info.get('beta', 'Data ej tillgänglig')}\n"
        result += f"Lägsta kurs (30 senaste dagarna): {hist['Low'].min()}\n"
        result += f"Högsta kurs (30 senaste dagarna): {hist['High'].max()}\n"

        return result
    except Exception as e:
        return f"Ett fel uppstod vid hämtning av data: {str(e)}"

def rank_stocks_by_beta(aktier):
    beta_values = {}
    for ticker in aktier.keys():
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            beta = info.get('beta', None)
            if beta is not None:
                stock_name = info.get('longName', 'Okänd')
                beta_values[stock_name] = beta
        except Exception as e:
            return f"Ett fel uppstod vid hämtning av data för {ticker}: {str(e)}"

    sorted_stocks = sorted(beta_values.items(), key=lambda item: item[1], reverse=True)
    result = "-------------Rangordning av aktier med avseende på betavärde-------------\n\n"
    for name, beta in sorted_stocks:
        result += f"{name}: Beta-värde = {beta}\n"

    return result

# --------------GUI part-----------------------
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
