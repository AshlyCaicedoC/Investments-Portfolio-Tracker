from portfolio_tracker.models.transaction import Transaction 

transactions = []

def add_transaction( portfolio, asset, quantity, side, price):
    transactions.append(Transaction(portfolio, asset, quantity, side, price))