from src.app.models import Currency


def initialize_currencies(app, db):
    '''
    Initialize the IRR, USD, CAD, EUR currencies in the Currency table
    '''
    currencies = [
        {"id": 1, "title": "Euro", "symbol": "EUR"},
        {"id": 2, "title": "United States Dollar", "symbol": "USD"},
        {"id": 3, "title": "Canadian Dollar", "symbol": "CAD"},
        {"id": 4, "title": "Iranian Rial", "symbol": "IRR"}
    ]
    with app.app_context():
        for currency in currencies:
            # Check if the currency exist
            existing_currency = Currency.query.filter_by(
                title=currency["title"]
            ).first()
            if not existing_currency:
                # Create the currency if it doesn't exist
                new_currency = Currency(
                    id=currency["id"],
                    title=currency["title"],
                    symbol=currency["symbol"]
                )
                db.session.add(new_currency)
                print(
                    f"Added currency: {currency['title']} "
                    f"with symbol {currency['symbol']}"
                )
            else:
                print(
                    f"Currency already exists: "
                    f"{currency['title']} with symbol {currency['symbol']}"
                )
        db.session.commit()
        print("Currencies initialized successfully.")
