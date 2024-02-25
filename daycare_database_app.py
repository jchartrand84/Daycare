import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database_manager import DatabaseManager
from calendar_view import CalendarView

"""
daycare_database_app.py

This file contains the DaycareDatabaseApp class which is responsible for managing the main application window and
interactions with the user. It provides functionality for adding and removing children, viewing the database,
applying payments, and viewing the calendar. It uses the DatabaseManager class to interact with the database.
"""


class DaycareDatabaseApp:
    """
    The DaycareDatabaseApp class manages the main application window and user interactions.
    """
    def __init__(self, root_window):
        """
        Initialize the DaycareDatabaseApp with a root Tkinter window.
        """
        # Initialize the root window and set the title
        self.root = root_window
        self.root.title('Daycare Database Management')

        # Initialize the DatabaseManager
        self.db_manager = DatabaseManager()

        # Set up the button frame with custom font and dimensions# Create the main application window
        custom_font = ('Helvetica', 12)
        button_frame = tk.Frame(self.root, bg='lightgrey')
        button_frame.pack(fill='x', padx=10, pady=10)
        button_width = 20
        button_height = 2

        # Add buttons for various functionalities like Calendar, Add New Child, View Database, etc.
        tk.Button(button_frame, text='Calendar', command=self.open_calendar_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=0, column=0, padx=5, pady=5)
        ttk.Separator(button_frame, orient='vertical').grid(row=0, column=1, rowspan=3, sticky='ns')
        tk.Button(button_frame, text='Add New Child', command=self.open_add_child_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=0, column=2, padx=5, pady=5)
        ttk.Separator(button_frame, orient='vertical').grid(row=0, column=3, rowspan=3, sticky='ns')
        tk.Button(button_frame, text='View Database', command=self.view_list, font=custom_font, bg='lightblue',
                  width=button_width, height=button_height).grid(
            row=0, column=4, padx=5, pady=5)
        tk.Button(button_frame, text='Remove Child', command=self.open_remove_child_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text='Process Payment', command=self.open_payment_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=1, column=4, padx=5, pady=5)
        tk.Button(button_frame, text='Exit', command=self.root.quit, font=custom_font, bg='lightblue',
                  width=button_width, height=button_height).grid(row=2, column=0, padx=5, pady=5)

        # Lock the window size
        window_width = 625
        window_height = 200
        self.root.minsize(window_width, window_height)
        self.root.maxsize(window_width, window_height)

    def open_calendar_window(self):
        """
        Open the calendar view window.
        """
        # Create an instance of the CalendarView class
        CalendarView(self.root, self.db_manager)

    def open_add_child_window(self):
        """
        Open the add child window.
        """
        # Create a new top-level window and set its title
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Child")

        # Add labels and entry fields for Name and Age
        tk.Label(add_window, text='Name:').grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)
        tk.Label(add_window, text='Age:').grid(row=1, column=0)
        age_entry = tk.Entry(add_window)
        age_entry.grid(row=1, column=1)

        # Add Enter and Cancel buttons
        tk.Button(add_window, text='Enter',
                  command=lambda: self.add_child(name_entry.get(), age_entry.get(), add_window)).grid(row=2, column=0)
        tk.Button(add_window, text='Cancel', command=add_window.destroy).grid(row=2, column=1)

        # Sort the children's names after adding a new child
        data = self.db_manager.read_database()
        data.sort(key=lambda x: x['name'])
        self.db_manager.write_database(data)

    def add_child(self, name, age, window):
        """
        Add a child to the database.
        """
        # Ensure the first letter of the name is uppercase
        name = name.capitalize()

        # Validate the name and age inputs
        if not name:
            messagebox.showerror("Error", "Name cannot be empty.", parent=window)
            return
        if not name.isalpha():
            messagebox.showerror("Error", "Name should only contain alphabetic characters.", parent=window)
            return
        if len(name) > 50:  # Limit the name to 50 characters
            messagebox.showerror("Error", "Name cannot be more than 50 characters.", parent=window)
            return
        try:
            age = int(age)
            if age < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Age must be a positive integer.", parent=window)
            return

        # Check if the name is unique
        if not self.db_manager.is_name_unique(name):
            messagebox.showerror("Error",
                                 f"The name '{name}' is already in use. Please use a unique name. "
                                 f"Note: names are not case sensitive.", parent=window)
            return

        # Add the new child to the database and sort the data by children's names
        data = self.db_manager.read_database()
        data.append({'name': name, 'age': age, 'balance': '0'})
        data.sort(key=lambda x: x['name'])

        # Write the updated child data to the database after applying the payment
        self.db_manager.write_database(data)
        messagebox.showinfo("Success", "Child added successfully", parent=window)
        window.destroy()  # Close the window after successfully adding the child

    def open_remove_child_window(self):
        """
        Open the remove child window.
        """
        # Create a new top-level window and set its title
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Child")

        # Add a label for the Name field
        tk.Label(remove_window, text='Name:').grid(row=0, column=0)

        # Get the list of children's names, sort it, and create an OptionMenu with it
        children_names = sorted([child['name'] for child in self.db_manager.read_database()])
        selected_name = tk.StringVar()
        name_remove_menu = tk.OptionMenu(remove_window, selected_name, *children_names)
        name_remove_menu.grid(row=0, column=1)

        # Add Enter and Cancel buttons
        tk.Button(remove_window, text='Enter', command=lambda: self.remove_child(selected_name.get(),
                                                                                 remove_window)).grid(row=1, column=0)
        tk.Button(remove_window, text='Cancel', command=remove_window.destroy).grid(row=1, column=1)

    def remove_child(self, name, window):
        """
        Remove a child from the database.
        """
        # Read the children's data from the database
        data = self.db_manager.read_database()

        # Remove the child from the database & prompt user with a success message
        data = [child for child in data if child['name'] != name]

        self.db_manager.write_database(data)
        messagebox.showinfo("Success", "Child removed successfully", parent=window)

        window.destroy()  # Close the window

    def view_list(self):
        """
        Open the view list window.
        This window displays a list of all children in the database along with their age and balance.
        """
        # Create a new top-level window and set its title
        list_window = tk.Toplevel(self.root)
        list_window.title("View List")

        # Create a Treeview widget with columns for Name, Age, and Balance
        tree = ttk.Treeview(list_window, columns=("Name", "Age", "Balance"), show="headings")
        tree.heading('Name', text='Name', anchor='e')
        tree.heading('Age', text='Age', anchor='e')
        tree.heading('Balance', text='Balance', anchor='e')

        tree.column('Name', anchor='e')
        tree.column('Age', anchor='e')
        tree.column('Balance', anchor='e')

        # Populate the Treeview with data from the database
        for child in sorted(self.db_manager.read_database(), key=lambda x: x['name'].lower()):
            formatted_balance = "{:.2f}".format(float(child['balance']))
            tree.insert('', tk.END, values=(child['name'], child['age'], formatted_balance))

        # Add the Treeview to the window and pack it
        tree.pack(expand=True, fill='both')

        # Add an Exit button to the window
        tk.Button(list_window, text='Exit', command=list_window.destroy).pack(fill='x')

    def open_payment_window(self):
        """
        Open the payment window.
        """
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Record Payment")

        tk.Label(payment_window, text='Name:').grid(row=0, column=0)

        # Read the children's data from the database
        children_data = self.db_manager.read_database()

        # Filter out the children with a balance of 0
        children_with_balance = [child for child in children_data if float(child['balance']) > 0]

        # Create a list of strings, where each string contains a child's name and their balance
        names_and_balances = [f"{child['name'].ljust(20)} {format(float(child['balance']), '.2f').strip().rjust(10)}"
                              for child in children_with_balance]

        # Create an OptionMenu with the list of strings
        selected_name_and_balance = tk.StringVar()
        name_payment_menu = tk.OptionMenu(payment_window, selected_name_and_balance, *names_and_balances)
        name_payment_menu.config(font=('Courier', 10))
        name_payment_menu.grid(row=0, column=1)

        tk.Label(payment_window, text='Amount:').grid(row=1, column=0)
        amount_entry = tk.Entry(payment_window)
        amount_entry.grid(row=1, column=1)

        # Add Apply and Exit buttons
        tk.Button(payment_window, text='Apply',
                  command=lambda: self.apply_payment(selected_name_and_balance.get().strip().split()[0],
                                                     amount_entry.get(),
                                                     payment_window)).grid(row=2, column=0)

        tk.Button(payment_window, text='Exit', command=payment_window.destroy).grid(row=2, column=1)

    def apply_payment(self, name, amount, window):
        """
        Apply a payment to a child's balance. If the payment is more than the balance,
        the balance is set to 0 and the overpayment is returned to the customer.
        """
        try:
            # Convert the amount to a float and validate it
            amount = float(amount)
            if amount < 0:
                messagebox.showerror("Error", "Invalid amount. Please enter a positive number.", parent=window)
                return

            # Read the children's data from the database
            data = self.db_manager.read_database()

            # Find the child with the given name and apply the payment
            for child in data:
                if child['name'] == name:
                    if amount > float(child['balance']):
                        # If the payment is more than the balance, calculate the overpayment
                        overpayment = amount - float(child['balance'])
                        child['balance'] = '0'
                        messagebox.showinfo("Overpayment", f"The payment exceeded the balance due. "
                                                           f"Change of {overpayment:.2f} "
                                                           f"is due to the customer.", parent=window)
                    else:
                        # If the payment is less than or equal to the balance, subtract the payment from the balance
                        child['balance'] = str(float(child['balance']) - amount)

                    # Write the updated child data to the database after applying the payment
                    self.db_manager.write_database(data)

                    # Show a success message and close the window
                    messagebox.showinfo("Success", f"Payment of {amount:.2f} applied to {name}", parent=window)
                    window.destroy()
                    return

        except ValueError:
            # If the amount is not a valid float, show an error message
            messagebox.showerror("Error", "Invalid amount. Please enter a positive number.", parent=window)
            return
