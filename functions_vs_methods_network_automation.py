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

# # This is a USER-DEFINED FUNCTION
# def connect_and_run_function(hostname, username, password, command, device_type="cisco_ios_telnet"):
#     device = {
#         "device_type": device_type,
#         "host": hostname,
#         "username": username,
#         "password": password,
#     }
#     with ConnectHandler(**device) as conn:
#         output = conn.send_command(command)
#     return output


# # Example: Built-in Function
# device_ips = ["10.0.0.5", "192.168.1.10", "172.16.0.1"]

# # len() → Built-in Function provided by Python
# print("Total devices to connect:", len(device_ips))


# -----------------------------------------------
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

    # USER-DEFINED METHOD
    def connect_and_run(self, command):
        device = {
            "device_type": self.device_type,
            "host": self.hostname,
            "username": self.username,
            "password": self.password,
        }
        with ConnectHandler(**device) as conn:
            output = conn.send_command(command)
        return output


# # Example: Built-in Method
# sample_output = "Gig0/0    10.0.0.1    YES manual up up"

# # split() → Built-in Method of Python’s str class
# fields = sample_output.split()
# print("Interface:", fields[0])
# print("IP Address:", fields[1])
# print("Status:", fields[-2], fields[-1])


# ---------------------------------------------------------------
# 3. Using Functions vs Methods
# -----------------------------

# # Calling a user-defined function
# print(connect_and_run_function("route-views.routeviews.org", "rviews", "rviews", "show version"))

# Creating an object and calling a user-defined method
device1 = NetworkDevice("route-views.routeviews.org", "rviews", "rviews")
print(device1.connect_and_run("show version"))

# ---------------------------------------------------------------
# Summary:          
# - Functions are standalone and not tied to any object.
# - Methods are tied to objects and can access object data.
