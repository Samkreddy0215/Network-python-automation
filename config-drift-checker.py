from netmiko import ConnectHandler
from difflib import unified_diff
import os

# Device Inventory
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

# Create Reports Folder
os.makedirs("reports", exist_ok=True)

for device in devices:

    print(f"Connecting to {device['host']}...")

    try:

        connection = ConnectHandler(**device)

        running_config = connection.send_command(
            "show running-config"
        )

        connection.disconnect()

        # Read Baseline Configuration
        baseline_file = "baseline_config.txt"

        with open(baseline_file, "r") as file:
            baseline = file.readlines()

        running = running_config.splitlines(keepends=True)

        # Compare Configurations
        differences = list(
            unified_diff(
                baseline,
                running,
                fromfile="Baseline",
                tofile="Running"
            )
        )

        report_file = f"reports/{device['host']}_config_drift.txt"

        with open(report_file, "w") as report:

            if differences:

                report.write("Configuration Drift Detected\n\n")

                report.writelines(differences)

                print(f"Drift Found on {device['host']}")

            else:

                report.write("No Configuration Drift Found")

                print(f"No Drift Found on {device['host']}")

    except Exception as error:

        print(f"Unable to connect to {device['host']}")

print("Configuration Drift Check Completed.")
