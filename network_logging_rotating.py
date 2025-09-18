"""
Python Logging with Rotating Logs | Network Automation Example
--------------------------------------------------------------

This script shows how to use RotatingFileHandler:
- Rotates log files once they reach a size limit.
- Sends logs to both console and file.
- Example: Running a command on a Cisco device with Netmiko.
"""

import logging
from logging.handlers import RotatingFileHandler
from netmiko import ConnectHandler

# ------------------------------------------------------
# 1. Setup logger and base level
# ------------------------------------------------------
logger = logging.getLogger("network_automation")  # Create a named logger
logger.setLevel(logging.DEBUG)                     # Logger processes DEBUG and above

# ------------------------------------------------------
# 2. Setup console handler (logs shown on screen)
# ------------------------------------------------------
console_handler = logging.StreamHandler()         # Send logs to console
console_handler.setLevel(logging.INFO)            # Console shows INFO and above

# ------------------------------------------------------
# 3. Setup rotating file handler (logs saved to file with rotation)
# ------------------------------------------------------
file_handler = RotatingFileHandler(
    "network_automation.log",  # Log file name
    maxBytes=200,             # Rotate after file reaches ~200 bytes
    backupCount=3,             # Keep 3 old log files
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)              # File logs everything (DEBUG+)

# ------------------------------------------------------
# 4. Setup formatter and apply to handlers
# ------------------------------------------------------
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# ------------------------------------------------------
# 5. Attach handlers to the logger
# ------------------------------------------------------
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# ------------------------------------------------------
# 6. Device details 
# ------------------------------------------------------
device = {
    "device_type": "cisco_ios_telnet",
    "host": "route-views.routeviews.org",   
    "username": "rviews",
    "password": "rviews",
}

command = "show version"

# ------------------------------------------------------
# 7. Connect and run command
# ------------------------------------------------------
try:
    logger.info(f"Connecting to device {device['host']}")
    net_connect = ConnectHandler(**device)

    logger.info(f"Sending command: {command}")
    output = net_connect.send_command(command)
    net_connect.disconnect()

    filename = f"{device['host']}.txt"
    with open(filename, "w") as f:
        f.write(output)

    logger.info(f"Command executed on {device['host']}. Output saved to {filename}")
    

except Exception as e:
    logger.error(f"Failed to connect to {device['host']} - {str(e)}")
