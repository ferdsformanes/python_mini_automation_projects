"""
Python Logging Advanced (Rotating Logs, Multiple Handlers)
----------------------------------------------------------

This script demonstrates:
1. Rotating Logs → Automatically rotate log files once they reach a size limit.
2. Multiple Handlers → Send logs to multiple destinations (e.g., console + file).
3. Different Log Levels per Handler → Control verbosity for console vs file.
4. Example use case: Network automation with Netmiko.

Why Advanced Logging?
---------------------
- Prevents huge log files by rotating them.
- Allows sending detailed logs to a file while keeping console logs clean.
- Essential for production-level network automation and troubleshooting.
"""

import logging
from logging.handlers import RotatingFileHandler
from netmiko import ConnectHandler
import argparse

# ------------------------------------------------------
# 1. Setup logging with multiple handlers
# ------------------------------------------------------

# Create a custom logger
logger = logging.getLogger("network_automation")
logger.setLevel(logging.DEBUG)  # Capture all logs at DEBUG level and above

# Console handler → INFO level (less verbose for user)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Rotating file handler → DEBUG level (detailed logs for troubleshooting)
file_handler = RotatingFileHandler(
    "advanced_device.log",   # Log file name
    maxBytes=5000,           # Max size of log file before rotating (bytes)
    backupCount=3,           # Keep 3 old log files
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# Create log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", 
                              datefmt="%Y-%m-%d %H:%M:%S")
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# ------------------------------------------------------
# 2. Configure argparse to accept IP and command
# ------------------------------------------------------
parser = argparse.ArgumentParser(description="Run command on network device")
parser.add_argument("--ip", required=True, help="IP address of the device", metavar="")
parser.add_argument("--command", required=True, help="Command to run on the device", metavar="")
args = parser.parse_args()

# ------------------------------------------------------
# 3. Create device dictionary for Netmiko
# ------------------------------------------------------
device = {
    "device_type": "cisco_ios_telnet",
    "host": args.ip,
    "username": "rviews",
    "password": "rviews",
}

# ------------------------------------------------------
# 4. Use try/except for connection and command execution
# ------------------------------------------------------
try:
    logger.info(f"Connecting to device {args.ip}")
    net_connect = ConnectHandler(**device)

    logger.info("Sending command to device")
    output = net_connect.send_command(args.command)

    # Save output to file
    filename = f"{args.ip}.txt"
    with open(filename, "w") as f:
        f.write(output)

    logger.info(f"Command executed on {args.ip}. Output saved to {filename}")

except Exception as e:
    logger.error(f"Failed to connect to {args.ip} - {str(e)}")
