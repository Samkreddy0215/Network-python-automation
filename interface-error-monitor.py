from netmiko import ConnectHandler
import csv

devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

healthy = 0
warning = 0
total_interfaces = 0

with open("interface_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Status",
        "Protocol",
        "Health"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ip interface brief"
            )

            lines = output.splitlines()[1:]

            for line in lines:

                columns = line.split()

                if len(columns) >= 6:

                    total_interfaces += 1

                    interface = columns[0]
                    status = columns[4]
                    protocol = columns[5]

                    if status == "up" and protocol == "up":
                        health = "Healthy"
                        healthy += 1
                    else:
                        health = "Warning"
                        warning += 1

                    writer.writerow([
                        device["host"],
                        interface,
                        status,
                        protocol,
                        health
                    ])

            connection.disconnect()

        except Exception as error:

            print(f"Connection failed: {error}")

print("--------------------------------")
print(f"Total Interfaces : {total_interfaces}")
print(f"Healthy          : {healthy}")
print(f"Warning          : {warning}")
print("--------------------------------")
print("Report Saved : interface_health_report.csv")
