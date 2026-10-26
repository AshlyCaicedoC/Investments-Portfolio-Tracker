class Asset: 
    def __init__(self, ticker, issuer):
        self.ticker = ticker
        self.issuer = issuer

    def __str__(self):
        return f"[Ticker:{self.ticker} | Issuer: {self.issuer}]"