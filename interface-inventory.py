from netmiko import ConnectHandler
import csv

# Device Inventory
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

with open("interface_inventory_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "IP Address",
        "Status",
        "Protocol"
    ])

    total_interfaces = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ip interface brief"
            )

            connection.disconnect()

            lines = output.splitlines()[1:]

            for line in lines:

                columns = line.split()

                if len(columns) >= 6:

                    total_interfaces += 1

                    writer.writerow([
                        device["host"],
                        columns[0],
                        columns[1],
                        columns[4],
                        columns[5]
                    ])

        except Exception as error:

            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Total Interfaces : {total_interfaces}")
print("----------------------------------------")
print("Report Saved : interface_inventory_report.csv")
