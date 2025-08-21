# Step 1: Import Required Modules
import pandas as pd
from netmiko import ConnectHandler
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed  # For concurrent execution using threads
import time  # For measuring execution time

# Step 2: Define the Base Class for Network Devices
class NetworkDevice:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def backup_config(self):
        pass  # To be implemented by subclasses
    def __str__(self):
        # Defines string representation of the object
        return f"{self.__class__.__name__}(hostname={self.hostname})"

# Step 3: Define the CiscoDevice Class (inherits from NetworkDevice)
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
            output = connection.send_command("show version")  # Fetch device version info
            connection.disconnect()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"{self.hostname}_cisco_config_{timestamp}.txt"

            with open(filename, "w") as file:
                file.write(output)
            return f"Cisco: {self.hostname} backup saved to {filename}"
        except Exception as e:
            return f"Cisco: Failed to back up {self.hostname}: {e}"

# Step 4: Define the JuniperDevice Class (inherits from NetworkDevice)
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
            output = connection.send_command("show bgp summary")  # Fetch BGP summary
            connection.disconnect()

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"{self.hostname}_juniper_config_{timestamp}.txt"

            with open(filename, "w") as file:
                file.write(output)
            return f"Juniper: {self.hostname} backup saved to {filename}"
        except Exception as e:
            return f"Juniper: Failed to back up {self.hostname}: {e}"

# Step 5: Read Device Information from CSV using Pandas
devices = []
df = pd.read_csv("devices.csv")  # Load device data from CSV file

for _, row in df.iterrows():  # Iterate over each row in the DataFrame
    if row["device_type"] == "cisco_ios_telnet":
        device = CiscoDevice(hostname=row["hostname"], username=row["username"], password=row["password"])
    elif row["device_type"] == "juniper_junos_telnet":
        device = JuniperDevice(hostname=row["hostname"], username=row["username"], password=row["password"])
    else:
        print(f"Skipping unknown device type: {row['device_type']}")
        continue
    devices.append(device)

# Step 6: Back Up All Devices in Parallel Using Multithreading

start_time = time.time()  # Start timer

success_count = 0
failure_count = 0

# Create a ThreadPoolExecutor with 5 threads
with ThreadPoolExecutor(max_workers=5) as executor:
    # Submit backup tasks for each device and collect futures
    futures = [executor.submit(device.backup_config) for device in devices]

    # Process results as they complete
    for future in as_completed(futures):
        try:
            result = future.result()  # Get the result of the backup
            if "backup saved to" in result:
                success_count += 1
            else:
                failure_count += 1
        except Exception as e:
            result = f"Backup failed: {e}"
            failure_count += 1
        print(result)

# End timer
end_time = time.time()

# Print summary
print(f"\n✅ Successful backups: {success_count}")
print(f"❌ Failed backups: {failure_count}")
print(f"⏱️ Total execution time: {end_time - start_time:.2f} seconds")
