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

expected_vlans = {
    "10": "Users",
    "20": "Voice",
    "30": "Servers",
    "99": "Management"
}

with open("vlan_consistency_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)
    writer.writerow([
        "Device",
        "VLAN ID",
        "Expected Name",
        "Actual Name",
        "Status"
    ])

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            conn = ConnectHandler(**device)

            output = conn.send_command("show vlan brief")

            conn.disconnect()

            actual_vlans = {}

            for line in output.splitlines():

                cols = line.split()

                if len(cols) >= 2 and cols[0].isdigit():
                    actual_vlans[cols[0]] = cols[1]

            for vlan_id, expected_name in expected_vlans.items():

                actual_name = actual_vlans.get(vlan_id, "Not Found")

                status = (
                    "PASS"
                    if actual_name == expected_name
                    else "FAIL"
                )

                writer.writerow([
                    device["host"],
                    vlan_id,
                    expected_name,
                    actual_name,
                    status
                ])

        except Exception as error:
            print(f"Connection failed: {error}")

print("----------------------------------------")
print("VLAN Consistency Check Completed")
print("----------------------------------------")
print("Report Saved : vlan_consistency_report.csv")
