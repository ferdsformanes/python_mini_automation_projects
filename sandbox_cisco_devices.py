# Automate SSH connections to Cisco devices (using Netmiko)

from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

devices = [
    {
        "device_type": "cisco_xr",
        "host": "sandbox-iosxr-1.cisco.com",
        "username": "admin",
        "password": "C1sco12345",
    },
    {
        "device_type": "cisco_nxos",
        "host": "sbx-nxos-mgmt.cisco.com",
        "username": "admin",
        "password": "Admin_1234!",
    },
]

for device in devices:
    try:
        print(f"\n== Connecting to {device['host']} ==")
        conn = ConnectHandler(**device)
        output = conn.send_command("show ip int brief")
        print(output)
        conn.disconnect()
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Connection failed for {device['host']}: {e}")
    except Exception as e:
        print(f"Error connecting to {device['host']}: {e}")

# Note: These sandbox devices are publicly available for testing and learning purposes.
# https://devnetsandbox.cisco.com/DevNet/catalog/Open-NX-OS-Programmability_open-nx-os
# https://devnetsandbox.cisco.com/DevNet/catalog/ios-xr-always-on_ios-xr-always-on
