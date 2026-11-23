class Asset: 
    def __init__(self, ticker, name):
        self.ticker = ticker.strip().upper()
        self.issuer = name.strip()
       

    def __str__(self):
        return f"[Ticker:{self.ticker} | Name: {self.name}]"
