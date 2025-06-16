# Python Class Inheritance in Network Automation

# What is Inheritance?
# Inheritance is a core concept in object-oriented programming (OOP) where a child class 
# inherits attributes and methods from a parent class. This allows code reuse and a clear 
# hierarchical structure, making it easier to manage common behavior across multiple device types.
#
# In this example, we will create a parent class for network devices and a child class for Cisco devices.
#
# Step 1: Import Required Modules
from netmiko import ConnectHandler
from datetime import datetime

# Step 2: Define the Parent Class
class NetworkDevice:
    def __init__(self, hostname, device_type, username=None):
        self.hostname = hostname
        self.device_type = device_type
        self.username = username

    def collect_version_info(self):
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username
        )
        output = connection.send_command("show version")
        connection.disconnect()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_show_version_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(output)
        print(f"'show version' info saved for {self.hostname} in {filename}")

# Step 3: Create Child Class for Cisco Devices
class CiscoTelnetDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews"):
        super().__init__(hostname, device_type="cisco_ios_telnet", username=username)

# Step 4: Instantiate Device Objects
device1 = CiscoTelnetDevice(hostname="route-views.routeviews.org")
device2 = CiscoTelnetDevice(hostname="route-views2.routeviews.org")

# Step 5: Run the Method to Collect Info
device1.collect_version_info()
device2.collect_version_info()
