flights = [
    {"flight_no": "AI-101", "source": "Delhi",    "destination": "Mumbai",    "fare": 4500, "total_seats": 6, "seats_left": 6},
    {"flight_no": "AI-202", "source": "Mumbai",    "destination": "Bangalore", "fare": 3800, "total_seats": 6, "seats_left": 6},
    {"flight_no": "AI-303", "source": "Delhi",     "destination": "Chennai",   "fare": 5200, "total_seats": 6, "seats_left": 6},
    {"flight_no": "AI-404", "source": "Bangalore", "destination": "Kolkata",   "fare": 4100, "total_seats": 6, "seats_left": 6},
]

bookings = []
TRAVEL_CLASSES = ("Economy", "Business")
CLASS_MULTIPLIER = {"Economy": 1.0, "Business": 1.8}


def show_menu():
    print("\n" + "=" * 45)
    print("     AIRLINE TICKET RESERVATION SYSTEM")
    print("=" * 45)
    print("1. View Available Flights")
    print("2. Book a Ticket")
    print("3. View All Bookings")
    print("4. Cancel a Booking")
    print("5. Search Flights by Route")
    print("6. Exit")
    print("=" * 45)


def view_flights():
    print(f"\n{'Flight No':<10}{'From':<12}{'To':<12}{'Fare':>8}{'Seats Left':>12}")
    print("-" * 55)
    for flight in flights:
        print(f"{flight['flight_no']:<10}{flight['source']:<12}{flight['destination']:<12}"
              f"{flight['fare']:>8}{flight['seats_left']:>12}")
    print("-" * 55)


def find_flight_by_number(flight_no):
    for flight in flights:
        if flight["flight_no"].upper() == flight_no.upper():
            return flight
    return None


def choose_travel_class():
    print("\nTravel Class Options:")
    for index, cls in enumerate(TRAVEL_CLASSES, start=1):
        print(f"  {index}. {cls}")

    while True:
        choice = input("Choose class number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(TRAVEL_CLASSES):
            return TRAVEL_CLASSES[int(choice) - 1]
        print("Invalid choice. Pick a number from the list above.")


def calculate_fare(base_fare, travel_class="Economy"):
    multiplier = CLASS_MULTIPLIER.get(travel_class, 1.0)
    return round(base_fare * multiplier, 2)


def book_ticket():
    view_flights()
    flight_no = input("\nEnter flight number to book: ").strip()
    flight = find_flight_by_number(flight_no)

    if flight is None:
        print("Flight not found. Please check the flight number.")
        return

    if flight["seats_left"] <= 0:
        print(f"Sorry, flight {flight['flight_no']} is fully booked. No seats left.")
        return

    passenger_name = input("Enter passenger name: ").strip().title()
    age = get_valid_age()
    travel_class = choose_travel_class()
    final_fare = calculate_fare(flight["fare"], travel_class)

    while True:
        confirm = input(f"Confirm booking for {passenger_name} at ₹{final_fare:.2f}? (yes/no): ").strip().lower()
        if confirm in ("yes", "no"):
            break
        print("Please type 'yes' or 'no'.")

    if confirm == "no":
        print("Booking cancelled by user.")
        return

    booking = {
        "passenger": passenger_name,
        "age": age,
        "flight_no": flight["flight_no"],
        "route": f"{flight['source']} -> {flight['destination']}",
        "class": travel_class,
        "fare_paid": final_fare
    }
    bookings.append(booking)
    flight["seats_left"] -= 1

    print("\n✔ Booking Confirmed!")
    print(f"  Passenger : {passenger_name}")
    print(f"  Flight    : {flight['flight_no']} ({booking['route']})")
    print(f"  Class     : {travel_class}")
    print(f"  Fare Paid : ₹{final_fare:.2f}")


def get_valid_age():
    while True:
        value = input("Enter passenger age: ").strip()
        if value.isdigit() and 1 <= int(value) <= 120:
            return int(value)
        print("Invalid age. Please enter a number between 1 and 120.")


def view_bookings():
    if not bookings:
        print("No bookings made yet.")
        return

    print(f"\n{'No.':<5}{'Passenger':<15}{'Flight':<10}{'Route':<20}{'Class':<10}{'Fare':>8}")
    print("-" * 70)
    total_revenue = 0
    for i, b in enumerate(bookings, start=1):
        print(f"{i:<5}{b['passenger']:<15}{b['flight_no']:<10}{b['route']:<20}{b['class']:<10}{b['fare_paid']:>8.2f}")
        total_revenue += b["fare_paid"]
    print("-" * 70)
    print(f"{'Total Revenue':<60}{total_revenue:>8.2f}")


def cancel_booking():
    if not bookings:
        print("No bookings to cancel.")
        return

    view_bookings()
    passenger_name = input("\nEnter passenger name to cancel: ").strip().title()
    flight_no = input("Enter flight number: ").strip().upper()

    for booking in bookings:
        if booking["passenger"] == passenger_name and booking["flight_no"].upper() == flight_no:
            bookings.remove(booking)
            flight = find_flight_by_number(flight_no)
            if flight:
                flight["seats_left"] += 1
            print(f"✔ Booking cancelled for {passenger_name} on flight {flight_no}.")
            return

    print("No matching booking found.")


def search_flights_by_route():
    raw_input_text = input(
        "Enter route as 'Source to Destination' (or a single city, Enter to skip): "
    ).strip().lower()

    source = ""
    destination = ""

    if raw_input_text != "":
        parts = raw_input_text.split(" to ")
        if len(parts) == 2:
            source = parts[0].strip().title()
            destination = parts[1].strip().title()
        else:
            source = parts[0].strip().title()

    results = []
    for flight in flights:
        source_match = (source == "" or flight["source"].lower() == source.lower())
        destination_match = (destination == "" or flight["destination"].lower() == destination.lower())
        if source_match and destination_match:
            results.append(flight)
        else:
            continue

    if not results:
        print("No flights found matching that route.")
        return

    print(f"\n{'Flight No':<10}{'From':<12}{'To':<12}{'Fare':>8}{'Seats Left':>12}")
    print("-" * 55)
    for flight in results:
        print(f"{flight['flight_no']:<10}{flight['source']:<12}{flight['destination']:<12}"
              f"{flight['fare']:>8}{flight['seats_left']:>12}")


def main():
    print("Welcome to the Airline Ticket Reservation System!")

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_flights()
        elif choice == "2":
            book_ticket()
        elif choice == "3":
            view_bookings()
        elif choice == "4":
            cancel_booking()
        elif choice == "5":
            search_flights_by_route()
        elif choice == "6":
            print("Thank you for using the Airline Reservation System. Safe travels! ✈️")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")


if __name__ == "__main__":
    main()