# Investments-Portfolio-Tracker
An app that will allow user to track their portfolios investments, buy and sell assets, and look up performance metrics. 

# How to set up  and run the app?
 **Database set up**
To install MySQL run this command in tour terminal to install and start MySQL `brew install mysql`
`brew services start mysql`.
**Clone the repo and set up you local environment like this**
  1. You need to clone the repo from github to your local machine use this command in your vs code terminal `git clone https://github.com/AshlyCaicedoC/Investments-Portfolio-Tracker.git`. 
  2.  Change the working directory to the Investments-Portfolio-Tracker folder, use this command `cd Investments-Portfolio-Tracker`
  3. Create a virtual environment, use this command for mac `python3 -m venv .venv` and windows `python -m venv .venv`
  4. Activate the virtual environment `ource .venv/bin/activate`
  5. Run this command `pip install -r requirements.txt` this is to guarantee your environment is all set up with the dependencies need to run the up smoothly in your local machine. 
  6. Finally, after you have set this environment run  `python -m portfolio_tracker.main` for windows and for macs run `python3 -m portfolio_tracker.main`.

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

# How to run the tests

From the project folder, with the virtual environment active, write on mac `python3 -m pytest -v` and on windows `python -m pytest -v`. The `-v` (verbose) option lists every test by name with PASSED or FAILED next to it, instead of just a dot per test. The tests use their own in-memory database, so MySQL doesn't need to be running.


# How did Test work 

The empty_db fixture in conftest.py is a fixture that allows us to create an empty database for the tests to run on. conftest.py is a module that pytest always opens before the tests start. With this module and the fixtures in it, we guarantee that the tests never touch the database of the actual application, and we avoid tests having external dependencies.

One important fixture is monkeypatch, because this one in specific is what allows us to point to the in-memory database that is used to run the tests instead of the MySQL database(the real one).

Shared setup lives in fixtures. funded_portfolio and set_prices are fixtures that the tests for every service use. All the fixtures that are shared between the tests of each service are stored in conftest.py, so they can be used across all test functions.

A bug I introduced on purpose: while testing the `price_service` module, I changed the constraint on the price from `price < 0` to `price < -1000`. The test `test_negative_price_is_refused` failed, and the report said `FAILED tests/test_price_service.py::test_negative_price_is_refused - Failed: DID NOT RAISE InvalidPriceError`. This happened because the price constraint was altered, and it let negative prices be passed to the app. 

# Decisions


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

6. **Are current prices stored in the database, or kept in memory and re-entered each run?**
There is no reason to store the current prices, because every time a user enters a price, he or she will be able to calculate the market value and unrealized gain from the price they entered in the session they are in. As for holdings, the price per share is stored in the transactions table, so the metrics related to it can be calculated from there. This is the reason why the prices are kept in memory.

7. **How many decimal places do you store for cash, share quantities, and prices, and what does that mean for rounding? For example, what happens to the cash balance when someone buys 3 shares at $33.3333?**
For cash 2 decimal places, for share quantities 4, and for prices 4. Cash has 2 because money is paid in cents, and quantities and prices have 4 so fractional shares and small prices can be saved exactly. All the calculations are done with `Decimal`, so there are no rounding errors while the app is calculating.

Before the cash changes, the cost of the trade is rounded to the nearest cent, the same way a broker does it. For example, if a user has $10,000.00 and buys 3 shares at $33.3333, the trade costs $99.9999, which is rounded to $100.00, so the cash goes down to $9,900.00. The transaction still saves the exact quantity and price. This was done to guarantee that the cash always changes in whole cents, and it is a way to make sure the cash and the transactions match.

8. **Which of your business rules does the database itself enforce, in addition to the checks in your Python code, and why those?**
Quantities have to be greater than 0, the price per share cannot be negative, and the balance cannot be negative. The database checks act like the last line of defense, so when wrong data enters the system it can be stopped, and this prevents the system from breaking.