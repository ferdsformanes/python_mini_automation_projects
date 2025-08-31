# sys.argv - sys means system, and argv means argument vector.
# It's a list that contains all the arguments you type in the command line when running a script.
# The first item, sys.argv[0], is always the script name itself.


import sys
from netmiko import ConnectHandler

# STEP 1: Check if enough arguments are passed
# We need at least 4 arguments: IP, username, password, and a command.
if len(sys.argv) < 5:
    print("Usage: python netmiko_connect.py <IP> <username> <password> <command>")
    sys.exit(1)
print(len(sys.argv))
# STEP 2: Extract arguments from sys.argv
print(sys.argv)  # Print all command-line arguments as a list

ip = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]
print(sys.argv[4:])
command = ' '.join(sys.argv[4:])  # Join list into one string

# STEP 3: Define the device dictionary
device = {
    'device_type': 'cisco_ios_telnet',
    'host': ip,
    'username': username,
    'password': password,
}

# STEP 4: Connect to the device and run the command
try:
    # Establish connection
    net_connect = ConnectHandler(**device)
    
    # Send the command provided from sys.argv and capture the output
    output = net_connect.send_command(command)
    print(output)

    net_connect.disconnect()

# STEP 5: Handle errors
except Exception as e:
    print(f"Connection failed: {e}")
