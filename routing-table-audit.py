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

with open("routing_table_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Connected Routes",
        "Static Routes",
        "OSPF Routes",
        "BGP Routes",
        "EIGRP Routes",
        "Total Routes"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command("show ip route")

            connection.disconnect()

            connected = 0
            static = 0
            ospf = 0
            bgp = 0
            eigrp = 0

            for line in output.splitlines():

                line = line.strip()

                if line.startswith("C "):
                    connected += 1
                elif line.startswith("S "):
                    static += 1
                elif line.startswith("O "):
                    ospf += 1
                elif line.startswith("B "):
                    bgp += 1
                elif line.startswith("D "):
                    eigrp += 1

            total = connected + static + ospf + bgp + eigrp

            writer.writerow([
                device["host"],
                connected,
                static,
                ospf,
                bgp,
                eigrp,
                total
            ])

        except Exception as error:

            print(f"Connection Failed: {error}")

print("----------------------------------------")
print("Routing Table Audit Completed")
print("----------------------------------------")
print("Report Saved : routing_table_report.csv")
