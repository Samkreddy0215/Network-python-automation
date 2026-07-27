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

with open("environment_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "Temperature Status",
        "Power Supply Status",
        "Fan Status",
        "Overall Health"
    ])

    healthy_devices = 0
    warning_devices = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            env_output = connection.send_command(
                "show environment all"
            )

            connection.disconnect()

            temp_status = "Normal"
            power_status = "Normal"
            fan_status = "Normal"

            output_upper = env_output.upper()

            if "OVERHEAT" in output_upper or "CRITICAL" in output_upper:
                temp_status = "Warning"

            if "POWER" in output_upper and "FAILED" in output_upper:
                power_status = "Warning"

            if "FAN" in output_upper and "FAILED" in output_upper:
                fan_status = "Warning"

            overall = "Healthy"

            if (
                temp_status == "Warning"
                or power_status == "Warning"
                or fan_status == "Warning"
            ):
                overall = "Warning"
                warning_devices += 1
            else:
                healthy_devices += 1

            writer.writerow([
                device["host"],
                temp_status,
                power_status,
                fan_status,
                overall
            ])

        except Exception as error:
            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Healthy Devices : {healthy_devices}")
print(f"Warning Devices : {warning_devices}")
print("----------------------------------------")
print("Report Saved : environment_health_report.csv")
