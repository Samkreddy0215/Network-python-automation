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

with open("interface_description_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Description",
        "Status"
    ])

    total_interfaces = 0
    missing_descriptions = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:
            connection = ConnectHandler(**device)

            output = connection.send_command("show running-config")

            connection.disconnect()

            current_interface = None
            description = ""

            for line in output.splitlines():

                if line.startswith("interface "):

                    if current_interface is not None:

                        status = "Present"

                        if description == "":
                            status = "Missing"
                            missing_descriptions += 1

                        total_interfaces += 1

                        writer.writerow([
                            device["host"],
                            current_interface,
                            description if description else "N/A",
                            status
                        ])

                    current_interface = line.replace("interface ", "").strip()
                    description = ""

                elif line.strip().startswith("description "):

                    description = line.strip().replace("description ", "")

            if current_interface is not None:

                status = "Present"

                if description == "":
                    status = "Missing"
                    missing_descriptions += 1

                total_interfaces += 1

                writer.writerow([
                    device["host"],
                    current_interface,
                    description if description else "N/A",
                    status
                ])

        except Exception as error:
            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Total Interfaces        : {total_interfaces}")
print(f"Missing Descriptions    : {missing_descriptions}")
print("----------------------------------------")
print("Report Saved : interface_description_report.csv")
