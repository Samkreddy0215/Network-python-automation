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
        "device_type": "cisco_nxos",
        "host": "10.1.1.2",
        "username": "admin",
        "password": "password"
    }
]

total_entries = 0
dynamic_entries = 0
static_entries = 0

with open("arp_table_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "IP Address",
        "MAC Address",
        "Interface",
        "Type"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command("show ip arp")

            lines = output.splitlines()

            for line in lines:

                columns = line.split()

                if len(columns) >= 6 and "." in columns[1]:

                    total_entries += 1

                    ip = columns[1]
                    mac = columns[3]
                    interface = columns[-1]

                    arp_type = "Dynamic"

                    if "ARPA" not in line.upper():
                        arp_type = "Static"

                    if arp_type == "Dynamic":
                        dynamic_entries += 1
                    else:
                        static_entries += 1

                    writer.writerow([
                        device["host"],
                        ip,
                        mac,
                        interface,
                        arp_type
                    ])

            connection.disconnect()

        except Exception as error:

            print(f"Connection Failed: {error}")

print("------------------------------------")
print(f"Total ARP Entries : {total_entries}")
print(f"Dynamic Entries   : {dynamic_entries}")
print(f"Static Entries    : {static_entries}")
print("------------------------------------")
print("Report Saved : arp_table_report.csv")
