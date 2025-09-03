import os
import psutil
import hashlib
import time
import socket
import threading
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(filename='defender.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Known malware hashes (example, in real use, load from database)
KNOWN_MALWARE_HASHES = {
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',  # example hash
    '9bf5ce6d9ffa13e30342a62a6dec17fd56556b36f2ceb5533ba9263931311c9b',  # test_malware.exe hash
    # Add more hashes here
}

# Suspicious file extensions
SUSPICIOUS_EXTENSIONS = ['.exe', '.dll', '.bat', '.scr', '.pif', '.com']

# Suspicious processes (example)
SUSPICIOUS_PROCESSES = ['malware.exe', 'virus.exe']

class SystemDefender:
    def __init__(self):
        self.scanned_files = set()
        self.blocked_ips = set()

    def calculate_hash(self, file_path):
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except (OSError, IOError):
            return None

    def scan_file(self, file_path):
        """Scan a file for malware."""
        if file_path in self.scanned_files:
            return
        self.scanned_files.add(file_path)
        file_hash = self.calculate_hash(file_path)
        if file_hash and file_hash in KNOWN_MALWARE_HASHES:
            print(f"Malware detected: {file_path}")
            logging.warning(f"Malware detected: {file_path}")
            self.destroy_file(file_path)
        elif Path(file_path).suffix.lower() in SUSPICIOUS_EXTENSIONS:
            print(f"Suspicious file: {file_path}")
            logging.info(f"Suspicious file: {file_path}")

    def scan_directory(self, directory):
        """Scan a directory recursively."""
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                self.scan_file(file_path)

    def monitor_processes(self):
        """Monitor running processes."""
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                if proc.info['name'] in SUSPICIOUS_PROCESSES:
                    print(f"Suspicious process: {proc.info['name']} (PID: {proc.info['pid']})")
                    logging.warning(f"Suspicious process: {proc.info['name']} (PID: {proc.info['pid']})")
                    self.kill_process(proc.info['pid'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def kill_process(self, pid):
        """Kill a process by PID."""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=3)
            print(f"Terminated process PID: {pid}")
            logging.info(f"Terminated process PID: {pid}")
        except psutil.NoSuchProcess:
            print(f"Process PID: {pid} already terminated")
            logging.info(f"Process PID: {pid} already terminated")
        except psutil.TimeoutExpired:
            proc.kill()
            print(f"Killed process PID: {pid}")
            logging.info(f"Killed process PID: {pid}")

    def destroy_file(self, file_path):
        """Delete a malicious file."""
        try:
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
            logging.info(f"Deleted file: {file_path}")
        except OSError as e:
            print(f"Failed to delete {file_path}: {e}")
            logging.error(f"Failed to delete {file_path}: {e}")

    def monitor_network(self):
        """Monitor network connections (basic)."""
        # This is a simple example; for advanced, use scapy
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', 0))
            s.listen(1)
            s.settimeout(1)
            conn, addr = s.accept()
            if addr[0] in self.blocked_ips:
                conn.close()
                logging.info(f"Blocked connection from: {addr[0]}")
            else:
                # Check for suspicious activity
                data = conn.recv(1024)
                if b'malicious' in data:  # example
                    self.blocked_ips.add(addr[0])
                    logging.warning(f"Suspicious connection from: {addr[0]}")
                conn.close()
        except socket.timeout:
            pass
        except Exception as e:
            logging.error(f"Network monitoring error: {e}")

    def defend(self):
        """Main defense loop."""
        for i in range(3):  # Test mode: run 3 times
            # Scan test directory
            self.scan_directory('test')
            # Monitor processes
            self.monitor_processes()
            # Monitor network
            self.monitor_network()
            time.sleep(1)  # Short sleep for test

def main():
    defender = SystemDefender()
    logging.info("System Defender AI started")
    # For test, run defend directly
    defender.defend()

if __name__ == "__main__":
    main()
