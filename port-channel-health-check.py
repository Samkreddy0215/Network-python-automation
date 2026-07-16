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

total_portchannels = 0
healthy = 0
issues = 0

with open("portchannel_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Port-Channel",
        "Protocol",
        "Status",
        "Member Interfaces"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show etherchannel summary"
            )

            connection.disconnect()

            lines = output.splitlines()

            for line in lines:

                if line.startswith("1") or line.startswith("2") or line.startswith("3"):

                    columns = line.split()

                    total_portchannels += 1

                    group = columns[0]
                    portchannel = columns[1]
                    protocol = columns[-1]

                    status = "Healthy"

                    if "(SU)" in line:
                        healthy += 1
                    else:
                        status = "Issue"
                        issues += 1

                    members = " ".join(columns[2:-1])

                    writer.writerow([
                        device["host"],
                        portchannel,
                        protocol,
                        status,
                        members
                    ])

        except Exception as error:

            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Total Port-Channels : {total_portchannels}")
print(f"Healthy             : {healthy}")
print(f"Issues Found        : {issues}")
print("----------------------------------------")
print("Report Saved : portchannel_health_report.csv")
