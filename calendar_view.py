import tkinter as tk
from tkcalendar import Calendar
import datetime
import os
from tkinter import messagebox
from attendance_window import AttendanceWindow
import csv

"""
calendar_view.py

This file contains the CalendarView class which is responsible for managing the calendar view window.
It provides functionality for navigating through months and selecting a date to view attendance.
"""


class CalendarView(tk.Toplevel):
    """
    The CalendarView class manages the calendar view window.
    """
    def __init__(self, parent, db_manager):
        """
        Initialize the CalendarView with a parent Tkinter window and a DatabaseManager.
        """
        super().__init__(parent)
        self.cal = None
        self.db_manager = db_manager
        self.title("Calendar View")
        self.setup_calendar()

    def setup_calendar(self):
        """
        Set up the calendar with the current date and add buttons for editing the date, exiting the calendar,
        and ending the month.
        """
        current_date = datetime.datetime.now()
        self.cal = Calendar(self, selectmode='day', year=current_date.year, month=current_date.month,
                            day=current_date.day, showweeknumbers=False)
        self.cal.pack(padx=10, pady=10)
        self.cal.selection_set(current_date)

        tk.Button(self, text='Edit Date', command=lambda: self.open_attendance_window(self.cal.selection_get())).pack(
            fill='x')
        tk.Button(self, text='Exit', command=self.destroy).pack(fill='x')
        tk.Button(self, text='End Month', command=self.end_month).pack(fill='x')  # Removed lambda function

    def open_attendance_window(self, date):
        """
        Open the attendance window for a specific date.
        """
        AttendanceWindow(self, self.db_manager, date)

    def end_month(self):
        """
        Finalize the month, calculate the total attendance for each child, update the children's balances, and export
        the attendance data to a CSV file.
        """
        # Ask the user for confirmation before ending the month
        if messagebox.askyesno("End Month", "Are you sure you want to end the month? This action is final."):
            date = self.cal.selection_get()
            month = date.strftime('%B')
            year = date.year
            filename = os.path.join(os.path.dirname(__file__), f'{month}_{year}_EndMonth.csv')
            if os.path.exists(filename):
                messagebox.showinfo("Error", "This month has already been finalized.", parent=self)
                return

            attendance_data = self.db_manager.read_attendance()
            attendance_data = [record for record in attendance_data if
                               datetime.datetime.strptime(record['date'], '%Y-%m-%d').strftime('%B') == month]

            total_attendance = {}
            for record in attendance_data:
                if record['name'] not in total_attendance:
                    total_attendance[record['name']] = 0
                total_attendance[record['name']] += 1

            children_data = self.db_manager.read_database()
            for child in children_data:
                if child['name'] in total_attendance:
                    child['balance'] = str(float(child['balance']) + 40 * total_attendance[child['name']])

            self.db_manager.write_database(children_data)

            with open(filename, mode='w', newline='') as file:
                fieldnames = ['date', 'name']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(attendance_data)

            messagebox.showinfo("Success", f"The month has been finalized and exported to {filename}", parent=self)
        else:
            # If the user clicked "No", show a message and do nothing
            messagebox.showinfo("Cancelled", "End month cancelled.")
