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
        self.root = root_window
        # rest of your code
        self.root.title('Daycare Database Management')
        self.db_manager = DatabaseManager()

        custom_font = ('Helvetica', 12)
        button_frame = tk.Frame(self.root, bg='lightgrey')
        button_frame.pack(fill='x', padx=10, pady=10)

        button_width = 20
        button_height = 2

        tk.Button(button_frame, text='Calendar', command=self.open_calendar_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=0, column=0, padx=5, pady=5)
        ttk.Separator(button_frame, orient='vertical').grid(row=0, column=1, rowspan=3, sticky='ns')
        tk.Button(button_frame, text='Add New Child', command=self.open_add_child_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=0, column=2, padx=5, pady=5)
        ttk.Separator(button_frame, orient='vertical').grid(row=0, column=3, rowspan=3, sticky='ns')
        tk.Button(button_frame, text='View Database', command=self.view_list, font=custom_font, bg='lightblue', width=button_width, height=button_height).grid(
            row=0, column=4, padx=5, pady=5)
        tk.Button(button_frame, text='Remove Child', command=self.open_remove_child_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=1, column=2, padx=5, pady=5)
        tk.Button(button_frame, text='Process Payment', command=self.open_payment_window, font=custom_font,
                  bg='lightblue', width=button_width, height=button_height).grid(row=1, column=4, padx=5, pady=5)
        tk.Button(button_frame, text='Exit', command=self.root.quit, font=custom_font, bg='lightblue', width=button_width, height=button_height).grid(row=2, column=0, padx=5, pady=5)

        # Lock the window size
        window_width = 625
        window_height = 200
        self.root.minsize(window_width, window_height)
        self.root.maxsize(window_width, window_height)

    def open_calendar_window(self):
        """
        Open the calendar view window.
        """
        CalendarView(self.root, self.db_manager)

    def open_add_child_window(self):
        """
        Open the add child window.
        """
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Child")

        tk.Label(add_window, text='Name:').grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        tk.Label(add_window, text='Age:').grid(row=1, column=0)
        age_entry = tk.Entry(add_window)
        age_entry.grid(row=1, column=1)

        tk.Label(add_window, text='Balance:').grid(row=2, column=0)
        balance_entry = tk.Entry(add_window)
        balance_entry.grid(row=2, column=1)

        tk.Button(add_window, text='Enter',
                  command=lambda: self.add_child(name_entry.get(), age_entry.get(), balance_entry.get(),
                                                 add_window)).grid(row=3, column=0)
        tk.Button(add_window, text='Cancel', command=add_window.destroy).grid(row=3, column=1)

        # Sort the children's names after adding a new child
        data = self.db_manager.read_database()
        data.sort(key=lambda x: x['name'])
        self.db_manager.write_database(data)

    def add_child(self, name, age, balance, window):
        """
        Add a child to the database.
        """
        data = self.db_manager.read_database()
        data.append({'name': name, 'age': age, 'balance': balance})

        # Sort the data by children's names
        data.sort(key=lambda x: x['name'])

        self.db_manager.write_database(data)
        messagebox.showinfo("Success", "Child added successfully", parent=window)
        window.destroy()

    def open_remove_child_window(self):
        """
        Open the remove child window.
        """
        remove_window = tk.Toplevel(self.root)
        remove_window.title("Remove Child")

        tk.Label(remove_window, text='Name:').grid(row=0, column=0)

        # Get the list of children's names, sort it, and create a Combobox with it
        children_names = sorted([child['name'] for child in self.db_manager.read_database()])
        name_combobox = ttk.Combobox(remove_window, values=children_names)
        name_combobox.grid(row=0, column=1)

        tk.Button(remove_window, text='Enter', command=lambda: self.remove_child(name_combobox.get(),
                                                                                 remove_window)).grid(row=1, column=0)
        tk.Button(remove_window, text='Cancel', command=remove_window.destroy).grid(row=1, column=1)

    def remove_child(self, name, window):
        """
        Remove a child from the database.
        """
        data = self.db_manager.read_database()
        data = [child for child in data if child['name'] != name]
        self.db_manager.write_database(data)
        messagebox.showinfo("Success", "Child removed successfully", parent=window)
        window.destroy()

    def view_list(self):
        """
        Open the view list window.
        """
        list_window = tk.Toplevel(self.root)
        list_window.title("View List")

        tree = ttk.Treeview(list_window, columns=("Name", "Age", "Balance"), show="headings")
        tree.heading('Name', text='Name', anchor='e')
        tree.heading('Age', text='Age', anchor='e')
        tree.heading('Balance', text='Balance', anchor='e')

        tree.column('Name', anchor='e')
        tree.column('Age', anchor='e')
        tree.column('Balance', anchor='e')

        for child in sorted(self.db_manager.read_database(), key=lambda x: x['name']):
            formatted_balance = "{:.2f}".format(float(child['balance']))
            tree.insert('', tk.END, values=(child['name'], child['age'], formatted_balance))

        tree.pack(expand=True, fill='both')
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

        # Create a Combobox with the list of strings
        name_combobox = ttk.Combobox(payment_window, values=names_and_balances, font=('Courier', 10))
        name_combobox.grid(row=0, column=1)

        tk.Label(payment_window, text='Amount:').grid(row=1, column=0)
        amount_entry = tk.Entry(payment_window)
        amount_entry.grid(row=1, column=1)

        tk.Button(payment_window, text='Apply',
                  command=lambda: self.apply_payment(name_combobox.get().strip().split()[0], amount_entry.get(),
                                                     payment_window)).grid(row=2, column=0)

        tk.Button(payment_window, text='Exit', command=payment_window.destroy).grid(row=2, column=1)

    def apply_payment(self, name, amount, window):
        """
        Apply a payment to a child's balance. If the payment is more than the balance,
        the balance is set to 0 and the overpayment is returned to the customer.
        """
        try:
            amount = float(amount)
            data = self.db_manager.read_database()
            for child in data:
                if child['name'] == name:
                    if amount > float(child['balance']):
                        overpayment = amount - float(child['balance'])
                        child['balance'] = '0'
                        messagebox.showinfo("Overpayment", f"The payment exceeded the balance due. "
                                                           f"An amount of {overpayment:.2f} "
                                                           f"will be returned to the customer.", parent=window)
                    else:
                        child['balance'] = str(float(child['balance']) - amount)
                    self.db_manager.write_database(data)
                    messagebox.showinfo("Success", f"Payment of {amount:.2f} applied to {name}", parent=window)
                    window.destroy()
                    return
            messagebox.showerror("Error", f"No child with name {name} found", parent=window)
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.", parent=window)
