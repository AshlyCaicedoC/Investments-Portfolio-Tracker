# Investments-Portfolio-Tracker
An app that will allow user to track their portfolios investments, buy and sell assets, and look up performance metrics. 

# How to set up the environment? 
 You need to activate the virtual environment and then run this command `pip install -r requirements.txt` this is to guarantee your environment is all set up with the dependencies need to run the up smoothly in your local machine. After you have set this environment run `python -m portfolio_tracker.main` for macs run `python3 -m portfolio_tracker.main`.


# Package layout 
1. **Models**
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
2. **Errors**
- base_error.py: Defines the base exception inherited by all custom application errors.
- asset_errors.py: Defines errors related to asset operations.
- portfolio_errors.py: Defines errors related to portfolio operations.
- transaction_errors.py: Defines errors related to buying and selling transactions.
- cash_errors.py: Defines errors related to cash deposits and balance operations.
3. **Application**
- cli.py: Handles user interaction, collects input, displays information, and calls the appropriate services.
- main.py: Configures application logging and starts the application.
- init.py: Marks directories as Python packages so their modules can be imported.

# The 5 decisions


1. **Are fractional shares allowed?**
   Yes, this app is meant for both beginners and experienced investors, so fractional shares are allowed. Quantities and prices are stored as `Decimal` to avoid rounding errors in money calculations.

2. **Is `aapl` the same asset as `AAPL`?**
   Yes, the app converts every ticker to uppercase when it is added and when it is looked up, so `aapl` and `AAPL` all refer to the same asset. This keeps the data consistent and prevents duplicates. Portfolio names work the same way: they are matched without regard to upper or lowercase.

3. **Do fully sold positions still appear in the portfolio view?**
   No, once a position is fully sold, it is removed from the portfolio to avoid confusing the user. Its history is not lost: the buy and sell transactions still appear in View Transactions, and the gain or loss from the sale is kept in the portfolio's realized gain/loss.

4. **How does the portfolio view handle an asset with no current price set?**
   It does not crash. The position is still listed with its ticker, quantity and average cost, but Current Price, Market Value and Unrealized Gain/Loss show "N/A". Because the app cannot value that asset, it is left out of the Total Market Value and Total Unrealized Gain/Loss. Once the user sets a price (option 8), the asset is included.

5. **Which errors does the user see, and which are only written to the log?**
   - **Shown to the user:** errors caused by user actions, such as an unknown ticker or portfolio, a duplicate asset or portfolio, no portfolio selected, an invalid quantity or price, not enough cash, selling more shares than owned, or deleting a portfolio that still has positions. All of these inherit from `PortfolioTrackerError`; the CLI shows them in red and the app keeps running. Input that is not a valid number shows a yellow message and asks again.

   - **Written to the log:** mainly bugs. `main.py` writes the full technical details to `portfolio_tracker.log`, and the user only sees a short message saying the app has to close. The log also records when the app starts and stops and every price update.