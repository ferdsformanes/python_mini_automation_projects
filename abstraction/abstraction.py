# Python Abstraction in Network Automation

# What is Abstraction?
# Abstraction means defining a common method in a base class,
# but letting child classes handle the actual details.

# It hides the complexity and shows only what matters.

# In Python, we use the 'abc' module to create abstract base classes.

# Why Use Abstraction in Network Automation?
# - Ensures all device classes follow the same structure
# - Requires child classes to implement key methods
# - Makes your code more organized and easier to scale
# - Useful for frameworks and multi-vendor support

# In this example, we’ll use abstraction to make sure
# all devices implement a method to run a show command.

# Step 1: Import Required Modules
from abc import ABC, abstractmethod
from netmiko import ConnectHandler
from datetime import datetime

# Step 2: Define an Abstract Base Class
class NetworkDevice(ABC):
    def __init__(self, hostname, device_type, username, password):
        self.hostname = hostname
        self.device_type = device_type
        self.username = username
        self.password = password

    # This method must be implemented by all child classes
    @abstractmethod
    def run_show_command(self):
        pass

# Step 3: Implement Cisco Device Class
class CiscoDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews", password=""):
        # Use cisco_ios_telnet as the device type
        super().__init__(hostname, device_type="cisco_ios_telnet", username=username, password=password)

    # Implementation of the abstract method
    def run_show_command(self):
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username,
            password=self.password
        )
        output = connection.send_command("show ip bgp summary")
        connection.disconnect()

        # Save output with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_cisco_bgp_summary_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(output)
        print(f"Cisco: 'show ip bgp summary' saved in {filename}")

# Step 4: Implement Juniper Device Class
class JuniperDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews", password="rviews"):
        # Use juniper_junos_telnet as the device type
        super().__init__(hostname, device_type="juniper_junos_telnet", username=username, password=password)

    # Implementation of the abstract method
    def run_show_command(self):
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username,
            password=self.password
        )
        output = connection.send_command("show bgp summary")
        connection.disconnect()

        # Save output with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_juniper_bgp_summary_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(output)
        print(f"Juniper: 'show bgp summary' saved in {filename}")

# Step 5: Instantiate Device Objects
cisco = CiscoDevice(hostname="route-views.routeviews.org", username="rviews")
juniper = JuniperDevice(hostname="route-server.ip.att.net", username="rviews", password="rviews")

# Step 6: Use Abstraction with Polymorphism
# Even though we call the same method, the behavior differs depending on the class.
devices = [cisco, juniper]

for device in devices:
    device.run_show_command()

# Note:
# If you try to instantiate NetworkDevice directly:
# base = NetworkDevice("1.1.1.1", "cisco_ios", "user", "pass")
# It will raise a TypeError because it's abstract and cannot be instantiated.
