import os
import tkinter as tk
from tkinter import messagebox
import datetime

"""
attendance_window.py

This file contains the AttendanceWindow class which is responsible for managing the attendance window.
It provides functionality for viewing attendance for a specific date, adding a child to the attendance,
and removing a child from the attendance.
"""


class AttendanceWindow(tk.Toplevel):
    """
    The AttendanceWindow class manages the attendance window.
    """
    def __init__(self, parent, db_manager, date):
        """
        Initialize the AttendanceWindow with a parent Tkinter window, a DatabaseManager, and a date.
        """
        # Initialize the AttendanceWindow with a parent Tkinter window, a DatabaseManager, and a date
        super().__init__(parent)
        self.db_manager = db_manager
        self.date = date
        self.title(f"Attendance for {date}")

        # Retrieve all children from the database and check if the database is empty
        all_children = self.get_all_children()
        if not all_children:
            messagebox.showinfo("Error", "No children in the database.", parent=self)
            return

        # Create a dropdown menu with the names of all children
        self.child_name = tk.StringVar(self)
        self.child_name.set(all_children[0])
        self.child_menu = tk.OptionMenu(self, self.child_name, *all_children)
        self.child_menu.config(width=20)
        self.child_menu.grid(row=0, column=2, sticky='w')

        # Add buttons for adding, removing, and exiting
        self.add_button = tk.Button(self, text='Add', command=lambda: self.
                                    add_child_to_attendance(self.child_name.get()), width=20)
        self.add_button.grid(row=1, column=2)

        self.remove_button = tk.Button(self, text='Remove', command=lambda: self.
                                       remove_child_from_attendance(self.child_name.get()), width=20)
        self.remove_button.grid(row=2, column=2)

        self.exit_button = tk.Button(self, text='Exit', command=self.destroy, width=20)
        self.exit_button.grid(row=3, column=2)

        # Add a vertical line between the two columns
        tk.Frame(self, width=2, bg="black").grid(row=0, column=1, rowspan=4, sticky='ns')

        self.grid_columnconfigure(0, weight=1, minsize=100)  # Set a minimum width for the first column
        self.update_labels()  # Update the attendance labels after adding or removing a child

    def update_labels(self):
        """
        Update the labels for the window.
        """
        # Remove all current labels
        for widget in self.grid_slaves():
            if isinstance(widget, tk.Label):
                widget.destroy()

        # Add new labels
        attendance = self.get_attendance(str(self.date))
        if attendance:
            for i, child in enumerate(sorted(attendance)):
                tk.Label(self, text=child).grid(row=i, column=0, sticky='e', padx=10)
        else:
            tk.Label(self, text='-').grid(row=0, column=0, sticky='e', padx=10)

    def get_attendance(self, date):
        """
        Get the attendance for a specific date.
        """
        attendance_data = self.db_manager.read_attendance()
        attendance = [record for record in attendance_data if record['date'] == date]
        return [record['name'] for record in attendance]

    def get_all_children(self):
        """
        Get all children from the database.
        """
        children_data = self.db_manager.read_database()
        return [child['name'] for child in children_data]

    def add_child_to_attendance(self, child_name):
        """
        Add a child to the attendance for the current date.
        """
        all_children = self.get_all_children()

        # Check if the child's name exists in the database
        if child_name not in all_children:
            messagebox.showinfo("Error", f"{child_name} does not exist in the database.", parent=self)
            return

        # Check if the current month has been finalized
        if self.check_month_finalized() or self.check_weekend():
            return

        # Check if the date is in the past
        if self.date < datetime.date.today():
            messagebox.showinfo("Error", "Cannot modify past dates.", parent=self)
            return

        # Check if the child is already attending on the specified date
        attendance_data = self.db_manager.read_attendance()
        for record in attendance_data:
            if record['date'] == str(self.date) and record['name'] == child_name:
                messagebox.showinfo("Error", f"{child_name} is already attending on {self.date}.", parent=self)
                return

        # Check if the daily limit has been reached
        daily_attendance = [record for record in attendance_data if record['date'] == str(self.date)]
        if len(daily_attendance) >= 6:
            messagebox.showinfo("Error", "Daily capacity (6) has been reached."
                                         "\nChild cannot be added to attendance.", parent=self)
            return

        # Write the updated attendance data to the database
        attendance_data.append({'date': self.date, 'name': child_name})
        self.db_manager.write_attendance(attendance_data)

        # Update the window labels
        self.update_labels()

    def remove_child_from_attendance(self, child_name):
        """
        Remove a child from the attendance for the current date.
        """
        # Retrieve all children from the database
        all_children = self.get_all_children()

        # Check if the child's name exists in the database
        if child_name not in all_children:
            messagebox.showinfo("Error", f"{child_name} does not exist in the database.", parent=self)
            return

        # Check if the current month has been finalized or if the current day is a weekend
        if self.check_month_finalized() or self.check_weekend():
            return

        # Retrieve the attendance data
        attendance_data = self.db_manager.read_attendance()

        # Check if the child is attending on the specified date
        for record in attendance_data:
            if record['date'] == str(self.date) and record['name'] == child_name:
                break
        else:
            messagebox.showinfo("Error", f"{child_name} is not attending on {self.date}.", parent=self)
            return

        # Remove the child from the attendance data
        attendance_data = [
            record for record in attendance_data
            if record['name'] != child_name or record['date'] != str(self.date)
        ]

        # Write the updated attendance data to the database
        self.db_manager.write_attendance(attendance_data)

        # Update the window labels
        self.update_labels()

    def check_month_finalized(self):
        """
        Check if the month has been finalized.
        """
        month = self.date.strftime('%B')
        year = self.date.year
        filename = os.path.join(os.path.dirname(__file__), f'{month}_{year}_EndMonth.csv')
        if os.path.exists(filename):
            messagebox.showinfo("Error", "The month has been finalized. You cannot modify the attendance.", parent=self)
            return True
        return False

    def check_weekend(self):
        """
        Check if the current date is a weekend.
        """
        if self.date.weekday() >= 5:  # 5 and 6 corresponds to Saturday and Sunday
            messagebox.showinfo("Error", "You cannot modify the attendance for weekends.", parent=self)
            return True
        return False
