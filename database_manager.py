import csv
import os
from tkinter import messagebox

"""
database_manager.py

This file contains the DatabaseManager class which is responsible for managing the interactions with the database.
It provides functionality for reading and writing to the database, as well as reading attendance data and writing
attendance data.
"""


class DatabaseManager:
    """
    The DatabaseManager class manages the interactions with the database.
    """
    def __init__(self, database_filename='daycare_database.csv', attendance_filename='attendance.csv'):
        """
        Initialize the DatabaseManager.
        """
        self.database_filename = os.path.join(os.path.dirname(__file__), database_filename)
        self.attendance_filename = os.path.join(os.path.dirname(__file__), attendance_filename)

    def is_name_unique(self, name):
        """
        Check if a name is unique in the database.
        """
        data = self.read_database()
        for row in data:
            if row['name'].lower() == name.lower():
                return False
        return True

    def read_database(self):
        """
        Read the current database of children and their balances.
        """
        if not os.path.exists(self.database_filename):
            return []
        with open(self.database_filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def write_database(self, data):
        """
        Write the updated data back to the database.
        """
        with open(self.database_filename, mode='w', newline='') as file:
            fieldnames = ['name', 'age', 'balance']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                row['balance'] = "{:.2f}".format(float(row['balance']))
                writer.writerow(row)

    def read_attendance(self):
        """
        Read the current attendance data.
        """
        if not os.path.exists(self.attendance_filename):
            return []
        with open(self.attendance_filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            return list(reader)

    def write_attendance(self, data):
        """
        Write the updated attendance data.
        """
        try:
            # Count the number of children for the given date
            date_counts = {}
            for row in data:
                date_counts[row['date']] = date_counts.get(row['date'], 0) + 1
                if date_counts[row['date']] > 6:
                    raise ValueError("Daily Capacity (6) has been reached.\nChild cannot be added to attendance.")

            with open(self.attendance_filename, mode='w', newline='') as file:
                fieldnames = ['date', 'name']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
