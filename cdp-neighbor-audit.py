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

total_neighbors = 0

with open("cdp_neighbor_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Neighbor",
        "Management IP",
        "Platform",
        "Local Interface",
        "Remote Interface"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show cdp neighbors detail"
            )

            connection.disconnect()

            neighbors = output.split("-------------------------")

            for neighbor in neighbors:

                if "Device ID:" in neighbor:

                    total_neighbors += 1

                    device_name = re.search(r"Device ID:\s*(.*)", neighbor)
                    ip = re.search(r"IP address:\s*(.*)", neighbor)
                    platform = re.search(r"Platform:\s*(.*?),", neighbor)
                    local = re.search(r"Interface:\s*(.*?),", neighbor)
                    remote = re.search(r"Port ID \(outgoing port\):\s*(.*)", neighbor)

                    writer.writerow([
                        device["host"],
                        device_name.group(1) if device_name else "",
                        ip.group(1) if ip else "",
                        platform.group(1) if platform else "",
                        local.group(1) if local else "",
                        remote.group(1) if remote else ""
                    ])

        except Exception as error:

            print(f"Connection Failed: {error}")

print("------------------------------------")
print(f"Total Neighbors : {total_neighbors}")
print("------------------------------------")
print("Report Saved : cdp_neighbor_report.csv")
