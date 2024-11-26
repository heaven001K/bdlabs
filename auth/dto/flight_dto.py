class FlightDTO:
    def __init__(self, flight_id, flight_number, departure_time, arrival_time, baggage_allowance):
        self.flight_id = flight_id
        self.flight_number = flight_number
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.baggage_allowance = baggage_allowance

    def to_dict(self):
        return {
            "flight_id": self.flight_id,
            "flight_number": self.flight_number,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "baggage_allowance": self.baggage_allowance
        }
