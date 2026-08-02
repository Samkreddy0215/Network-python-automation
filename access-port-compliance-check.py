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

EXPECTED_ACCESS_VLAN = "10"
EXPECTED_VOICE_VLAN = "20"

with open("access_port_compliance_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Mode",
        "Access VLAN",
        "Voice VLAN",
        "Compliance"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            conn = ConnectHandler(**device)

            output = conn.send_command("show interfaces switchport")

            conn.disconnect()

            interface = ""
            mode = ""
            access_vlan = ""
            voice_vlan = ""

            for line in output.splitlines():

                line = line.strip()

                if line.startswith("Name:"):
                    interface = line.replace("Name:", "").strip()

                elif line.startswith("Administrative Mode:"):
                    mode = line.replace("Administrative Mode:", "").strip()

                elif line.startswith("Access Mode VLAN:"):
                    match = re.search(r'(\d+)', line)
                    access_vlan = match.group(1) if match else ""

                elif line.startswith("Voice VLAN:"):
                    match = re.search(r'(\d+)', line)
                    voice_vlan = match.group(1) if match else ""

                    compliance = "PASS"

                    if "static access" in mode.lower():

                        if access_vlan != EXPECTED_ACCESS_VLAN:
                            compliance = "FAIL"

                        if voice_vlan not in ("", EXPECTED_VOICE_VLAN):
                            compliance = "FAIL"

                        writer.writerow([
                            device["host"],
                            interface,
                            mode,
                            access_vlan,
                            voice_vlan,
                            compliance
                        ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print("Access Port Compliance Check Completed")
print("----------------------------------------")
print("Report Saved : access_port_compliance_report.csv")
