"""
What is Logging?
----------------
Logging in Python is a way to record events that happen while your program runs.
Instead of using print() statements, logging provides a flexible system to 
track, debug, and monitor your code in production.

Why Use Logging?
----------------
1. Better than print() - you can control *where* the logs go (console, file, etc.)
2. Different severity levels (info, warning, error, etc.)
3. Useful for debugging issues in production without modifying code.
4. Helps in troubleshooting and auditing what happened.

Logging Levels (in increasing order of severity)
------------------------------------------------
DEBUG    - Detailed information, mostly useful for developers.
INFO     - Confirmation that things are working as expected.
WARNING  - Something unexpected happened, but the program still works.
ERROR    - A serious problem; program failed to do something.
CRITICAL - Very serious error; program may not continue running.
"""

"""
logging.basicConfig(
    *,
    filename=None,             # Default: None → logs go to sys.stderr (unless handlers/stream is set)
    filemode='a',              # Default: 'a' → append mode if filename is set
    format=None,               # Default: None → uses "%(levelname)s:%(name)s:%(message)s"
    datefmt=None,              # Default: None → asctime shown as "YYYY-MM-DD HH:MM:SS,mmm"
    style='%',                 # Default: '%' → printf-style formatting
    level=logging.WARNING,     # Default: logging.WARNING (only WARNING and above are logged)
    stream=None,               # Default: None → sys.stderr (ignored if filename is set)
    handlers=None,             # Default: None → introduced in Python 3.3
    force=False,               # Default: False → won’t reconfigure logging if already set
    encoding=None,             # Default: None → platform default encoding (if filename is set)
    errors='backslashreplace'  # Default: 'backslashreplace' → handles encoding errors
)
"""
# usage: netmiko_with_logging.py [-h] --ip  --command
import logging
from netmiko import ConnectHandler
import argparse


logging.basicConfig(
    handlers=[
        logging.FileHandler("device.log"),     # Save logs to file
        logging.StreamHandler()                # Show logs in console
    ],
    level=logging.INFO,                 # log everything from INFO and above
    format="%(asctime)s - %(levelname)s - %(message)s", # Show timestamp, log level, and your message
    datefmt="%Y-%m-%d %H:%M:%S"  # Format the timestamp (YYYY-MM-DD HH:MM:SS)
)

# Create parser
parser = argparse.ArgumentParser(description="Run command on network device")
parser.add_argument("--ip", required=True, help="IP address of the device", metavar="")
parser.add_argument("--command", required=True, help="Command to run on the device", metavar="")
args = parser.parse_args()

# Device connection details
device = {
    "device_type": "cisco_ios_telnet",
    "host": args.ip,
    "username": "rviews",
    "password": "rviews",
}

try:
    logging.info(f"Connecting to device {args.ip}")
    net_connect = ConnectHandler(**device)

    logging.info("Sending command to device")
    output = net_connect.send_command(args.command)

    # Save output to a file
    filename = f"{args.ip}.txt"
    with open(filename, "w") as f:
        f.write(output)

    logging.info(f"Command successfully executed on {args.ip}. Output saved to {filename}")

except Exception as e:
    logging.error(f"Failed to connect to {args.ip} - {str(e)}")
