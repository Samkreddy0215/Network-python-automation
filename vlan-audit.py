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

with open("vlan_audit_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "VLAN ID",
        "VLAN Name",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command("show vlan brief")

            lines = output.splitlines()

            for line in lines:

                columns = line.split()

                if len(columns) >= 3 and columns[0].isdigit():

                    writer.writerow([
                        device["host"],
                        columns[0],
                        columns[1],
                        columns[2]
                    ])

            connection.disconnect()

        except Exception as error:

            print(f"Connection Failed: {error}")

print("--------------------------------")
print("VLAN Audit Completed")
print("Report Saved : vlan_audit_report.csv")
print("--------------------------------")
