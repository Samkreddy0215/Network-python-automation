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

with open("cpu_memory_health_report.csv", "w", newline="") as csvfile:

    writer = csv.writer(csvfile)

    writer.writerow([
        "Device",
        "CPU (%)",
        "Memory Used (%)",
        "Health Status"
    ])

    healthy = 0
    warning = 0

    for device in devices:

        print(f"Connecting to {device['host']}...")

        try:

            connection = ConnectHandler(**device)

            cpu_output = connection.send_command(
                "show processes cpu | include CPU utilization"
            )

            mem_output = connection.send_command(
                "show processes memory | include Processor"
            )

            connection.disconnect()

            cpu = 0
            memory = 0

            cpu_match = re.search(r"five seconds: (\\d+)%", cpu_output)

            if cpu_match:
                cpu = int(cpu_match.group(1))

            mem_values = re.findall(r"(\\d+)", mem_output)

            if len(mem_values) >= 2:
                used = int(mem_values[0])
                free = int(mem_values[1])
                total = used + free
                if total > 0:
                    memory = round((used / total) * 100)

            status = "Healthy"

            if cpu > 80 or memory > 80:
                status = "Warning"
                warning += 1
            else:
                healthy += 1

            writer.writerow([
                device["host"],
                cpu,
                memory,
                status
            ])

        except Exception as error:
            print(f"Connection Failed: {error}")

print("----------------------------------------")
print(f"Healthy Devices : {healthy}")
print(f"Warnings        : {warning}")
print("----------------------------------------")
print("Report Saved : cpu_memory_health_report.csv")
