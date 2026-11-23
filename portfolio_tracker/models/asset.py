class Asset: 
    def __init__(self, ticker, issuer):
        self.ticker = ticker.strip().upper()
        self.issuer = issuer.strip()
       

    def __str__(self):
        return f"[Ticker:{self.ticker} | Name: {self.issuer}]"
