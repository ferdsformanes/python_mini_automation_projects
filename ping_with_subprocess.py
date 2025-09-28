import subprocess
from datetime import datetime

# ---------------------------------------------------------
# SUBPROCESS (BUILT-IN) LETS YOU:
# - Run system/CLI commands
# - Manage input/output/error streams
# - Control processes (wait, timeouts, return codes, etc.)
# ---------------------------------------------------------
#
# ---------------------------------------------------------
# WHY USE IT IN NETWORK AUTOMATION?
# - Run tools: ping, traceroute, nslookup
# - Automate checks & parse outputs
# ---------------------------------------------------------

# ---------------------------------------------------------
# EXAMPLE: PING MULTIPLE DEVICES
# Use a list of IPs and ping each one.
# ---------------------------------------------------------


devices = ["8.8.8.8", "1.1.1.1", "4.2.2.2", "192.168.1.1"]

def ping_device(ip):
    """Ping a single device and return result."""
    try:
        # Run ping command (Windows uses 'ping -n', Linux/Mac uses 'ping -c')
        result = subprocess.run(
            ["ping", "-n", "4", ip],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return f"--- {ip} is reachable ---{result.stdout}"
        else:
            return f"--- {ip} is unreachable ---{result.stderr}"

    except subprocess.TimeoutExpired:
        return f"--- {ip} timed out ---"
    except Exception as e:
        return f"--- Error with {ip}: {e} ---"
    
# ---------------------------------------------------------
# HANDLING OUTPUT
# Save results in a file with timestamp.
# ---------------------------------------------------------

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"ping_results_{timestamp}.txt"

with open(output_file, "w") as f:
    for device in devices:
        result = ping_device(device)
        print(result)           
        f.write(result + "\n")

