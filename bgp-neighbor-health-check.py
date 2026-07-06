from netmiko import ConnectHandler
import csv

# Cisco Devices
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.2",
        "username": "admin",
        "password": "password"
    }
]

healthy = 0
failed = 0

with open("bgp_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Neighbor",
        "Remote AS",
        "State",
        "Prefixes",
        "Uptime"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ip bgp summary"
            )

            lines = output.splitlines()

            for line in lines:

                if "." in line:

                    columns = line.split()

                    if len(columns) >= 10:

                        neighbor = columns[0]
                        remote_as = columns[2]
                        uptime = columns[8]
                        state = columns[9]

                        if state.isdigit():
                            prefixes = state
                            state = "Established"
                            healthy += 1
                        else:
                            prefixes = "0"
                            failed += 1

                        writer.writerow([
                            device["host"],
                            neighbor,
                            remote_as,
                            state,
                            prefixes,
                            uptime
                        ])

            connection.disconnect()

        except Exception as error:

            print(f"Unable to connect to {device['host']}")

print("----------------------------------")
print(f"Healthy Neighbors : {healthy}")
print(f"Failed Neighbors  : {failed}")
print("----------------------------------")
print("Report Saved : bgp_health_report.csv")
