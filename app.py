# from flask import Flask, request, render_template, redirect, url_for
# import yfinance as yf
# import pandas as pd
# import os

# app = Flask(__name__)

# # Path to the CSV file
# DATA_FILE = 'data/stock_data.csv'

# # Helper functions
# def fetch_latest_price(ticker):
#     stock = yf.Ticker(ticker)
#     latest_price = stock.history(period="1d")['Close'].iloc[-1]
#     return latest_price

# def calculate_returns(purchase_price, latest_price):
#     return ((latest_price - purchase_price) / purchase_price) * 100

# def calculate_portfolio_return(stocks_data):
#     total_investment = sum(stock['purchase_price'] * stock['shares'] for stock in stocks_data)
#     total_current_value = sum(stock['latest_price'] * stock['shares'] for stock in stocks_data)
#     portfolio_return = ((total_current_value - total_investment) / total_investment) * 100
#     return portfolio_return

# def load_data():
#     if os.path.exists(DATA_FILE):
#         try:
#             return pd.read_csv(DATA_FILE).to_dict(orient='records')
#         except pd.errors.EmptyDataError:
#             return []
#     else:
#         return []

# def save_data(data):
#     df = pd.DataFrame(data)
#     os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
#     df.to_csv(DATA_FILE, index=False)

# # Routes
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         ticker = request.form['ticker']
#         purchase_price = float(request.form['purchase_price'])
#         shares = int(request.form['num_shares'])
        
#         latest_price = fetch_latest_price(ticker)
#         return_performance = calculate_returns(purchase_price, latest_price)
        
#         stock_data = load_data()
#         stock_data.append({
#             'ticker': ticker,
#             'purchase_price': purchase_price,
#             'shares': shares,
#             'latest_price': latest_price,
#             'return_performance': return_performance
#         })
#         save_data(stock_data)
#         return redirect(url_for('index'))
    
#     stock_data = load_data()
#     portfolio_return = calculate_portfolio_return(stock_data) if stock_data else 0
#     return render_template('index.html', stocks=stock_data, portfolio_return=portfolio_return)

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, redirect, url_for
import yfinance as yf
import pandas as pd
import os

app = Flask(__name__)

# Path to the CSV file
DATA_FILE = 'data/stock_data.csv'

# Helper functions
def fetch_latest_price(ticker):
    stock = yf.Ticker(ticker)
    latest_price = stock.history(period="1d")['Close'].iloc[-1]
    return latest_price

def calculate_returns(purchase_price, latest_price):
    return ((latest_price - purchase_price) / purchase_price) * 100

def calculate_portfolio_return(stocks_data):
    total_investment = sum(stock['purchase_price'] * stock['shares'] for stock in stocks_data)
    total_current_value = sum(stock['latest_price'] * stock['shares'] for stock in stocks_data)
    portfolio_return = ((total_current_value - total_investment) / total_investment) * 100
    return portfolio_return

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE).to_dict(orient='records')
        except pd.errors.EmptyDataError:
            return []
    else:
        return []

def save_data(data):
    df = pd.DataFrame(data)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    df.to_csv(DATA_FILE, index=False)

def delete_stock(ticker):
    stock_data = load_data()
    stock_data = [stock for stock in stock_data if stock['ticker'] != ticker]
    save_data(stock_data)

# Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ticker = request.form['ticker']
        purchase_price = float(request.form['purchase_price'])
        shares = int(request.form['num_shares'])
        
        latest_price = fetch_latest_price(ticker)
        return_performance = calculate_returns(purchase_price, latest_price)
        
        stock_data = load_data()
        stock_data.append({
            'ticker': ticker,
            'purchase_price': purchase_price,
            'shares': shares,
            'latest_price': latest_price,
            'return_performance': return_performance
        })
        save_data(stock_data)
        return redirect(url_for('index'))
    
    stock_data = load_data()
    portfolio_return = calculate_portfolio_return(stock_data) if stock_data else 0
    return render_template('index.html', stocks=stock_data, portfolio_return=portfolio_return)

@app.route('/delete', methods=['POST'])
def delete():
    ticker = request.form['ticker']
    delete_stock(ticker)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
