# ---------------------------------------------------------
# Automate Traceroute with Python + Excel
# ---------------------------------------------------------
import subprocess
import pandas as pd
from datetime import datetime
import platform


devices_df = pd.read_excel("devices.xlsx")
devices = devices_df["IP"].tolist()

def traceroute_device(ip):
    try:
        # Choose command based on OS
        cmd = "tracert" if platform.system().lower() == "windows" else "traceroute"
        
        result = subprocess.run(
            [cmd, ip],
            capture_output=True,
            text=True,
            timeout=60   
        )

        output = result.stdout.strip() if result.stdout else result.stderr.strip()

        if result.returncode == 0:
            return "Success", output
        else:
            return "Completed with errors", output

    except subprocess.TimeoutExpired as e:
        partial_output = e.stdout.strip() if e.stdout else ""
        return "Timed out", partial_output

    except Exception as e:
        return f"Error: {e}", ""


results = []

for device in devices:
    status, output = traceroute_device(device)
    print(f"{device}: {status}")
    results.append({
        "IP": device,
        "Status": status,
        "Output": output
    })

results_df = pd.DataFrame(results)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"traceroute_results_{timestamp}.xlsx"
results_df.to_excel(output_file, index=False)

print(f"\n✅ Results saved to {output_file}")
