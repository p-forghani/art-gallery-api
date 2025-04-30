from src.app.models import Currency


def initialize_currencies(app, db):
    '''
    Initialize the IRR, USD, CAD, EUR currencies in the Currency table
    '''
    currencies = [
        {"id": 1, "title": "Euro", "symbol": "€", "code": "EUR"},
        {"id": 2, "title": "United States Dollar",
         "symbol": "$", "code": "USD"},
        {"id": 3, "title": "Canadian Dollar", "symbol": "C$", "code": "CAD"},
        {"id": 4, "title": "Iranian Rial", "symbol": "﷼", "code": "IRR"},
        {"id": 5, "title": "Toman", "symbol": "تومان", "code": "TOMAN"},
        {"id": 7, "title": "Pound Sterling", "symbol": "£", "code": "GBP"},
        {"id": 8, "title": "Yen", "symbol": "¥", "code": "JPY"},
        {"id": 9, "title": "Ruble", "symbol": "₽", "code": "RUB"},
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
                    symbol=currency["symbol"],
                    code=currency["code"],
                )
                db.session.add(new_currency)
        db.session.commit()
        print("Currencies initialized successfully.")
