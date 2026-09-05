sender="toshibabadrr@gmail.com"
password= ""


import pandas
import smtplib
import datetime

class Reservation:
    def __init__(self,customer_name,customer_number,customer_email,flight_id,seats=1):
        self.customer_name=customer_name
        self.customer_number=customer_number
        self.customer_email=customer_email
        self.flight_id=flight_id
        self.seats=seats
        self.flight_info=None

    def reserve_flight(self):
        data=pandas.read_csv(r"D:\Maryam\Python NTI\NTI Project\Data\flights.csv")

        if self.seats<=0:
            print("number of seats must be greater than 0")
            return False

        flight_exists=False

        for x in range(len(data)):
            if data["flight_id"][x]==self.flight_id:
                flight_exists=True
                available=data["available_seats"][x]

                if available<self.seats:
                    print("sorry, not enough available seats")
                    return False

                new_seats=[]
                for y in range(len(data)):
                    if y==x:
                        new_seats.append(available-self.seats)
                    else:
                        new_seats.append(data["available_seats"][y])

                data["available_seats"]=new_seats

                self.flight_info={
                    "from":data["from"][x],
                    "to":data["to"][x],
                    "date":data["date"][x],
                    "day":data["day"][x],
                    "departure_time":data["departure_time"][x],
                    "arrival_time":data["arrival_time"][x],
                    "gate":data["gate"][x],
                    "terminal":data["terminal"][x],
                    "price":data["price"][x]
                }
                break

        if flight_exists==False:
            print("flight not found")
            return False

        data.to_csv(r"D:\Maryam\Python NTI\NTI Project\Data\flights.csv",index=False)

        return True

    def save_reservation(self):
        today=datetime.date.today()

        with open(r"D:\Maryam\Python NTI\NTI Project\Data\reservations.csv","a") as file:
            file.write(f"{self.customer_name},{self.customer_number},{self.customer_email},{self.flight_id},{self.flight_info['from']},{self.flight_info['to']},{self.flight_info['date']},{self.seats},{today}\n")

    def create_confirmation(self):
        with open("confirmation.txt","r") as file:
            message=file.read()

        message=message.replace("CUSTOMER_NAME",str(self.customer_name))
        message=message.replace("FLIGHT_ID",str(self.flight_id))
        message=message.replace("FROM",str(self.flight_info["from"]))
        message=message.replace("TO",str(self.flight_info["to"]))
        message=message.replace("DATE",str(self.flight_info["date"]))
        message=message.replace("DAY",str(self.flight_info["day"]))
        message=message.replace("DEPARTURE_TIME",str(self.flight_info["departure_time"]))
        message=message.replace("ARRIVAL_TIME",str(self.flight_info["arrival_time"]))
        message=message.replace("GATE",str(self.flight_info["gate"]))
        message=message.replace("TERMINAL",str(self.flight_info["terminal"]))
        message=message.replace("SEATS",str(self.seats))
        message=message.replace("PRICE",str(self.flight_info["price"]))

        return message

    def send_email(self,message):


        with smtplib.SMTP("smtp.gmail.com",port=587) as connection:
            connection.starttls()
            connection.login(user=sender,password=password)
            connection.sendmail(
                from_addr=sender,
                to_addrs=self.customer_email,
                msg=f"Subject: Flight Reservation Confirmation\n\n{message}"
            )

    def make_reservation(self):
        success=self.reserve_flight()

        if success==True:
            self.save_reservation()
            message=self.create_confirmation()
            self.send_email(message)
            print("reservation successful, confirmation email sent!")
        else:
            print("reservation failed")