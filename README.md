# Investments-Portfolio-Tracker
An app that will allow user to track their portfolios investments, buy and sell assets, and look up performance metrics. 

# How to set up the environment? 
 You need to activate the virtual environment and then run this command `pip install -r requirements.txt` this is to guarantee your environment is all set up with the dependencies need to run the up smoothly in your local machine. 


# Package layout 
 Models
- asset.py: Represents an investment asset, storing its ticker and issuer/name.
- portfolio.py: Represents an investment portfolio, storing its description, positions, and realized gains.
- position.py: Represents an asset holding within a portfolio, storing its ticker, quantity, and average cost.
- transaction.py: Represents a buy or sell transaction, recording the portfolio, asset, transaction side, quantity, price, and date/time.
- cash_account.py: Represents the user's shared cash account and maintains its balance.
Services
- asset_service.py: Manages asset creation, duplicate prevention, and asset lookup.
- portfolio_service.py: Manages portfolio creation, selection, lookup, deletion, and portfolio summaries.
- price_service.py: Manages manually entered current prices for registered assets.
- cash_service.py: Manages cash deposits and provides access to the shared cash balance.
- transaction_service.py: Manages buying and selling assets, updating positions, cash balances, and realized gains/losses.
Errors
- base_error.py: Defines the base exception inherited by all custom application errors.
- asset_errors.py: Defines errors related to asset operations.
- portfolio_errors.py: Defines errors related to portfolio operations.
- transaction_errors.py: Defines errors related to buying and selling transactions.
- cash_errors.py: Defines errors related to cash deposits and balance operations.
Application
- cli.py: Handles user interaction, collects input, displays information, and calls the appropriate services.
- main.py: Configures application logging and starts the application.
- init.py: Marks directories as Python packages so their modules can be imported.

# The 5 decisions