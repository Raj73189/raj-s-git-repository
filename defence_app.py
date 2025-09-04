# CLI Application for Intelligent Defence System
# This app provides an interactive command-line interface to use the SystemDefender class
# Developed for monitoring and threat response for the Indian Armed Forces

import sys
import time
import logging
from raj9 import SystemDefender  # Import the SystemDefender class from raj9.py

# Function to display the main menu options
def display_menu():
    print("\n=== Intelligent Defence System ===")
    print("1. Start full system scan")
    print("2. Monitor running processes")
    print("3. View defender log")
    print("4. Exit")

# Function to read and display the defender log file
def view_log():
    try:
        with open('defender.log', 'r') as log_file:
            print("\n--- Defender Log ---")
            print(log_file.read())
            print("--- End of Log ---\n")
    except FileNotFoundError:
        print("Log file not found. No logs available yet.")

# Main function to run the CLI app
def main():
    # Create an instance of the SystemDefender
    defender = SystemDefender()
    logging.info("Defence App started")

    while True:
        # Display the menu options
        display_menu()
        # Get user input
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            print("Starting full system scan...")
            # Scan the 'test' directory as example
            defender.scan_directory('test')
            print("Scan completed.")
        elif choice == '2':
            print("Monitoring running processes...")
            # Monitor processes once
            defender.monitor_processes()
            print("Process monitoring completed.")
        elif choice == '3':
            # Display the defender log
            view_log()
        elif choice == '4':
            print("Exiting the Defence System app. Stay safe!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

        # Small delay before showing menu again
        time.sleep(1)

if __name__ == "__main__":
    main()
