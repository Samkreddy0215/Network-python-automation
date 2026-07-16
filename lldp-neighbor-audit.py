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
    },
    {
        "device_type": "cisco_nxos",
        "host": "10.1.1.2",
        "username": "admin",
        "password": "password"
    }
]

total_neighbors = 0

with open("lldp_neighbor_report.csv", "w", newline="") as csvfile:

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
                "show lldp neighbors detail"
            )

            connection.disconnect()

            neighbors = output.split("------------------------------------------------")

            for neighbor in neighbors:

                if "System Name:" in neighbor:

                    total_neighbors += 1

                    system_name = re.search(r"System Name:\s*(.*)", neighbor)
                    management_ip = re.search(r"Management Address:\s*(.*)", neighbor)
                    local_interface = re.search(r"Local Intf:\s*(.*)", neighbor)
                    port_id = re.search(r"Port id:\s*(.*)", neighbor)
                    system_desc = re.search(r"System Description:\s*(.*?)Time remaining", neighbor, re.S)

                    writer.writerow([
                        device["host"],
                        system_name.group(1).strip() if system_name else "",
                        management_ip.group(1).strip() if management_ip else "",
                        system_desc.group(1).split("\n")[0].strip() if system_desc else "",
                        local_interface.group(1).strip() if local_interface else "",
                        port_id.group(1).strip() if port_id else ""
                    ])

        except Exception as error:

            print(f"Connection Failed: {error}")

print("-------------------------------------")
print(f"Total Neighbors : {total_neighbors}")
print("-------------------------------------")
print("Report Saved : lldp_neighbor_report.csv")
