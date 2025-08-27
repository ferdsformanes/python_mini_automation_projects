import sys
from netmiko import ConnectHandler

# Check if enough arguments are passed
if len(sys.argv) < 5:
    print("Usage: python netmiko_connect.py <IP> <username> <password> <command>")
    sys.exit(1)

# Extract arguments
ip = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
command = ' '.join(sys.argv[4:])  # Support multi-word commands

# Define device
device = {
    'device_type': 'cisco_ios_telnet',  # Change based on your device
    'host': ip,
    'username': username,
    'password': password,
}

# Connect and run command
try:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command(command)
    print(output)
    net_connect.disconnect()
except Exception as e:
    print(f"Connection failed: {e}")
