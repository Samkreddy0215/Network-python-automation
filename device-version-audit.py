from netmiko import ConnectHandler
import csv
import re

# Device Inventory
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

with open("device_version_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Hostname",
        "Model",
        "IOS Version",
        "Serial Number",
        "Uptime"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command("show version")

            connection.disconnect()

            hostname = "Unknown"
            model = "Unknown"
            version = "Unknown"
            serial = "Unknown"
            uptime = "Unknown"

            hostname_match = re.search(r"(\S+)\s+uptime is\s+(.*)", output)
            version_match = re.search(r"Cisco IOS.*Version\s+([^,]+)", output)
            model_match = re.search(r"cisco\s+(\S+).*processor", output, re.IGNORECASE)
            serial_match = re.search(r"Processor board ID\s+(\S+)", output)

            if hostname_match:
                hostname = hostname_match.group(1)
                uptime = hostname_match.group(2)

            if version_match:
                version = version_match.group(1)

            if model_match:
                model = model_match.group(1)

            if serial_match:
                serial = serial_match.group(1)

            writer.writerow([
                device["host"],
                hostname,
                model,
                version,
                serial,
                uptime
            ])

        except Exception as error:
            print(f"Connection Failed: {error}")

print("----------------------------------------")
print("Device Version Audit Completed")
print("----------------------------------------")
print("Report Saved : device_version_report.csv")
