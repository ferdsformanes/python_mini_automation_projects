# # --- import module_name ---
# import device_utils
# output1 = device_utils.connect_and_run_command(device_utils.cisco_device, "show version")
# print(output1)

# # --- from module_name import ... ---
# from device_utils import connect_and_run_command, cisco_device
# output2 = connect_and_run_command(cisco_device, "show ip interface brief")
# print(output2)

# # --- import module_name as alias ---
# import device_utils as du
# output3 = du.connect_and_run_command(du.cisco_device, "show inventory")
# print(output3)

# --- from module_name import * ---
from device_utils import *
output4 = connect_and_run_command(cisco_device, "show version")
print(output4)
