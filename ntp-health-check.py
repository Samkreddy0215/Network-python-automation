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

total_devices = 0
healthy = 0
issues = 0

with open("ntp_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "NTP Server",
        "Reach",
        "Stratum",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ntp associations"
            )

            connection.disconnect()

            total_devices += 1

            server = "Unknown"
            reach = "Unknown"
            stratum = "Unknown"
            status = "Not Synchronized"

            for line in output.splitlines():

                if line.startswith("*"):

                    fields = line.split()

                    server = fields[0].replace("*", "")

                    if len(fields) >= 7:
                        stratum = fields[4]
                        reach = fields[6]

                    status = "Synchronized"
                    healthy += 1
                    break

            if status != "Synchronized":
                issues += 1

            writer.writerow([
                device["host"],
                server,
                reach,
                stratum,
                status
            ])

        except Exception as error:

            issues += 1
            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Total Devices Checked : {total_devices}")
print(f"Synchronized          : {healthy}")
print(f"NTP Issues            : {issues}")
print("----------------------------------------")
print("Report Saved : ntp_health_report.csv")
