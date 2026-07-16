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

total_groups = 0
healthy_groups = 0
issue_groups = 0

with open("vrrp_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Group",
        "State",
        "Virtual IP",
        "Priority"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command("show vrrp brief")

            connection.disconnect()

            lines = output.splitlines()

            for line in lines:

                columns = line.split()

                if len(columns) >= 5 and columns[0].startswith("Vlan"):

                    total_groups += 1

                    interface = columns[0]
                    group = columns[1]
                    state = columns[2]
                    virtual_ip = columns[3]
                    priority = columns[4]

                    if state in ["Master", "Backup"]:
                        healthy_groups += 1
                    else:
                        issue_groups += 1

                    writer.writerow([
                        device["host"],
                        interface,
                        group,
                        state,
                        virtual_ip,
                        priority
                    ])

        except Exception as error:
            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Total VRRP Groups : {total_groups}")
print(f"Healthy Groups    : {healthy_groups}")
print(f"Issues Found      : {issue_groups}")
print("----------------------------------------")
print("Report Saved : vrrp_health_report.csv")
