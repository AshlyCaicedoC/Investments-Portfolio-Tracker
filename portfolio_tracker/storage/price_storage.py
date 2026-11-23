from portfolio_tracker.models.price import Price


def find_price(session, asset):
    # returns the stored price as a Decimal, or None if no price has been set yet
    price = session.get(Price, asset.id)
    if price is None:
        return None
    return price.price


def save_price(session, asset, value):
    # each asset has only one current price: update it if it exists, otherwise create it
    price = session.get(Price, asset.id)

    if price is None:
        session.add(Price(asset=asset, price=value))
    else:
        price.price = value
    