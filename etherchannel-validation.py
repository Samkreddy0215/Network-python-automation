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

with open("etherchannel_validation_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Port-Channel",
        "Protocol",
        "Member Ports",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:
            conn = ConnectHandler(**device)

            output = conn.send_command("show etherchannel summary")

            conn.disconnect()

            for line in output.splitlines():

                if "Po" in line and "(" in line:

                    columns = line.split()

                    port_channel = columns[0]
                    protocol = columns[-2]
                    members = columns[-1]

                    status = "PASS"

                    if "(D)" in line or "(I)" in line:
                        status = "FAIL"

                    writer.writerow([
                        device["host"],
                        port_channel,
                        protocol,
                        members,
                        status
                    ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print("EtherChannel Validation Completed")
print("----------------------------------------")
print("Report Saved : etherchannel_validation_report.csv")
