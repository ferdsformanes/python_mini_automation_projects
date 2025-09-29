# Python Subprocess + Pandas Tutorial | Automate Ping with Excel  
import subprocess
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# READ DEVICES FROM EXCEL
# ---------------------------------------------------------
# Your Excel file must have a column "IP"
devices_df = pd.read_excel("devices.xlsx")
devices = devices_df["IP"].tolist()


# ---------------------------------------------------------
# PING FUNCTION
# ---------------------------------------------------------
def ping_device(ip):
    """Ping a single device and return result + full output."""
    try:
        # Windows uses 'ping -n', Linux/Mac uses 'ping -c'
        result = subprocess.run(
            ["ping", "-n", "4", ip],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return "Reachable", result.stdout.strip()
        else:
            return "Unreachable", result.stderr.strip()

    except subprocess.TimeoutExpired:
        return "Timed out", ""
    except Exception as e:
        return f"Error: {e}", ""


# ---------------------------------------------------------
# RUN PINGS AND COLLECT RESULTS
# ---------------------------------------------------------
results = []

for device in devices:
    status, output = ping_device(device)
    print(f"{device}: {status}")
    results.append({
        "IP": device,
        "Status": status,
        "Output": output
    })

# Convert results to DataFrame
results_df = pd.DataFrame(results)

# ---------------------------------------------------------
# SAVE RESULTS TO EXCEL WITH TIMESTAMP
# ---------------------------------------------------------
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"ping_results_{timestamp}.xlsx"
results_df.to_excel(output_file, index=False)

print(f"\n✅ Results saved to {output_file}")
