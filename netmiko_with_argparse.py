"""
argparse is a Python module for parsing command-line arguments with built-in validation and auto-generated help.

📌 Example:
    python netmiko_with_argparse.py --ip 192.168.1.1 --username admin --password cisco123 --command "show version"

📌 Help:
    python netmiko_with_argparse.py --help
"""

import argparse 
from netmiko import ConnectHandler

# Create an ArgumentParser object to handle command-line input
parser = argparse.ArgumentParser(description="Connect to a device and run a command")

# Define command-line arguments
parser.add_argument("--ip", required=True, help="IP address of the device", metavar="")  # name shown in help
parser.add_argument("--username", required=True, help="Login username", metavar="")  # name shown in help
parser.add_argument("--password", required=True, help="Login password", metavar="")  # name shown in help
parser.add_argument("--device_type", default="cisco_ios_telnet", help="Netmiko device type (default: cisco_ios_telnet)", metavar="")  # name shown in help
parser.add_argument("--command", required=True, help="Command to send to the device", metavar="")  # name shown in help

# Parse arguments into a Namespace object (acts like a container for the arguments)
# It holds the parsed arguments as attributes.
args = parser.parse_args()

# Build device dictionary for Netmiko using parsed arguments
device = {
    "device_type": args.device_type,
    "host": args.ip,
    "username": args.username,
    "password": args.password,
}

# Connect to device and run the given command
with ConnectHandler(**device) as net_connect:
    output = net_connect.send_command(args.command)
    print(output)
