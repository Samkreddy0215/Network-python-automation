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

with open("interface_utilization_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Input Rate (bps)",
        "Output Rate (bps)",
        "Status"
    ])

    high_utilization = 0
    total_interfaces = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:
            connection = ConnectHandler(**device)

            interfaces = connection.send_command(
                "show interfaces summary"
            )

            for line in interfaces.splitlines():

                columns = line.split()

                if len(columns) < 2:
                    continue

                interface = columns[0]

                if interface.startswith(("Gi", "Te", "Eth")):

                    details = connection.send_command(
                        f"show interfaces {interface}"
                    )

                    input_rate = "Unknown"
                    output_rate = "Unknown"

                    for detail in details.splitlines():

                        if "input rate" in detail:
                            input_rate = detail.split(",")[0].split()[-2]

                        if "output rate" in detail:
                            output_rate = detail.split(",")[0].split()[-2]

                    total_interfaces += 1

                    status = "Normal"

                    try:
                        if input_rate != "Unknown" and int(input_rate) > 100000000:
                            status = "High Utilization"

                        if output_rate != "Unknown" and int(output_rate) > 100000000:
                            status = "High Utilization"

                    except ValueError:
                        pass

                    if status == "High Utilization":
                        high_utilization += 1

                    writer.writerow([
                        device["host"],
                        interface,
                        input_rate,
                        output_rate,
                        status
                    ])

            connection.disconnect()

        except Exception as error:
            print(f"Connection Failed: {error}")

print("-------------------------------------------")
print(f"Total Interfaces      : {total_interfaces}")
print(f"High Utilization      : {high_utilization}")
print("-------------------------------------------")
print("Report Saved : interface_utilization_report.csv")
