from netmiko import ConnectHandler
import csv
import re

devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

EXPECTED_ROOT = "0011.2233.4455"

with open("stp_root_bridge_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "VLAN",
        "Root Bridge",
        "Expected Root",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            conn = ConnectHandler(**device)

            output = conn.send_command("show spanning-tree root")

            conn.disconnect()

            vlan = ""

            for line in output.splitlines():

                if line.startswith("VLAN"):
                    vlan = line.split()[0].replace("VLAN", "")

                mac = re.search(r"([0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4})", line)

                if mac and vlan:

                    root_bridge = mac.group(1)

                    status = "PASS"

                    if root_bridge.lower() != EXPECTED_ROOT.lower():
                        status = "FAIL"

                    writer.writerow([
                        device["host"],
                        vlan,
                        root_bridge,
                        EXPECTED_ROOT,
                        status
                    ])

print("----------------------------------------")
print("STP Root Bridge Validation Completed")
print("----------------------------------------")
print("Report Saved : stp_root_bridge_report.csv")
