# Backup Network Devices from a CSV File (Using Pandas + Classes)

# Step 1: Import Required Modules
import pandas as pd
from netmiko import ConnectHandler
from datetime import datetime

# Step 2: Define the Base Class
class NetworkDevice:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def backup_config(self):
        pass  # Placeholder to be overridden

    def __str__(self):
        # Defines how the object is shown when printed (class name + hostname + username)
        return f"{self.__class__.__name__}(hostname={self.hostname})"


# Step 3: Define the CiscoDevice Class (Telnet)
class CiscoDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews", password=""):
        super().__init__(hostname, username, password)
        self.device_type = "cisco_ios_telnet"

    def backup_config(self):
        try:
            connection = ConnectHandler(
                device_type=self.device_type,
                host=self.hostname,
                username=self.username,
                password=self.password
            )
            output = connection.send_command("show version")
            connection.disconnect()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"{self.hostname}_cisco_config_{timestamp}.txt"

            with open(filename, "w") as file:
                file.write(output)

            print(f"Cisco: {self.hostname} backup saved to {filename}")
        except Exception as e:
            print(f"Cisco: Failed to back up {self.hostname}: {e}")

            

# Step 4: Define the JuniperDevice Class (Telnet)
class JuniperDevice(NetworkDevice):
    def __init__(self, hostname, username="rviews", password=""):
        super().__init__(hostname, username, password)
        self.device_type = "juniper_junos_telnet"

    def backup_config(self):
        try:
            connection = ConnectHandler(
                device_type=self.device_type,
                host=self.hostname,
                username=self.username,
                password=self.password
            )
            output = connection.send_command("show bgp summary")
            connection.disconnect()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"{self.hostname}_juniper_config_{timestamp}.txt"

            with open(filename, "w") as file:
                file.write(output)

            print(f"Juniper: {self.hostname} backup saved to {filename}")
        except Exception as e:
            print(f"Juniper: Failed to back up {self.hostname}: {e}")

            

# Step 5: Read Devices from CSV using Pandas
devices = []

df = pd.read_csv("devices.csv")  # Load CSV into DataFrame

for _, row in df.iterrows():  # Loop through each row in DataFrame
    if row["device_type"] == "cisco_ios_telnet":
        device = CiscoDevice(hostname=row["hostname"], username=row["username"], password=row["password"])
    elif row["device_type"] == "juniper_junos_telnet":
        device = JuniperDevice(hostname=row["hostname"], username=row["username"], password=row["password"])
    else:
        print(f"Skipping unknown device type: {row['device_type']}")
        continue
    devices.append(device)
    
# Step 6: Back Up All Devices
for device in devices:
    print(f"Backing up {device}...")
    device.backup_config()
