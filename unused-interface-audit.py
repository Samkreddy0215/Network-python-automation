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

with open("unused_interface_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow([
        "Device",
        "Interface",
        "Admin Status",
        "Protocol Status",
        "Recommendation"
    ])

    total = 0
    unused = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            conn = ConnectHandler(**device)

            output = conn.send_command("show ip interface brief")

            conn.disconnect()

            for line in output.splitlines()[1:]:

                cols = line.split()

                if len(cols) >= 6:

                    interface = cols[0]
                    admin_status = cols[4]
                    protocol_status = cols[5]

                    recommendation = "In Use"

                    if admin_status == "administratively" and protocol_status == "down":
                        recommendation = "Review or Decommission"
                        unused += 1

                    total += 1

                    writer.writerow([
                        device["host"],
                        interface,
                        admin_status,
                        protocol_status,
                        recommendation
                    ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print(f"Interfaces Checked : {total}")
print(f"Unused Interfaces  : {unused}")
print("----------------------------------------")
print("Report Saved : unused_interface_report.csv")
