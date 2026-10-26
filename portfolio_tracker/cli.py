from rich.console import Console
from rich.table import Table
from portfolio_tracker.service.asset_service import add_asset, assets, find_asset
from portfolio_tracker.service.portfolio_service import create_portfolio, portfolios, find_portfolio
from portfolio_tracker.service.transaction_service import add_transaction


console = Console()

MAIN_MENU = """
==== 
MAIN MENU 
====
1) Create Portfolio
2) View portfolios
3) Add asset
4) Deposit funds
5) Print Assets
6) Buy
7) View transactions 
0) Exit
"""
# helper function: any time you want to inforce thata the input is a number you use this 
# we can use this ask_number function that convert text into a number. 
def ask_number(prompt):
    while True:
        text = input(prompt).strip()
        # tell the interpreter what to do if an exception (error) happens
        try:
            return float(text)
        except ValueError:
            console.print(f"[yellow]'{text}' is not a number. Try again.[/yellow]")

def handle_create_porfolio():
    name = input("Portfolio name: ").strip()
    description = input("Porfolio description: ").strip()
    create_portfolio(name, description)

def handle_print_porfolios():
    if len(portfolios)== 0:
         console.print("[blue]No portfolios available[/blue]")
         return
    table = Table(title = "Porfolios")
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style= "white")

    for portfolio in portfolios.values():
        table.add_row(portfolio.name, portfolio.description)

    console.print(table)

def handle_print_assets():
    if len(assets)== 0:
         console.print("[blue]No assets available[/blue]")
         return

    table = Table(title = "All available assets")
    table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    table.add_column("Issuer", style= "white")

    for asset in assets.values():
        table.add_row(asset.ticker, asset.issuer)

    console.print(table)
    

def handle_add_asset():
    ticker = input("Ticker: ").strip()
    issuer = input("Issuer: ").strip()
    add_asset(ticker, issuer)

def deposit():
    amount= ask_number("Amount to deposit: ")
    console.print(f"The user decided to add {amount} to their balance...")

def handle_buy():
    #recorded as a transaction 
    portfolio = input("Portfolio: ").strip()
    ticker= input (" Ticker: ").strip()
    quantity = ask_number("Quantity: ")
    price = ask_number ("Purchase price: ")
    asset = find_asset(ticker)
    portfolio = find_portfolio(portfolio_name)
    add_transaction(portfolio, asset, "BUY", quantity, price)
    console.print(" Buy transaction completed")
    # two things can go wrong 1) no existing portfolio 2)no existin ticker 

def handle_print_transaction():
    if len(transaction)== 0:
         console.print("[blue]No transactions are available[/blue]")
         return

    table = Table(title = "transactions")
    table.add_column("Portfolio Name ", justify="right", style="cyan", no_wrap=True)
    table.add_column("Ticker", style= "white")
    table.add_column("side", style= "white")
    table.add_column("Price", style= "white")
    table.add_column("Quantity", style= "white")
    table.add_column("Datetime", style= "white")


    for transaction in transactions:
        table.add_row(transaction.portfolio.name, 
                        transaction.asset.ticker, 
                        transaction.side, 
                        transaction.price, 
                        transaction.quatity, 
                        transaction.datetime
        )

    console.print(table)




def run():
    while True:
        console.print(MAIN_MENU)
        user_input = ask_number("Choose an option: ")
        try:
        if user_input == 0:
            console.print("Thank you for choosing us!")
            break
        if user_input == 1:
            handle_create_porfolio()
        if user_input == 2:
            handle_print_porfolios()
        if user_input == 3:
            handle_add_asset()
        if user_input == 4:
            deposit()
        if user_input == 5:
             handle_print_assets()
        if user_input == 6:
            handle_buy()
        if user_input = 7:
            handle_print_transactions()
        except Exception as e:
            console.print(f"[red]{str(e)}[/red]")
