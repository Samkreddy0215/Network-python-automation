from netmiko import ConnectHandler
from datetime import datetime
import os

# Device Inventory
devices = [
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.1",
        "username": "admin",
        "password": "password"
    },
    {
        "device_type": "cisco_ios",
        "host": "10.1.1.2",
        "username": "admin",
        "password": "password"
    }
]

backup_folder = "backups"

if not os.path.exists(backup_folder):
    os.makedirs(backup_folder)

successful = 0
failed = 0

for device in devices:

    print(f"Connecting to {device['host']}...")

    try:

        connection = ConnectHandler(**device)

        hostname = connection.find_prompt().replace("#", "")

        running_config = connection.send_command(
            "show running-config"
        )

        connection.disconnect()

        filename = f"{backup_folder}/{hostname}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        with open(filename, "w") as backup_file:
            backup_file.write(running_config)

        successful += 1

        print(f"Backup saved: {filename}")

    except Exception as error:

        failed += 1
        print(f"Backup failed for {device['host']}: {error}")

print("----------------------------------------")
print(f"Successful Backups : {successful}")
print(f"Failed Backups     : {failed}")
print("----------------------------------------")
print("Configuration backup completed.")
