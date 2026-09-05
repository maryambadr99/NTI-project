import pandas
import Backend.reservation as reservation

data = pandas.read_csv("D:\Maryam\Python NTI\NTI Project\Data\flights.csv")
flight_list = data.to_dict(orient="records")


class customer():
    def __init__(self):
        self.name = "name"
        self.phone = "phone"
        self.email = "gmail"
        self.flight = pandas.read_csv("D:\Maryam\Python NTI\NTI Project\Data\flights.csv")

    def display_flight(self):
        print(self.flight)

    def search_flight(self):

        to = input("what country do you want to travel?").strip().lower()
        from1 = input("what country do you want to travel from?").strip().lower()
        flight_exist = "no"

        for flight in flight_list:
            if flight["to"].lower() == to and flight["from"].lower() == from1:
                flight_exist = "yes"
                print("\n this flight is available")
                print("flight ID:", flight["flight_id"])
                print("from:", flight["from"])
                print("to:", flight["to"])
                print("Date:", flight["date"])
                print("Day:", flight["day"])
                print("Departure time:", flight["departure_time"])
                print("Arrival time:", flight["arrival_time"])
                print("Gate:", flight["gate"])
                print("Available seats:", flight["available_seats"])
                print("price:", flight["price"])
                print("=======================================")
                
        if flight_exist == "no":
            print("this flight is not available")

    def reserve(self):

        self.name = input("please enter your name:")
        self.phone = input("please enter your phone:")
        self.email = input("please enter your email:")
        to = input("what country do you want to travel?").strip().lower()
        from1 = input("what country do you want to travel from?").strip().lower()
        flight_exist = "no"

        for flight in flight_list:
            if flight["to"].lower() == to and flight["from"].lower() == from1:
                flight_exist = "yes"
                print("\n this flight is available")
                print("flight ID:", flight["flight_id"])
                print("from:", flight["from"])
                print("to:", flight["to"])
                print("Date:", flight["date"])
                print("Day:", flight["day"])
                print("Departure time:", flight["departure_time"])
                print("Arrival time:", flight["arrival_time"])
                print("Gate:", flight["gate"])
                print("Available seats:", flight["available_seats"])
                print("price:", flight["price"])
                print("=======================================")
        if flight_exist == "no":
            print("this flight is not available")

        else:
            flight_id = int(input("please enter your flight ID:"))
            seats = int(input("How many seats do you want ?:"))

            while seats <= 0:
                print("sorry:invalid")
                seats = int(input(" please enter a true seats?:"))

            reservation_obj = reservation.Reservation(self.name, self.phone, self.email, flight_id, seats)
            reservation_obj.make_reservation()

    def menu(self):
        while True:
            print("1. display flight")
            print("2. search")
            print("3. reserve")
            print("4. exit")
            choice = input("please enter your choice:")
            if choice == "1":
                self.display_flight()
            elif choice == "2":
                self.search_flight()
            elif choice == "3":
                self.reserve()
            elif choice == "4":
                break
            else:
                print("invalid choice")

