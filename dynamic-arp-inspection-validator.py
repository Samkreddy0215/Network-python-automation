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

with open("dynamic_arp_inspection_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "DAI Status",
        "Protected VLANs",
        "Trusted Interfaces",
        "Compliance"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            conn = ConnectHandler(**device)

            dai = conn.send_command("show ip arp inspection")
            interfaces = conn.send_command("show ip arp inspection interfaces")

            conn.disconnect()

            status = "Enabled" if "Source Mac Validation" in dai else "Disabled"

            vlans = "None"
            for line in dai.splitlines():
                if "Vlan Configuration" in line:
                    vlans = line.split(":")[-1].strip()

            trusted = interfaces.count("Trusted")

            compliance = "PASS" if status == "Enabled" else "FAIL"

            writer.writerow([
                device["host"],
                status,
                vlans,
                trusted,
                compliance
            ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print("Dynamic ARP Inspection Validation Completed")
print("----------------------------------------")
print("Report Saved : dynamic_arp_inspection_report.csv")
