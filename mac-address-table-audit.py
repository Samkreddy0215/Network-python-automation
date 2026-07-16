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

total_mac = 0
dynamic_mac = 0
static_mac = 0

with open("mac_address_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "VLAN",
        "MAC Address",
        "Type",
        "Interface"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            output = connection.send_command(
                "show mac address-table"
            )

            lines = output.splitlines()

            for line in lines:

                columns = line.split()

                if len(columns) >= 5 and columns[0].isdigit():

                    total_mac += 1

                    vlan = columns[0]
                    mac = columns[1]
                    mac_type = columns[2]
                    interface = columns[-1]

                    if mac_type.upper() == "DYNAMIC":
                        dynamic_mac += 1
                    else:
                        static_mac += 1

                    writer.writerow([
                        device["host"],
                        vlan,
                        mac,
                        mac_type,
                        interface
                    ])

            connection.disconnect()

        except Exception as error:

            print(f"Connection failed: {error}")

print("---------------------------------------")
print(f"Total MAC Addresses : {total_mac}")
print(f"Dynamic Entries     : {dynamic_mac}")
print(f"Static Entries      : {static_mac}")
print("---------------------------------------")
print("Report Saved : mac_address_report.csv")
