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

total_devices = 0
healthy = 0
issues = 0

with open("dhcp_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "DHCP Server",
        "Leases",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ip dhcp binding"
            )

            connection.disconnect()

            total_devices += 1

            lease_count = 0

            for line in output.splitlines():

                if "." in line:
                    lease_count += 1

            if lease_count > 0:
                status = "Healthy"
                healthy += 1
            else:
                status = "No Active Leases"
                issues += 1

            writer.writerow([
                device["host"],
                device["host"],
                lease_count,
                status
            ])

        except Exception as error:

            print(f"Connection Failed: {error}")
            issues += 1

print("----------------------------------------")
print(f"Total Devices Checked : {total_devices}")
print(f"Healthy Devices       : {healthy}")
print(f"Issues Found          : {issues}")
print("----------------------------------------")
print("Report Saved : dhcp_health_report.csv")
