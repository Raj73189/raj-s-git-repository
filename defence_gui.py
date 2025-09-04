# GUI Application for Intelligent Defence System
# This app provides a graphical user interface to use the SystemDefender class
# Developed for monitoring and threat response for the Indian Armed Forces

import tkinter as tk
from tkinter import messagebox, scrolledtext
import logging
from raj9 import SystemDefender  # Import the SystemDefender class from raj9.py

# Function to start full system scan
def start_scan():
    defender.scan_directory('test')
    messagebox.showinfo("Scan Complete", "Full system scan completed.")

# Function to monitor processes
def monitor_processes():
    defender.monitor_processes()
    messagebox.showinfo("Monitoring Complete", "Process monitoring completed.")

# Function to view defender log
def view_log():
    try:
        with open('defender.log', 'r') as log_file:
            log_content = log_file.read()
        log_window = tk.Toplevel(root)
        log_window.title("Defender Log")
        log_text = scrolledtext.ScrolledText(log_window, width=80, height=20)
        log_text.insert(tk.END, log_content)
        log_text.pack()
    except FileNotFoundError:
        messagebox.showerror("Error", "Log file not found.")

# Main GUI setup
root = tk.Tk()
root.title("Intelligent Defence System")

# Create an instance of the SystemDefender
defender = SystemDefender()
logging.info("Defence GUI App started")

# Create buttons for actions
scan_button = tk.Button(root, text="Start Full Scan", command=start_scan)
scan_button.pack(pady=10)

monitor_button = tk.Button(root, text="Monitor Processes", command=monitor_processes)
monitor_button.pack(pady=10)

log_button = tk.Button(root, text="View Log", command=view_log)
log_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
