# Simple Interface Status Checker

interfaces = {
    "GigabitEthernet0/0": "up",
    "GigabitEthernet0/1": "down",
    "GigabitEthernet0/2": "up"
}

print("Interface Status Report")
print("-" * 30)

for interface, status in interfaces.items():
    print(f"{interface}: {status}")
