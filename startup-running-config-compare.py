from netmiko import ConnectHandler
import difflib

devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    }
]

for device in devices:

    print(f"Connecting to {device['host']}...")

    try:
        connection = ConnectHandler(**device)

        running = connection.send_command("show running-config")
        startup = connection.send_command("show startup-config")

        hostname = connection.find_prompt().replace("#", "")

        connection.disconnect()

        diff = difflib.unified_diff(
            startup.splitlines(),
            running.splitlines(),
            fromfile="startup-config",
            tofile="running-config",
            lineterm=""
        )

        report_name = f"{hostname}_config_diff.txt"

        with open(report_name, "w") as report:
            report.write("\n".join(diff))

        print(f"Configuration comparison saved to {report_name}")

    except Exception as error:
        print(f"Connection failed: {error}")

print("----------------------------------------")
print("Startup vs Running Configuration Comparison Completed")
print("----------------------------------------")
