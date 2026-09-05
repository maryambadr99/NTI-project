import csv
from prettytable import PrettyTable


class Aircraft:
    def __init__(self,name,serial_number,model,status,capacity):
        self.name=name
        self.serial_number=serial_number
        self.model=model
        self.status=status
        self.capacity=capacity

    def display_info(self): 
        table = PrettyTable()
        table.field_names = [ "Name", "Serial Number", "Model", "Status", "Capacity" ] 
        table.add_row([ self.name, self.serial_number, self.model, self.status, self.capacity ])
        print(table)

def load_aircraft():
    flights = []
    with open(r"D:\Maryam\Python NTI\NTI Project\Data\aircraft.csv", "r") as file:
        contents = csv.reader(file)
        next(contents)
        for row in contents:
            if len(row) != 5:
                continue
            flights.append(
                Aircraft(row[0], row[1], row[2], row[3], row[4]))
    return flights

def store_aircraft(flights):
    with open(r"D:\Maryam\Python NTI\NTI Project\Data\aircraft.csv","w")as file:
        writer=csv.writer(file)
        writer.writerow(["name","serial_number","model","status","capacity"])
        for aircraft in flights:
            writer.writerow([aircraft.name, aircraft.serial_number, aircraft.model, aircraft.status, aircraft.capacity])

def display_all(flights):
    table = PrettyTable() 
    table.field_names = [ "Name", "Serial Number", "Model", "Status", "Capacity" ] 
    for aircraft in flights: table.add_row([ aircraft.name, aircraft.serial_number, aircraft.model, aircraft.status, aircraft.capacity ])
    print(table)

    
def search(flights):
    user=input("enter the aircraft name or its serial number").strip().upper()
    for aircraft in flights:
        if user==aircraft.name or user==aircraft.serial_number:
            aircraft.display_info()
            return aircraft
    print("sorry no flight with this name or serial number")
    return None

def edit_aircraft(flights):
    target_flights=search(flights)
    if target_flights:
        print("enter the name ,serial number,model,status,capacity or press enter to not change")
        new_name=input("enter the new name:")
        new_serial_number=input("enter the new serial number:")
        new_model=input("enter the new model")
        new_status=input("enter the new status:")
        new_capacity=input("enter the new capacity:")

        if new_name!="":
            target_flights.name=new_name
        if new_serial_number != "":
            target_flights.serial_number = new_serial_number
        if new_model != "":
            target_flights.model = new_model
        if new_status != "":
            target_flights.status = new_status
        if new_capacity != "":
            target_flights.capacity = new_capacity

        store_aircraft(flights)
        print("the data have changed successfully")
