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

with open("dhcp_snooping_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "DHCP Snooping",
        "Configured VLANs",
        "Trusted Interfaces",
        "Compliance"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            conn = ConnectHandler(**device)

            snooping = conn.send_command("show ip dhcp snooping")
            trusted = conn.send_command("show ip dhcp snooping statistics")

            conn.disconnect()

            enabled = "Enabled" if "DHCP snooping is enabled" in snooping else "Disabled"

            vlan_line = "None"
            for line in snooping.splitlines():
                if "Configured VLANs" in line:
                    vlan_line = line.split(":")[-1].strip()
                    break

            trusted_count = trusted.count("Trusted")

            compliance = "PASS"

            if enabled != "Enabled":
                compliance = "FAIL"

            writer.writerow([
                device["host"],
                enabled,
                vlan_line,
                trusted_count,
                compliance
            ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print("DHCP Snooping Validation Completed")
print("----------------------------------------")
print("Report Saved : dhcp_snooping_report.csv")
