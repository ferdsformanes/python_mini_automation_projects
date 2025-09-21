from netmiko import ConnectHandler

# Device dictionary (public route server for demo)
cisco_device = {
    "device_type": "cisco_ios_telnet",
    "host": "route-views.routeviews.org",  
    "username": "rviews",
    "password": "rviews",
}

def connect_and_run_command(device, command):
    """Connect to a device and run a command"""
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command(command)
        connection.disconnect()
        return output
    except Exception as e:
        return f"Error: {e}"
