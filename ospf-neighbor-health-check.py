from netmiko import ConnectHandler
import csv

# Device Inventory
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

with open("ospf_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Neighbor ID",
        "Neighbor IP",
        "State",
        "Interface",
        "Dead Timer"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show ip ospf neighbor"
            )

            lines = output.splitlines()

            for line in lines:

                if "." in line:

                    columns = line.split()

                    if len(columns) >= 6:

                        neighbor_id = columns[0]
                        dead_time = columns[2]
                        neighbor_ip = columns[4]
                        interface = columns[5]
                        state = columns[3].split("/")[0]

                        if state == "FULL":
                            healthy += 1
                        else:
                            failed += 1

                        writer.writerow([
                            device["host"],
                            neighbor_id,
                            neighbor_ip,
                            state,
                            interface,
                            dead_time
                        ])

            connection.disconnect()

        except Exception:

            print(f"Unable to connect to {device['host']}")

print("-----------------------------------")
print(f"Healthy Neighbors : {healthy}")
print(f"Failed Neighbors  : {failed}")
print("-----------------------------------")
print("Report Saved : ospf_health_report.csv")
