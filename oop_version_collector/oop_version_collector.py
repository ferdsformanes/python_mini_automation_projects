# Automate Device Version Info Collection Using Python Class and Netmiko

# Introduction
# - Automatically collect 'show version' output from network devices using Python and Netmiko.
# - This script gathers system information (not full configuration) and saves it to uniquely named files.
# - Each file includes a readable timestamp for easy identification and tracking.

# Step 1: Import Required Modules
from netmiko import ConnectHandler
from datetime import datetime  # For timestamping filenames

# Step 2: Define the NetworkDevice Class
class NetworkDevice:
    def __init__(self, hostname, device_type, username=None):
        self.hostname = hostname
        self.device_type = device_type
        self.username = username

    def collect_version_info(self):
        # Step 3: Connect to the device using Netmiko
        connection = ConnectHandler(
            device_type=self.device_type,
            host=self.hostname,
            username=self.username
        )

        # Step 4: Run 'show version' command to collect system info
        output = connection.send_command("show version")
        connection.disconnect()

        # Step 5: Generate timestamped filename
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.hostname}_show_version_{timestamp}.txt"

        # Step 6: Save output to the file
        with open(filename, "w") as file:
            file.write(output)
        print(f"'show version' info saved for {self.hostname} in {filename}")

# Step 7: Create Device Objects
device1 = NetworkDevice(
    hostname="route-views.routeviews.org",
    device_type="cisco_ios_telnet",
    username="rviews"
)

device2 = NetworkDevice(
    hostname="route-views2.routeviews.org",
    device_type="cisco_ios_telnet"
)

# Step 8: Collect 'show version' Output from Each Device
device1.collect_version_info()
device2.collect_version_info()

