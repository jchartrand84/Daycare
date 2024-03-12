import tkinter as tk
from daycare_database_app import DaycareDatabaseApp

"""
main.py

This file is the entry point of the Daycare Database Application. It initializes the Tkinter root window and the
DaycareDatabaseApp, and then starts the Tkinter event loop.
"""


if __name__ == "__main__":
    """
    This condition checks if this file is the entry point of the program. If it is, it creates a new Tkinter window,
    initializes the DaycareDatabaseApp with this window, and starts the Tkinter event loop.
    """
    root = tk.Tk()
    app = DaycareDatabaseApp(root)
    root.mainloop()
