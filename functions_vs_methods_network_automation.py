# ---------------------------------------------------------------
# Functions vs Methods in Python (Network Automation Example)
# ---------------------------------------------------------------

# 1. What is a Function?
# ----------------------
# - A function is defined using "def".
# - It is independent and not tied to any object.
# - You pass data to it and get back a result.
# - Functions are useful for reusable tasks.

from netmiko import ConnectHandler

def connect_and_run_function(hostname, username, password, command, device_type="cisco_ios_telnet"):
    device = {
        "device_type": device_type,
        "host": hostname,
        "username": username,
        "password": password,
    }
    with ConnectHandler(**device) as conn:
        output = conn.send_command(command)
    return output

# -------------------------------------------------------------------------------
# 2. What is a Method?
# --------------------
# - A method is similar to a function, but it is defined inside a class.
# - It is tied to an object (an instance of a class).
# - Methods can access and modify the object’s data (via 'self').

class NetworkDevice:
    def __init__(self, hostname, username, password, device_type="cisco_ios_telnet"):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.device_type = device_type

    def connect_and_run(self, command):
        from netmiko import ConnectHandler
        device = {
            "device_type": self.device_type,
            "host": self.hostname,
            "username": self.username,
            "password": self.password,
        }
        with ConnectHandler(**device) as conn:
            output = conn.send_command(command)
        return output

# ---------------------------------------------------------------

# 3. Using Functions vs Methods
# -----------------------------

print(connect_and_run_function("route-views.routeviews.org", "rviews", "rviews", "show version"))

device1 = NetworkDevice("route-views.routeviews.org", "rviews", "rviews")
print(device1.connect_and_run("show version"))

# ---------------------------------------------------------------
# Summary
# -------
# - Functions are independent blocks of code.
# - Methods are functions that belong to a class and operate on objects.