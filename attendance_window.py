import os
import tkinter as tk
from tkinter import messagebox

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
        super().__init__(parent)
        self.db_manager = db_manager
        self.date = date
        self.title(f"Attendance for {date}")

        attendance = self.get_attendance(str(date))
        if attendance:
            for child in attendance:
                tk.Label(self, text=child).pack()
        else:
            tk.Label(self, text='-').pack()

        all_children = self.get_all_children()
        child_name = tk.StringVar(self)
        child_name.set(all_children[0])
        child_menu = tk.OptionMenu(self, child_name, *all_children)
        child_menu.pack()

        tk.Button(self, text='Add', command=lambda: self.add_child_to_attendance(child_name.get())).pack(fill='x')
        tk.Button(self, text='Remove', command=lambda: self.remove_child_from_attendance(child_name.get())).pack(
            fill='x')
        tk.Button(self, text='Exit', command=self.destroy).pack(fill='x')

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
        if self.check_month_finalized():
            return

        attendance_data = self.db_manager.read_attendance()
        for record in attendance_data:
            if record['date'] == str(self.date) and record['name'] == child_name:
                messagebox.showinfo("Error", f"{child_name} is already attending on {self.date}.", parent=self)
                return

        attendance_data.append({'date': str(self.date), 'name': child_name})
        self.db_manager.write_attendance(attendance_data)

        self.destroy()
        AttendanceWindow(self.master, self.db_manager, self.date)

    def remove_child_from_attendance(self, child_name):
        """
        Remove a child from the attendance for the current date.
        """
        if self.check_month_finalized():
            return

        attendance_data = self.db_manager.read_attendance()
        for record in attendance_data:
            if record['date'] == str(self.date) and record['name'] == child_name:
                break
        else:
            messagebox.showinfo("Error", f"{child_name} is not attending on {self.date}.", parent=self)
            return

        attendance_data = [
            record for record in attendance_data
            if record['name'] != child_name or record['date'] != str(self.date)
        ]
        self.db_manager.write_attendance(attendance_data)
        self.destroy()
        AttendanceWindow(self.master, self.db_manager, self.date)

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
