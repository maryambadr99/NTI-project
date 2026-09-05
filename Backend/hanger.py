import csv
from prettytable import PrettyTable

class Hanger:
    def __init__(self, hanger, aircraft, status):
        self.hanger = hanger
        self.aircraft = aircraft
        self.status = status

    def show_info(self):
        table = PrettyTable()
        table.field_names = [ "Hanger", "Aircraft", "Status" ] 
        table.add_row([ self.hanger, self.aircraft, self.status ]) 
        print(table)
        
def get_aircraft_info(serial_number):
    try:
        with open(r"D:\Maryam\Python NTI\NTI Project\Data\aircraft.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["serial_number"] == serial_number:
                    print(f"Aircraft: {row['name']} , Model: {row['model']} , Status: {row['status']}")
                    return
    except FileNotFoundError:
        print("Aircraft file not found")

def show_hangers():
    try:
        with open(r"D:\Maryam\Python NTI\NTI Project\Data\hangers.csv", "r") as file:
            reader = csv.DictReader(file)
            print("Hangers")
            for row in reader:
                hanger = Hanger(row["Hanger"], row["Aircraft"], row["Status"])
                hanger.show_info()
                if row["Status"] == "Occupied":
                    get_aircraft_info(row["Aircraft"])
    except FileNotFoundError:
        print("Hangers not found")


def search_hanger(hanger_num):
    try:
        with open(r"D:\Maryam\Python NTI\NTI Project\Data\hangers.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Hanger"] == hanger_num:
                    hanger = Hanger(
                        row["Hanger"], row["Aircraft"], row["Status"]
                    )
                    hanger.show_info()
                    if row["Status"] == "Occupied":
                        get_aircraft_info(row["Aircraft"])
                    return
            print("Hanger not found")
    except FileNotFoundError:
        print("Hangers not found")

def check_hanger(hanger_num):
    try:
        with open(r"D:\Maryam\Python NTI\NTI Project\Data\hangers.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["Hanger"] == hanger_num:
                    if row["Status"].strip().lower() == "occupied":
                        print("Hanger is occupied")
                        get_aircraft_info(row["Aircraft"])
                    else:
                        print("Hanger is empty")
                    return
            print("Hanger not found")
    except FileNotFoundError:
        print("Hangers not found")

        
def hanger_menu():
    while True:
        print("Hanger Menu")
        print("1.Show Hangers")
        print("2.Search Hanger")
        print("3.Check Hanger")
        print("4.Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            show_hangers()
        elif choice == "2":
            number = input("Enter hanger number: ")
            search_hanger(number)
        elif choice == "3":
            number = input("Enter hanger number: ")
            check_hanger(number)
        elif choice == "4":
            break
        else:
            print("Invalid choice")
