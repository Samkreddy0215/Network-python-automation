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

with open("bgp_route_validation_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Network",
        "Next Hop",
        "Metric",
        "Local Preference",
        "AS Path"
    ])

    total_routes = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ip bgp"
            )

            connection.disconnect()

            for line in output.splitlines():

                line = line.strip()

                if line.startswith("*") or line.startswith(">") or line.startswith("*>"):

                    columns = line.split()

                    if len(columns) >= 6:

                        total_routes += 1

                        writer.writerow([
                            device["host"],
                            columns[1],
                            columns[2],
                            columns[3],
                            columns[4],
                            " ".join(columns[5:])
                        ])

        except Exception as error:

            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Total BGP Routes : {total_routes}")
print("----------------------------------------")
print("Report Saved : bgp_route_validation_report.csv")
