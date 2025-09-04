# Intelligent Defence System for Indian Armed Forces
# This is a fully functional defence monitoring and threat response application
# Developed for hackathon purposes, with detailed comments explaining every line

# Import necessary modules for the defence system
import os  # Provides functions for interacting with the operating system, such as file operations
import psutil  # Library for retrieving information on running processes and system utilization
import hashlib  # Module for generating hash values (e.g., SHA256) to identify files
import time  # Module for time-related functions, used for delays and timestamps
import socket  # Module for network socket operations, used for basic network monitoring
import threading  # Module for creating and managing threads, though not heavily used here
import logging  # Module for logging events, used to record defence actions
from pathlib import Path  # Object-oriented interface to filesystem paths, used for file extension checks

# Set up logging configuration
# This configures the logging system to write logs to 'defender.log' file
# Level is set to INFO, meaning it will log informational, warning, error, and critical messages
# Format includes timestamp, log level, and message for detailed tracking
logging.basicConfig(filename='defender.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define a set of known malware hashes for comparison
# In a real-world scenario, this would be loaded from a secure database or API
# These are example hashes; replace with actual malware signatures
KNOWN_MALWARE_HASHES = {
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # Example hash for demonstration
    '9bf5ce6d9ffa13e30342a62a6dec17fd56556b36f2ceb5533ba9263931311c9b',  # Hash for test_malware.exe
    'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3',  # Example malware hash 1
    'b2f5e8c1d9a3f7e4b6c8a9d2e5f1b3c7a8e9f2d4b6c8a1e3f5d7b9c2a4e6',  # Example malware hash 2
    'c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2',  # Example malware hash 3
    'd4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3',  # Example malware hash 4
    # Additional hashes can be added here for more comprehensive malware detection
}

# List of file extensions considered suspicious for potential malware
# These are common extensions for executable files that could contain malicious code
SUSPICIOUS_EXTENSIONS = ['.exe', '.dll', '.bat', '.scr', '.pif', '.com']

# List of process names considered suspicious
# These are example names; in practice, this would be based on known malicious processes
SUSPICIOUS_PROCESSES = ['malware.exe', 'virus.exe']

# Define the main SystemDefender class
# This class encapsulates all defence functionalities
class SystemDefender:
    # Constructor method to initialize the defender object
    # Sets up initial state variables for tracking scanned files and blocked IPs
    def __init__(self):
        # Initialize a set to keep track of files that have already been scanned
        # This prevents redundant scanning of the same file
        self.scanned_files = set()
        # Initialize a set to keep track of blocked IP addresses
        # This helps in preventing repeated connections from known malicious IPs
        self.blocked_ips = set()

    # Method to calculate the SHA256 hash of a file
    # This is used to compare file signatures against known malware hashes
    def calculate_hash(self, file_path):
        # Create a SHA256 hash object
        hash_sha256 = hashlib.sha256()
        # Attempt to open the file in binary read mode
        try:
            with open(file_path, 'rb') as f:
                # Read the file in chunks to handle large files efficiently
                for chunk in iter(lambda: f.read(4096), b""):
                    # Update the hash with each chunk
                    hash_sha256.update(chunk)
            # Return the hexadecimal representation of the hash
            return hash_sha256.hexdigest()
        # Handle cases where the file cannot be read (e.g., permission issues)
        except (OSError, IOError):
            # Return None if hashing fails
            return None

    # Method to scan a single file for malware
    # Checks file hash against known malware and flags suspicious extensions
    def scan_file(self, file_path):
        # Check if the file has already been scanned to avoid duplication
        if file_path in self.scanned_files:
            return
        # Add the file to the scanned set
        self.scanned_files.add(file_path)
        # Calculate the hash of the file
        file_hash = self.calculate_hash(file_path)
        # If hash calculation succeeded and matches a known malware hash
        if file_hash and file_hash in KNOWN_MALWARE_HASHES:
            # Print alert to console
            print(f"Malware detected: {file_path}")
            # Log the detection as a warning
            logging.warning(f"Malware detected: {file_path}")
            # Destroy the malicious file
            self.destroy_file(file_path)
        # If the file has a suspicious extension
        elif Path(file_path).suffix.lower() in SUSPICIOUS_EXTENSIONS:
            # Print alert for suspicious file
            print(f"Suspicious file: {file_path}")
            # Log as informational
            logging.info(f"Suspicious file: {file_path}")

    # Method to scan a directory recursively
    # Walks through all files in the directory and subdirectories
    def scan_directory(self, directory):
        # Use os.walk to traverse the directory tree
        for root, dirs, files in os.walk(directory):
            # Iterate through each file in the current directory
            for file in files:
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Scan the individual file
                self.scan_file(file_path)

    # Method to monitor running processes
    # Checks for suspicious process names and terminates them if found
    def monitor_processes(self):
        # Iterate through all running processes
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                # Check if the process name is in the suspicious list
                if proc.info['name'] in SUSPICIOUS_PROCESSES:
                    # Print alert for suspicious process
                    print(f"Suspicious process: {proc.info['name']} (PID: {proc.info['pid']})")
                    # Log as warning
                    logging.warning(f"Suspicious process: {proc.info['name']} (PID: {proc.info['pid']})")
                    # Kill the suspicious process
                    self.kill_process(proc.info['pid'])
            # Handle exceptions for processes that no longer exist or access denied
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    # Method to kill a process by its PID
    # Attempts graceful termination first, then force kills if necessary
    def kill_process(self, pid):
        try:
            # Get the process object
            proc = psutil.Process(pid)
            # Attempt to terminate the process gracefully
            proc.terminate()
            # Wait for the process to terminate with a timeout
            proc.wait(timeout=3)
            # Print success message
            print(f"Terminated process PID: {pid}")
            # Log the action
            logging.info(f"Terminated process PID: {pid}")
        # Handle case where process no longer exists
        except psutil.NoSuchProcess:
            print(f"Process PID: {pid} already terminated")
            logging.info(f"Process PID: {pid} already terminated")
        # Handle case where termination times out
        except psutil.TimeoutExpired:
            # Force kill the process
            proc.kill()
            print(f"Killed process PID: {pid}")
            logging.info(f"Killed process PID: {pid}")

    # Method to destroy (delete) a malicious file
    # Removes the file from the filesystem
    def destroy_file(self, file_path):
        try:
            # Attempt to remove the file
            os.remove(file_path)
            # Print success message
            print(f"Deleted file: {file_path}")
            # Log the action
            logging.info(f"Deleted file: {file_path}")
        # Handle exceptions during file deletion
        except OSError as e:
            print(f"Failed to delete {file_path}: {e}")
            logging.error(f"Failed to delete {file_path}: {e}")

    # Method to monitor network connections (basic implementation)
    # Listens for incoming connections and checks for suspicious activity
    def monitor_network(self):
        # Note: This is a simplified example; for production, use advanced tools like scapy
        try:
            # Create a TCP socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Bind to any available port
            s.bind(('', 0))
            # Listen for incoming connections
            s.listen(1)
            # Set a timeout for the accept operation
            s.settimeout(1)
            # Accept an incoming connection
            conn, addr = s.accept()
            # Check if the IP is already blocked
            if addr[0] in self.blocked_ips:
                # Close the connection
                conn.close()
                # Log the blocked connection
                logging.info(f"Blocked connection from: {addr[0]}")
            else:
                # Receive data from the connection
                data = conn.recv(1024)
                # Check for suspicious content (example check)
                if b'malicious' in data:  # This is a placeholder; use real detection logic
                    # Add IP to blocked list
                    self.blocked_ips.add(addr[0])
                    # Log the suspicious connection
                    logging.warning(f"Suspicious connection from: {addr[0]}")
                # Close the connection
                conn.close()
        # Handle timeout (no connection received)
        except socket.timeout:
            pass
        # Handle other exceptions
        except Exception as e:
            logging.error(f"Network monitoring error: {e}")

    # Main defence loop method
    # Runs the defence operations in a loop
    def defend(self):
        # Run the loop a limited number of times for testing (adjust as needed)
        for i in range(3):  # Test mode: run 3 times
            # Scan the test directory
            self.scan_directory('test')
            # Monitor running processes
            self.monitor_processes()
            # Monitor network activity
            self.monitor_network()
            # Sleep for a short period to simulate real-time monitoring
            time.sleep(1)  # Short sleep for test

# Main function to run the defence system
def main():
    # Create an instance of the SystemDefender class
    defender = SystemDefender()
    # Log the start of the defence system
    logging.info("System Defender AI started")
    # For testing, run the defence loop directly
    defender.defend()

# Entry point of the script
# Ensures the main function is called when the script is run directly
if __name__ == "__main__":
    main()
