import csv,pandas
from os import system
from prettytable import PrettyTable
from Backend.AIRCRAFTS import load_aircraft, display_all, search, edit_aircraft
from Backend.hanger import show_hangers, search_hanger, check_hanger

def check_admin():

    user = input("Please enter your username: ")
    password = input("Please enter your password: ")

    while True:

        found = False

        with open(r"D:\Maryam\Python NTI\NTI Project\Data\admins_pass.csv") as file:
            reader = csv.reader(file)

            for row in reader:
                users = row[0]
                passwords = row[1]

                if user == users and password == passwords:
                    found = True
                    system("cls")
                    admin_menu()

        if not found:
            print("Invalid username or password")
            user = input("Please enter your username: ")
            password = input("Please enter your password: ")

def admin_menu():
    while True:
        print("="*10, "ADMIN MENU", "="*10)
        choice = input("1.Display Aircrafts\n2.Manage Aircafts\n3.Display Hangers\n4.Search\n5.Exit\n")

        if choice == "1":
            aircrafts = load_aircraft()
            display_all(aircrafts)

        elif choice == "2":
            system("cls")
            aircrafts = load_aircraft()
            edit_aircraft(aircrafts)

        elif choice == "3":
             show_hangers()

        elif choice == "4":
            search_admin()

        elif choice == "5":
            print("Thanks for using!")
            return

        else:
            system("cls")
            print("Invalid choice")

def search_admin():
    while True:
        choice = input("1.Search Aircrafts\n2.Search Hangers\n3.Exit\n").upper()

        if choice == "1":
            aircraft = load_aircraft()            
            search(aircraft)

        elif choice == "2":
            hanger_num = input("Enter hanger number: ")
            search_hanger(hanger_num)

        elif choice == "3":
            break

        elif choice == "VIP":
            secret_valid()

        else:
            system("cls")
            print("Invalid choice")

def secret_menu():
    while True:

        print("="*10, "SECRET MENU", "="*10)
        choice = input("1.Display labors info\n2.Report\n3.Exit\n")

        if choice == "1":
            labors()
            return

        elif choice == "2":
            system("cls")
            report()
            return

        elif choice == "3":
            break

        else:
            print("Invalid choice")

def secret_valid():
    code = input("Enter security code: ")

    if code == "NTI2026":
        print("="*30)
        print("        ACCESS APPROVED\n", "         VIP ACCESS")
        print("="*30)
        secret_menu()

    else:
        print("="*30)
        print("        ACCESS DENIED\n", "  SECURITY CODE UNAVAILABLE")
        print("="*30)

def labors():
    table = PrettyTable(["Labor ID", "Name", "Position", "Aircraft ID", "Clearance", "Status", "Specialization"])

    with open(r"D:\Maryam\Python NTI\NTI Project\Data\labors.csv", "r") as file:
        reader = csv.reader(file)

        for row in reader:
            table.add_row(row)

    print(table)

def report():
    aircrafts = pandas.read_csv(r"D:\Maryam\Python NTI\NTI Project\Data\aircraft.csv")
    labors_data = pandas.read_csv(r"D:\Maryam\Python NTI\NTI Project\Data\labors.csv")
    
    print("Total aircrafts:", len(aircrafts))
    print("Active aircrafts:", len(aircrafts[aircrafts["status"] == "Active"]))
    print("Maintenance aircrafts:", len(aircrafts[aircrafts["status"] == "Maintenance"]))
    print("Grounded aircrafts:", len(aircrafts[aircrafts["status"] == "Grounded"]))

    print("Total labors:", len(labors_data))
    print("Active labors:", len(labors_data[labors_data["Status"] == "Active"]))
    print("Labors on leave:", len(labors_data[labors_data["Status"] == "On Leave"]))

