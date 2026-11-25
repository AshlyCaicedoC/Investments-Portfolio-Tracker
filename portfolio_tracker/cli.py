from rich.console import Console
from rich.table import Table
from decimal import Decimal, InvalidOperation

from portfolio_tracker.service.portfolio_service import (
    create_portfolio,
    view_all_portfolios,
    select_portfolio,
    view_selected_portfolio,
    get_portfolio_summary,
    delete_portfolio
)
from portfolio_tracker.service.cash_service import deposit_cash, get_cash_balance
from portfolio_tracker.service.price_service import set_price, get_price
from portfolio_tracker.service.transaction_service import buy, sell, list_transactions
from portfolio_tracker.errors.base_error import PortfolioTrackerError
from portfolio_tracker.service.asset_service import add_asset, find_asset, list_assets

console = Console()

MAIN_MENU = """
==== 
MAIN MENU 
====
1) Create Portfolio
2) View Portfolios
3) Select Portfolio
4) View Selected Portfolio
5) Delete Portfolio
6) Add Asset
7) Print Assets
8) Set Current Asset Price
9) Deposit Funds
10) View Cash Balance
11) Buy
12) Sell
13) View Transactions
0) Exit
"""
# helper function: any time you want to inforce thata the input is a number you use this 
# we can use this ask_number function that convert text into a number. 
def ask_number(prompt):
    while True:
        text = input(prompt).strip()
        # tell the interpreter what to do if an exception (error) happens
        try:
           number = Decimal(text)
        except InvalidOperation:
            console.print(f"[yellow]'{text}' is not a number. Try again![/yellow]")
            continue 

        if not number.is_finite():
            console.print(f"[yellow]'{text}' is not a valid number. Try again![/yellow]")
            continue

        return number

def handle_create_porfolio():
    name = input("Portfolio name: ").strip()
    description = input("Porfolio description: ").strip()
    create_portfolio(name, description)
    console.print(f"[green]Portfolio '{name}' created successfully![/green]")

def handle_select_portfolio():
    name = input("Portfolio name: ").strip()
    portfolio = select_portfolio(name)

    console.print(
        f"[green]Selected portfolio: {portfolio.name}[/green]")

def handle_print_portfolios():
    portfolios = view_all_portfolios()
    if len(portfolios) == 0:
        console.print("[blue]No portfolios available[/blue]")
        return

    table = Table(title="Portfolios")
    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")

    for portfolio in portfolios:
        table.add_row(portfolio.name, portfolio.description)

    console.print(table)

def handle_print_assets():
    assets= list_assets()
    if len(assets)== 0:
         console.print("[blue]No assets available[/blue]")
         return

    table = Table(title = "All available assets")
    table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
    table.add_column("Issuer", style= "white")

    for asset in assets:                       
        table.add_row(asset.ticker, asset.issuer)

    console.print(table)
    

def handle_add_asset():
    ticker = input("Ticker: ").strip()
    issuer = input("Issuer: ").strip()
    add_asset(ticker, issuer)
    console.print(f"[green]Asset {ticker.upper()} added successfully[/green]")

def deposit():
    amount= ask_number("Amount to deposit: ")
    deposit_cash(amount)
    console.print(f"[green]Deposited ${amount:,.2f}. New balance: ${get_cash_balance():,.2f}[/green]")

def handle_buy():
    ticker = input("Ticker: ").strip()
    quantity = ask_number("Quantity: ")
    price = ask_number("Purchase price: ")

    buy(ticker, quantity, price)

    console.print("[green]Buy transaction has been successfully completed![/green]") 

def handle_sell():
    ticker = input("Ticker: ").strip()
    quantity = ask_number("Quantity: ")
    price = ask_number("Selling price: ")

    realized_gain = sell(ticker, quantity, price)

    console.print(
        f"[green]Sell transaction completed. "
        f"Realized gain/loss: ${realized_gain}[/green]")

def handle_print_transactions():
    transactions= list_transactions()

    if len(transactions) == 0:
        console.print("[blue]No transactions are available[/blue]")
        return

    table = Table(title="Transactions")
    table.add_column("Portfolio Name")
    table.add_column("Ticker")
    table.add_column("Side")
    table.add_column("Price")
    table.add_column("Quantity")
    table.add_column("Datetime")

    for transaction in transactions:
        table.add_row(
            transaction.portfolio.name,
            transaction.asset.ticker,
            transaction.side,
            format_money(transaction.price_per_share),
            str(transaction.quantity),
            str(transaction.trade_date)
        )

    console.print(table)

def handle_view_cash_balance():
    balance = get_cash_balance()
    console.print(f"Available cash: {format_money(balance)}")

def handle_delete_portfolio():
    name = input("Portfolio name to delete: ").strip()
    delete_portfolio(name)
    console.print("[green]Portfolio deleted successfully[/green]")

def handle_set_price():
    ticker = input("Ticker: ").strip()
    price = ask_number("Current asset price: ")

    set_price(ticker, price)

    console.print(
        f"[green]Current price for {ticker.upper()} successfully updated![/green]"
    )

# helper function: shows money with 2 decimals, or N/A when there is no value yet
def format_money(value):
    if value is None:
        return "N/A"
    return f"${value:,.2f}"

def handle_view_selected_portfolio():
    summary = get_portfolio_summary()
    portfolio = summary["portfolio"]

    console.print(f"\n[bold cyan]Portfolio: {portfolio.name}[/bold cyan]")
    console.print(f"Description: {portfolio.description}")

    if len(summary["rows"]) == 0:
        console.print("[blue]This portfolio has no positions yet[/blue]")
    else:
        table = Table(title="Positions")
        table.add_column("Ticker", justify="right", style="cyan", no_wrap=True)
        table.add_column("Quantity", justify="right")
        table.add_column("Average Cost", justify="right")
        table.add_column("Current Price", justify="right")
        table.add_column("Market Value", justify="right")
        table.add_column("Unrealized Gain/Loss", justify="right")

        for row in summary["rows"]:
            table.add_row(
                row["ticker"],
                str(row["quantity"]),
                format_money(row["average_cost"]),
                format_money(row["current_price"]),
                format_money(row["market_value"]),
                format_money(row["unrealized_gain"])
            )

        console.print(table)

    console.print(f"Total market value: {format_money(summary['total_market_value'])}")
    console.print(f"Total unrealized gain/loss: {format_money(summary['total_unrealized_gain'])}")
    console.print(f"Realized gain/loss: {format_money(summary['realized_gain'])}")

def run():
    while True:
        console.print(MAIN_MENU)
        user_input = ask_number("Choose an option: ")
        try:
            if user_input == 0:
                console.print("Thank you for choosing us!")
                break
            elif user_input == 1:
                handle_create_porfolio()
            elif user_input == 2:
                handle_print_portfolios()
            elif user_input == 3:
                handle_select_portfolio()
            elif user_input == 4:
                handle_view_selected_portfolio()
            elif user_input == 5:
                handle_delete_portfolio()
            elif user_input == 6:
                handle_add_asset()
            elif user_input == 7:
                handle_print_assets()
            elif user_input == 8:
                handle_set_price()
            elif user_input == 9:
                deposit()
            elif user_input == 10:
                handle_view_cash_balance()
            elif user_input == 11:
                handle_buy()
            elif user_input == 12:
                handle_sell()
            elif user_input == 13:
                handle_print_transactions()
            else:
                console.print("[yellow]Invalid menu option.[/yellow]")
        except PortfolioTrackerError as e:
            console.print(f"[red]{str(e)}[/red]")
