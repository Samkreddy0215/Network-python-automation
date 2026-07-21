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

dns_server = "8.8.8.8"

healthy = 0
issues = 0

with open("dns_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "DNS Server",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                f"ping {dns_server}"
            )

            connection.disconnect()

            if "Success rate is 100 percent" in output:
                status = "Reachable"
                healthy += 1
            else:
                status = "Unreachable"
                issues += 1

            writer.writerow([
                device["host"],
                dns_server,
                status
            ])

        except Exception as error:

            print(f"Connection Failed: {error}")
            issues += 1

print("----------------------------------------")
print(f"Healthy Devices : {healthy}")
print(f"Issues Found    : {issues}")
print("----------------------------------------")
print("Report Saved : dns_health_report.csv")
