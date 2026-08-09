from netmiko import ConnectHandler
import csv
import re

devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password",
    }
]

REPORT_FILE = "bpdu_guard_audit_report.csv"

with open(REPORT_FILE, "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Interface",
        "Switchport Mode",
        "PortFast",
        "BPDU Guard",
        "Status",
    ])

    for device in devices:

        print(f"\nConnecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            interfaces_output = connection.send_command(
                "show interfaces status"
            )

            config_output = connection.send_command(
                "show running-config"
            )

            connection.disconnect()

            interfaces = []

            for line in interfaces_output.splitlines():

                match = re.match(
                    r"^(Gi\S+|Fa\S+|Te\S+)\s+",
                    line.strip()
                )

                if match:
                    interfaces.append(match.group(1))

            for interface in interfaces:

                interface_pattern = (
                    rf"interface {re.escape(interface)}"
                    rf"(.*?)(?=\ninterface |\Z)"
                )

                match = re.search(
                    interface_pattern,
                    config_output,
                    re.DOTALL
                )

                if not match:
                    continue

                interface_config = match.group(1)

                access_port = (
                    "switchport mode access"
                    in interface_config
                )

                if not access_port:
                    continue

                portfast_enabled = (
                    "spanning-tree portfast"
                    in interface_config
                )

                bpdu_guard_enabled = (
                    "spanning-tree bpduguard enable"
                    in interface_config
                )

                status = "PASS"

                if not portfast_enabled:
                    status = "FAIL"

                if not bpdu_guard_enabled:
                    status = "FAIL"

                writer.writerow([
                    device["host"],
                    interface,
                    "Access",
                    (
                        "Enabled"
                        if portfast_enabled
                        else "Disabled"
                    ),
                    (
                        "Enabled"
                        if bpdu_guard_enabled
                        else "Disabled"
                    ),
                    status,
                ])

                print(
                    f"{interface}: "
                    f"PortFast="
                    f"{portfast_enabled}, "
                    f"BPDU Guard="
                    f"{bpdu_guard_enabled}, "
                    f"{status}"
                )

        except Exception as error:

            print(
                f"Connection failed for "
                f"{device['host']}: {error}"
            )

print("\n----------------------------------------")
print("BPDU Guard Audit Completed")
print("----------------------------------------")
print(f"Report Saved: {REPORT_FILE}")
