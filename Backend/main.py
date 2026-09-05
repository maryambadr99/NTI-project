from Backend.customer2 import customer
from Backend.admin import check_admin
from os import system


def main():
    
    while True:

        print("\n========== AIRPORT SYSTEM ==========")
        print("1. Customer")
        print("2. Admin")
        print("3. Exit")

        mode = input("Enter your mode: ")

        if mode == "1":
            customer1 = customer()
            system("cls")
            customer1.menu()

        elif mode == "2":
            check_admin()

        elif mode == "3":
            break

        else:
            print("Invalid choice")


main()