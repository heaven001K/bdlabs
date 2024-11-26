class TicketDTO:
    def __init__(self, ticket_id, user_id, flight_id, purchase_date, price):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.flight_id = flight_id
        self.purchase_date = purchase_date
        self.price = price

    def to_dict(self):
        return {
            "ticket_id": self.ticket_id,
            "user_id": self.user_id,
            "flight_id": self.flight_id,
            "purchase_date": str(self.purchase_date),
            "price": str(self.price)
        }
