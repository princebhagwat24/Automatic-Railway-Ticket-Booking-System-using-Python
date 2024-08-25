import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar
import re
import threading
import schedule
import datetime
from PIL import Image, ImageTk

class TicketBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Ticket Booking System")

        self.create_tabs()
        self.autofill_details()  # Autofill details when the application starts

    def load_css(self):
        # Define the CSS
        css = """
        .TLabel {
            font-size: 12;
            font-weight: bold;
            color: blue;
        }
        .TButton {
            background-color: green;
            color: white;
            font-weight: bold;
        }
        """

        # Apply the CSS to the style
        self.style = ttk.Style()
        self.style.element_create("Custom.Treeheading.border", "from", "default")
        self.style.layout("Custom.Treeview.Heading", [
            ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
            ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
                ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
                    ("Custom.Treeheading.image", {'sticky': ''}),
                    ("Custom.Treeheading.text", {'sticky': 'we'})
                ]})
            ]}),
        ])
        self.style.configure("Custom.Treeview.Heading", font=('Helvetica', 10), background="blue", foreground="white")
        self.style.configure(".", font=('Helvetica', 10))

        # Create a custom theme
        self.style.theme_create("custom", parent="plastik", settings={
            "TLabel": {"configure": {"foreground": "green"}},
            "TButton": {"configure": {"background": "yellow", "foreground": "blue"}},
            "TNotebook.Tab": {"configure": {"padding": [10, 10], "background": "orange"}},
        })

        # Set the custom theme
        self.style.theme_use("custom")

    def create_tabs(self):
        self.tab_control = ttk.Notebook(self.root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)  # Payment Tab
        self.tab_control.add(self.tab1, text='Journey Details')
        self.tab_control.add(self.tab2, text='Booking Details')
        self.tab_control.add(self.tab3, text='Passenger Details')
        self.tab_control.add(self.tab4, text='Payment')  # Add the Payment Tab
        self.tab_control.pack(expand=1, fill='both')

        self.create_tab1()
        self.create_tab2()
        self.create_tab3()
        self.create_tab4()  # Create the Payment Tab

    def create_tab1(self):
        tk.Label(self.tab1, text="Source:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = tk.Entry(self.tab1)
        self.source_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab1, text="Destination:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.destination_entry = tk.Entry(self.tab1)
        self.destination_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.tab1, text="Date (dd-mm-yyyy):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.date_var = tk.StringVar()  # Variable to store selected date
        self.date_entry = tk.Entry(self.tab1, textvariable=self.date_var)  # Entry field to display selected date
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)
        self.date_entry.bind("<Button-1>", self.show_calendar)  # Bind left-click event to show_calendar function

        next_button = tk.Button(self.tab1, text="Next", command=self.validate_tab1)
        next_button.grid(row=3, column=0, columnspan=2, pady=10)

    def show_calendar(self, event):
        top = tk.Toplevel(self.root)
        cal = Calendar(top, selectmode='day', date_pattern='dd-mm-yyyy')  # Calendar widget
        cal.pack(padx=10, pady=10)

        def select_date():
            selected_date = cal.get_date()  # Get selected date from calendar
            self.date_var.set(selected_date)  # Set selected date to date entry field
            top.destroy()  # Close the calendar popup

        select_button = tk.Button(top, text="Select Date", command=select_date)
        select_button.pack(pady=5)

    def validate_tab1(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()
        date = self.date_entry.get()
        
        if not source.isalpha():
            messagebox.showerror("Error", "Source field should contain only characters.")
            return
        elif not destination.isalpha():
            messagebox.showerror("Error", "Destination field should contain only characters.")
            return
        elif not self.validate_date_format(date):
            messagebox.showerror("Error", "Date field should be in dd-mm-yyyy format.")
            return

        self.show_tab2()

    def validate_date_format(self, date):
        try:
            day, month, year = map(int, date.split('-'))
            if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 9999):
                return False
        except ValueError:
            return False
        return True

    def create_tab2(self):
        tk.Label(self.tab2, text="Class:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.class_var = tk.StringVar(self.tab2)
        self.class_var.set("Sleeper")
        class_option = tk.OptionMenu(self.tab2, self.class_var, "Sleeper", "3AC", "2AC", "1AC")
        class_option.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.tab2, text="Number of Passengers:").grid(row=1, column=0, padx=5, pady=5, sticky="w")  # Updated label
        self.num_passengers_var = tk.IntVar(self.tab2)  # Changed variable name
        self.num_passengers_entry = tk.Entry(self.tab2, textvariable=self.num_passengers_var)  # Changed variable name
        self.num_passengers_entry.grid(row=1, column=1, padx=5, pady=5)  # Changed variable name

        next_button = tk.Button(self.tab2, text="Next", command=self.show_tab3)  # Update the command to show_tab3
        next_button.grid(row=2, column=0, columnspan=2, pady=10)

    def create_tab3(self):
        tk.Label(self.tab3, text="Passenger Details", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        berth_options = ["Lower Berth", "Middle Berth", "Upper Berth", "Side Lower", "Side Upper"]

        self.passenger_entries = []
        for i in range(3):  # Let's create 3 sets of fields for passenger details
            tk.Label(self.tab3, text=f"Passenger {i+1}").grid(row=i*6+1, column=0, columnspan=2, pady=5)
            tk.Label(self.tab3, text="Name:").grid(row=i*6+2, column=0, padx=5, pady=5, sticky="w")
            name_entry = tk.Entry(self.tab3)
            name_entry.grid(row=i*6+2, column=1, padx=5, pady=5)
            tk.Label(self.tab3, text="Age:").grid(row=i*6+3, column=0, padx=5, pady=5, sticky="w")
            age_entry = tk.Entry(self.tab3)
            age_entry.grid(row=i*6+3, column=1, padx=5, pady=5)
            tk.Label(self.tab3, text="Gender:").grid(row=i*6+4, column=0, padx=5, pady=5, sticky="w")
            gender_var = tk.StringVar(self.tab3)
            gender_var.set("Male")
            gender_option_menu = tk.OptionMenu(self.tab3, gender_var, "Male", "Female", "Others")
            gender_option_menu.grid(row=i*6+4, column=1, padx=5, pady=5)
            tk.Label(self.tab3, text="Berth Preference:").grid(row=i*6+5, column=0, padx=5, pady=5, sticky="w")
            berth_var = tk.StringVar(self.tab3)
            berth_var.set(berth_options[0])  # Set default value
            berth_option_menu = tk.OptionMenu(self.tab3, berth_var, *berth_options)
            berth_option_menu.grid(row=i*6+5, column=1, padx=5, pady=5)

            self.passenger_entries.append((name_entry, age_entry, gender_var, berth_var))

        book_button = tk.Button(self.tab3, text="Book Tickets", command=self.validate_passenger_details)  # Change the command to validate_passenger_details
        book_button.grid(row=18, column=0, columnspan=2, pady=10)

    def create_tab4(self):
        tk.Label(self.tab4, text="Payment Options", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.tab4, text="Card Number:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.card_number_entry = tk.Entry(self.tab4)
        self.card_number_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.tab4, text="Expiration Date (mm/yy):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.expiry_date_entry = tk.Entry(self.tab4)
        self.expiry_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.tab4, text="CVV:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.cvv_entry = tk.Entry(self.tab4)
        self.cvv_entry.grid(row=3, column=1, padx=5, pady=5)

        back_button = tk.Button(self.tab4, text="Back", command=self.show_tab3)
        back_button.grid(row=4, column=0, pady=10)

        pay_button = tk.Button(self.tab4, text="Pay Now", command=self.book_tickets)
        pay_button.grid(row=4, column=1, pady=10)

    def show_tab2(self):
        num_passengers = self.num_passengers_var.get()  # Get the number of passengers entered
        if num_passengers <= 0:
            messagebox.showerror("Error", "Please enter a valid number of passengers.")
            return
        self.tab_control.select(self.tab2)

    def validate_num_passengers(self):
        num_passengers = self.num_passengers_var.get()
        return num_passengers == len(self.passenger_entries)

    def show_tab3(self):
        if not self.validate_num_passengers():
            messagebox.showerror("Error", "Number of passengers does not match passenger details.")
            return
        self.tab_control.select(self.tab3)

    def show_tab4(self):
        self.tab_control.select(self.tab4)

    def book_tickets(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()
        date = self.date_entry.get()
        class_choice = self.class_var.get()
        num_tickets = self.num_passengers_var.get()

        passenger_details = []
        for entry_set in self.passenger_entries:
            name = entry_set[0].get()
            age = entry_set[1].get()
            gender = entry_set[2].get()
            berth_preference = entry_set[3].get()
            passenger_details.append((name, age, gender, berth_preference))

        # Retrieve payment details
        card_number = self.card_number_entry.get()
        expiry_date = self.expiry_date_entry.get()
        cvv = self.cvv_entry.get()

        # Validate payment details
        if not (re.match(r'^\d{16}$', card_number) and re.match(r'^\d{2}/\d{2}$', expiry_date) and re.match(r'^\d{3}$', cvv)):
            messagebox.showerror("Error", "Please enter valid payment details.")
            return

        # Printing the booking details
        booking_details = f"Source: {source}\n"
        booking_details += f"Destination: {destination}\n"
        booking_details += f"Date: {date}\n"
        booking_details += f"Class: {class_choice}\n"
        booking_details += f"Number of Passengers: {num_tickets}\n\n"
        booking_details += "Passenger Details:\n"
        for i, passenger in enumerate(passenger_details, 1):
            booking_details += f"Passenger {i}:\n"
            booking_details += f"Name: {passenger[0]}\n"
            booking_details += f"Age: {passenger[1]}\n"
            booking_details += f"Gender: {passenger[2]}\n"
            booking_details += f"Berth Preference: {passenger[3]}\n\n"

        # Include payment details in the booking information
        booking_details += "Payment Details:\n"
        booking_details += f"Card Number: {card_number}\n"
        booking_details += f"Expiration Date: {expiry_date}\n"
        booking_details += f"CVV: {cvv}"

        # Create a log file with timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"booking_{timestamp}.log"

        # Write booking details to the log file
        with open(log_filename, "w") as log_file:
            log_file.write(booking_details)

        # Show booking details in messagebox
        messagebox.showinfo("Booking Details", booking_details)
        messagebox.showinfo("Booking Successful", "Ticket booked successfully!")

    def autofill_details(self):
        # Set default values for journey details
        self.source_entry.insert(0, "Mumbai")
        self.destination_entry.insert(0, "Kosamba")
        self.date_var.set("29-05-2024")
        self.class_var.set("3AC")
        self.num_passengers_var.set(3)  # Autofill details for 3 passengers

        # Autofill passenger details for demonstration
        passenger_details = [
            ("POSTER PRESENTATION", "30", "Male", "Lower Berth"),
            ("SOE", "25", "Female", "Upper Berth"),
            ("MINOR PROJECT", "40", "Male", "Middle Berth")
        ]

        for i, entry_set in enumerate(self.passenger_entries):
            entry_set[0].insert(0, passenger_details[i][0])  # Name
            entry_set[1].insert(0, passenger_details[i][1])  # Age
            entry_set[2].set(passenger_details[i][2])        # Gender
            entry_set[3].set(passenger_details[i][3])        # Berth Preference

        # Autofill payment details (you can add this section if needed)
        self.card_number_entry.insert(0, "1234567890123456")
        self.expiry_date_entry.insert(0, "12/25")
        self.cvv_entry.insert(0, "123")

    def validate_passenger_details(self):
        for entry_set in self.passenger_entries:
            name = entry_set[0].get()
            age = entry_set[1].get()
            gender = entry_set[2].get()
            berth_preference = entry_set[3].get()

            if not name.replace(" ", "").isalpha():
                messagebox.showerror("Error", "Name should contain only characters.")
                return False
            
            if not age.isdigit():
                messagebox.showerror("Error", "Age should contain only integers.")
                return False

        self.show_tab4()  # If all validations pass, proceed to the payment tab

def run_booking():
    root = tk.Tk()
    app = TicketBookingSystem(root)
    root.mainloop()

# Schedule the booking to run at a specific time
schedule.every().day.at("15:58").do(run_booking)

# Run the scheduler in a separate thread
def scheduler_thread():
    while True:
        schedule.run_pending()

scheduler_t = threading.Thread(target=scheduler_thread)
scheduler_t.start()

if __name__ == "__main__":
    run_booking()
