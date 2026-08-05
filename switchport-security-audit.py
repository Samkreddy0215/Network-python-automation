from netmiko import ConnectHandler
import csv
import re

devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

with open("switchport_security_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Port Security",
        "Maximum MAC",
        "Violation Mode",
        "Compliance"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:
            conn = ConnectHandler(**device)

            output = conn.send_command("show port-security interface")

            conn.disconnect()

            interface = ""

            for line in output.splitlines():

                line = line.strip()

                if line.startswith("Port"):
                    match = re.search(r'Port\s*:\s*(\S+)', line)
                    if match:
                        interface = match.group(1)

                elif line.startswith("Port Security"):
                    enabled = line.split(":")[-1].strip()

                elif line.startswith("Maximum MAC Addresses"):
                    max_mac = line.split(":")[-1].strip()

                elif line.startswith("Violation Mode"):
                    violation = line.split(":")[-1].strip()

                    compliance = "PASS"

                    if enabled.lower() != "enabled":
                        compliance = "FAIL"

                    writer.writerow([
                        device["host"],
                        interface,
                        enabled,
                        max_mac,
                        violation,
                        compliance
                    ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print("Switchport Security Audit Completed")
print("----------------------------------------")
print("Report Saved : switchport_security_report.csv")
