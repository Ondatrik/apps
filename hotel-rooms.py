import pandas as pd
from datetime import datetime


# the function prints the Menu options, requests user's choice and returns it
def menu():
    print("\nMENU")
    print("A. Check for available rooms")
    print("B. Allot a room")
    print("C. Update occupancy for existing customer")
    print("D. Display occupied rooms")
    print("E. Checkout a customer")
    print("F. Write updates to a file")
    print("Q. Quit application")
    choice = input("\nSelect choice: ")
    print("\n")
    return choice


# The function downloads information about the current room occupancy from Excel file in current directory
# and creates a global variable "rooms"
def load_rooms():
    global rooms
    rooms = pd.read_excel("hotel_room_occupancy.xlsx")
    rooms = rooms.set_index("Room_No")


# The function returns a global variable available_rooms,
# which is called in the below functions check_rooms() and allot_room()
def free_rooms():
    global available_rooms
    available_rooms = rooms[rooms["Name"] == "Not Occupied"]
    return available_rooms


# The function returns a global variable occupied_rooms, which is called in the below functions update_occupancy(),
# display_occupied() and checkout()
def occupied_rooms():
    global occupied_rooms
    occupied_rooms = rooms[rooms['Name'] != "Not Occupied"]
    return occupied_rooms


# The function displays all the available rooms
def check_rooms():
    free_rooms()
    print(available_rooms.to_string(index=True))


# The function allows the user to allot a not occupied room
# It accepts a room number as an input and checks it against a list of the currently available rooms
# Also, it requests data for allotment (Name of the guest, date occupancy and days of occupancy)
# and updates rooms dataframe
# Finally, the function handles two types of errors - ValueError and TypeError
def allot_room():
    done = False
    while not done:
        try:
            to_allot = int(input("Room number: "))
            current_free_rooms = list(free_rooms().index)
            if to_allot in current_free_rooms:
                name = input("Name: ")
                date = input("Date of occupancy (in format yyyy-mm-dd): ").split('-')
                allot_date = []
                for i in date:
                    i = int(i)
                    allot_date.append(i)
                allot_date = datetime(*allot_date)  # datetime unction does not accept list, only integers.
                # That's why I pass values of the list allot_date within the function
                days = int(input("Days of Occupancy: "))
                rooms.loc[to_allot, ["Name", "Date_Occupancy", "Days_Occupancy"]] = [name, allot_date, days]
                print(f"The room {to_allot} is alloted successfully!")
                print(rooms.loc[to_allot, :].to_string(index=True))
            else:
                print(f"The room number {to_allot} is not available for allotment")
            done = True
        except ValueError:
            print("Please insert data in the correct format")
        except TypeError:  # TypeError occurs when accepting customer input in the date variable
            print("Please insert data in the correct format")


# The function updates the number of stay days for the existing guest
# It handles ValueErrors and raise a custom Error if a user inserts number of days <=0

def update_occupancy():
    done = False
    while not done:
        try:
            to_update = int(input("Room number: "))
            current_occ_rooms = list(occupied_rooms().index)

            if to_update in current_occ_rooms:
                new_days = int(input("New number of days: "))
                if new_days <= 0:
                    raise Exception("New number of days should be more than 0")
                else:
                    rooms.loc[to_update, "Days_Occupancy"] = new_days
                    print(f"The number of stay days for the room {to_update} is updated.")
                    print(rooms.loc[to_update, :])
            else:
                print(f"The room {to_update} is not occupied.")
            done = True
        except ValueError:
            print("Please insert data in the correct format")
        except Exception:
            print("New number of days should be more than 0")


# The function displays the list of occupied rooms along with the customer name
def display_occupied():
    occupied_rooms()
    print(occupied_rooms["Name"].to_string(index=True))


# The function allows a user to check out a customer
# It accepts a room number as an input, checks it against a list of the currently occupied rooms
# and resets the room information to the default settings
# It also handles ValueErrors
def checkout():
    columns = ["Name", "Date_Occupancy", "Days_Occupancy"]
    default_date = datetime(2022, 1, 1)
    default_values = ["Not Occupied", default_date, 0]

    done = False
    while not done:
        try:
            to_checkout = int(input("Room number: "))
            current_occ_rooms = list(occupied_rooms().index)
            if to_checkout in current_occ_rooms:
                rooms.loc[to_checkout, columns] = default_values
                print(f"The customer successfully vacated the room number {to_checkout}!")
                print(rooms.loc[to_checkout, :])
            else:
                print(f"The room {to_checkout} is not occupied.")
            done = True
        except ValueError:
            print("Please insert data in the correct format")


def write_updates():
    rooms.to_excel("out_hotel_room_occupancy.xlsx")
    print("The new file out_hotel_room_occupancy.xlsx was successfully saved to the current directory")


# main
# Load the current information from a file
load_rooms()

# Menu flow with user's choice

user_choice = 'N'

while user_choice != 'Q' and user_choice != 'q':
    if user_choice == 'A' or user_choice == 'a':
        check_rooms()
    elif user_choice == 'B' or user_choice == 'b':
        allot_room()
    elif user_choice == 'C' or user_choice == 'c':
        update_occupancy()
    elif user_choice == 'D' or user_choice == 'd':
        display_occupied()
    elif user_choice == 'E' or user_choice == 'e':
        checkout()
    elif user_choice == 'F' or user_choice == 'f':
        write_updates()
    else:
        pass
    user_choice = menu()
