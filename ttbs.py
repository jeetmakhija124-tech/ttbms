trains = []
bookings = []


def add_train():
    print("\n--- Add Train ---")
    name = input("Enter train name: ")
    from_location = input("Enter departure station: ")
    to_location = input("Enter arrival station: ")
    date = input("Enter date (DD/MM/YYYY): ")
    time = input("Enter departure time (HH:MM AM/PM): ")
    seats = int(input("Enter total seats: "))
    price = float(input("Enter price per seat (INR): "))

    train = {
        "id": len(trains) + 1,
        "name": name,
        "from_location": from_location,
        "to_location": to_location,
        "date": date,
        "time": time,
        "total_seats": seats,
        "booked_seats": 0,
        "price": price
    }
    trains.append(train)
    print(f"Train '{name}' added from '{from_location}' to '{to_location}'!")


def view_trains():
    print("\n--- All Trains ---")
    if len(trains) == 0:
        print("No trains found.")
        return

    for t in trains:
        seats_left = t["total_seats"] - t["booked_seats"]
        print(f"\nID       : {t['id']}")
        print(f"Name     : {t['name']}")
        print(f"Route    : {t['from_location']} --> {t['to_location']}")
        print(f"Date     : {t['date']} at {t['time']}")
        print(f"Seats    : {seats_left} left")
        print(f"Price    : INR {t['price']:.2f}")
        print("-" * 30)


def book_ticket():
    print("\n--- Book Ticket ---")
    if len(trains) == 0:
        print("No trains available.")
        return

    view_trains()
    name = input("Enter your name: ")
    age = int(input("Enter your age: "))
    train_id = int(input("Enter Train ID to book: ")) - 1

    if train_id < 0 or train_id >= len(trains):
        print("Invalid Train ID.")
        return

    selected = trains[train_id]
    seats_left = selected["total_seats"] - selected["booked_seats"]

    if seats_left == 0:
        print("Sorry, this train is full!")
        return

    seats = int(input(f"How many seats? ({seats_left} left): "))

    if seats > seats_left:
        print(f"Only {seats_left} seat(s) available.")
        return

    total = seats * selected["price"]

    booking = {
        "id": len(bookings) + 1,
        "name": name,
        "age": age,
        "train_id": selected["id"],
        "train_name": selected["name"],
        "route": f"{selected['from_location']} --> {selected['to_location']}",
        "date": selected["date"],
        "time": selected["time"],
        "seats": seats,
        "total": total,
        "payment": "Pending"
    }
    bookings.append(booking)
    selected["booked_seats"] += seats

    print(f"\nTicket booked for {name}!")
    print(f"Train    : {selected['name']}")
    print(f"Route    : {booking['route']}")
    print(f"Date     : {booking['date']} at {booking['time']}")
    print(f"Seats    : {seats}")
    print(f"Total    : INR {total:.2f}")
    print(f"Booking ID : {booking['id']}")


def view_bookings():
    print("\n--- All Bookings ---")
    if len(bookings) == 0:
        print("No bookings found.")
        return

    for b in bookings:
        print(f"\nBooking ID : {b['id']}")
        print(f"Passenger  : {b['name']} (Age: {b['age']})")
        print(f"Train      : {b['train_name']}")
        print(f"Route      : {b['route']}")
        print(f"Date       : {b['date']} at {b['time']}")
        print(f"Seats      : {b['seats']}")
        print(f"Total      : INR {b['total']:.2f}")
        print(f"Payment    : {b['payment']}")
        print("-" * 30)


def update_payment():
    print("\n--- Update Payment ---")
    if len(bookings) == 0:
        print("No bookings found.")
        return

    bid = int(input("Enter Booking ID: "))
    for b in bookings:
        if b["id"] == bid:
            print(f"Current status: {b['payment']}")
            print("1. Paid\n2. Pending")
            ch = input("Choose: ")
            if ch == "1":
                b["payment"] = "Paid"
            else:
                b["payment"] = "Pending"
            print("Payment updated!")
            return

    print("Booking not found.")


def cancel_booking():
    print("\n--- Cancel Booking ---")
    if len(bookings) == 0:
        print("No bookings found.")
        return

    bid = int(input("Enter Booking ID to cancel: "))
    for i, b in enumerate(bookings):
        if b["id"] == bid:
            for t in trains:
                if t["id"] == b["train_id"]:
                    t["booked_seats"] -= b["seats"]
            removed = bookings.pop(i)
            print(f"Booking ID {removed['id']} for '{removed['name']}' cancelled successfully!")
            return

    print("Booking not found.")


def save_to_file():
    file = open("train_data.txt", "w")

    file.write("=== TRAINS ===\n")
    for t in trains:
        file.write(f"{t['id']},{t['name']},{t['from_location']},{t['to_location']},{t['date']},{t['time']},{t['total_seats']},{t['booked_seats']},{t['price']}\n")

    file.write("\n=== BOOKINGS ===\n")
    for b in bookings:
        file.write(f"{b['id']},{b['name']},{b['age']},{b['train_id']},{b['train_name']},{b['route']},{b['date']},{b['time']},{b['seats']},{b['total']},{b['payment']}\n")

    file.close()
    print("Data saved.")


def load_from_file():
    try:
        file = open("train_data.txt", "r")
        lines = file.readlines()
        file.close()

        section = None
        trains.clear()
        bookings.clear()

        for line in lines:
            line = line.strip()
            if line == "=== TRAINS ===":
                section = "trains"
            elif line == "=== BOOKINGS ===":
                section = "bookings"
            elif line == "":
                continue
            elif section == "trains":
                p = line.split(",")
                trains.append({"id": int(p[0]), "name": p[1], "from_location": p[2],
                                "to_location": p[3], "date": p[4], "time": p[5],
                                "total_seats": int(p[6]), "booked_seats": int(p[7]),
                                "price": float(p[8])})
            elif section == "bookings":
                p = line.split(",")
                bookings.append({"id": int(p[0]), "name": p[1], "age": int(p[2]),
                                  "train_id": int(p[3]), "train_name": p[4], "route": p[5],
                                  "date": p[6], "time": p[7], "seats": int(p[8]),
                                  "total": float(p[9]), "payment": p[10]})

        print("Data loaded.")

    except FileNotFoundError:
        print("No saved data. Starting fresh.")


def staff_menu():
    while True:
        print("\n==========================")
        print("        STAFF MENU        ")
        print("==========================")
        print("1. Add Train")
        print("2. View Trains")
        print("3. View Bookings")
        print("4. Update Payment")
        print("5. Save Data")
        print("6. Back")
        print("==========================")

        choice = input("Enter choice (1-6): ")

        if choice == "1":
            add_train()
        elif choice == "2":
            view_trains()
        elif choice == "3":
            view_bookings()
        elif choice == "4":
            update_payment()
        elif choice == "5":
            save_to_file()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def passenger_menu():
    while True:
        print("\n==========================")
        print("      PASSENGER MENU      ")
        print("==========================")
        print("1. View Trains")
        print("2. Book Ticket")
        print("3. Cancel Booking")
        print("4. Back")
        print("==========================")

        choice = input("Enter choice (1-4): ")

        if choice == "1":
            view_trains()
        elif choice == "2":
            book_ticket()
        elif choice == "3":
            cancel_booking()
        elif choice == "4":
            break
        else:
            print("Invalid choice.")


def main():
    load_from_file()

    while True:
        print("\n==========================")
        print("  TRAIN BOOKING SYSTEM    ")
        print("==========================")
        print("1. Staff")
        print("2. Passenger")
        print("3. Exit")
        print("==========================")

        choice = input("Enter choice (1-3): ")

        if choice == "1":
            staff_menu()
        elif choice == "2":
            passenger_menu()
        elif choice == "3":
            save_to_file()
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


main()
