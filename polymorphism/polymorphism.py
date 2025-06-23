# Python Polymorphism in Network Automation

# What is Polymorphism?
# Polymorphism is an object-oriented programming (OOP) concept where different classes 
# define methods with the same name, but with different behaviors.

# This means you can call the same method on different objects, and Python will automatically 
# run the correct version — based on the object's class.

# Why is it called "Polymorphism"?
# The word comes from Greek: "poly" means many, and "morph" means form.
# So, polymorphism means "many forms" — the same method name can behave differently 
# depending on which class implements it.

# Why and When Do We Use Polymorphism?
# - To call the same method on different objects, with each responding differently.
# - Makes code flexible and scalable — add new device types without changing main logic.
# - Useful in network automation for handling multi-vendor devices with shared method names.

# In this example, we reuse a parent class for network devices 
# and override a method in the child classes to customize behavior 
# for Cisco and Juniper devices.

# Step 1: Import Required Modules
from netmiko import ConnectHandler
from datetime import datetime

# Step 2: Define the Parent Class
class NetworkDevice:
    def __init__(self, hostname, device_type="cisco_ios_telnet", username=None, password=""):
        self.hostname = hostname
        self.device_type = device_type
        self.username = username
        self.password = password

    # Define a generic method to run a show command
    def run_show_command(self):
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username,
            password=self.password
        )
        output = connection.send_command("show version")  # Default command
        connection.disconnect()

        # Save the output with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_show_version_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(output)
        print(f"'show version' info saved for {self.hostname} in {filename}")

# Step 3: Create Child Class for Cisco Devices
class CiscoTelnetDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews", password=""):
        # Use cisco_ios_telnet device_type
        super().__init__(hostname, device_type="cisco_ios_telnet", username=username, password=password)

    # Override the method to send a Cisco-specific command
    def run_show_command(self):
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username,
            password=self.password
        )
        output = connection.send_command("show ip bgp summary")
        connection.disconnect()

        # Save the output with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_bgp_summary_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(output)
        print(f"'show ip bgp summary' saved for {self.hostname} in {filename}")

# Step 4: Create Child Class for Juniper Devices
class JuniperDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews", password=""):
        # Use juniper_junos_telnet device_type
        super().__init__(hostname, device_type="juniper_junos_telnet", username=username, password=password)

    # Override the method to send a Juniper-specific command
    def run_show_command(self):
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username,
            password=self.password
        )
        output = connection.send_command("show bgp summary")
        connection.disconnect()

        # Save the output with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_juniper_bgp_summary_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(output)
        print(f"'show bgp summary' saved for {self.hostname} in {filename}")

# Step 5: Instantiate Device Objects
cisco_device = CiscoTelnetDevice(
    hostname="route-views.routeviews.org",
    username="rviews",
)

juniper_device = JuniperDevice(
    hostname="route-server.ip.att.net",
    username="rviews",
    password="rviews"
)

# Step 6: Demonstrate Polymorphism
# This is where polymorphism occurs — we call the same method 'run_show_command()'
# on each object, and Python automatically uses the correct version based on the class.
devices = [cisco_device, juniper_device]


for device in devices:
    device.run_show_command()
