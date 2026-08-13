from netmiko import ConnectHandler
import json
import os
import sys
from datetime import datetime

DEVICE = {
    "device_type": "cisco_ios",
    "host": "10.1.1.1",
    "username": os.getenv("NETWORK_USERNAME"),
    "password": os.getenv("NETWORK_PASSWORD"),
}

PRE_FILE = "pre_change_snapshot.json"
POST_FILE = "post_change_snapshot.json"
REPORT_FILE = "change_validation_report.txt"


def validate_credentials():
    """Verify required credentials are available."""

    if not DEVICE["username"] or not DEVICE["password"]:
        raise RuntimeError(
            "Set NETWORK_USERNAME and NETWORK_PASSWORD "
            "environment variables before running."
        )


def collect_snapshot():
    """Collect operational state from the network device."""

    validate_credentials()

    print(f"Connecting to {DEVICE['host']}...")

    connection = ConnectHandler(**DEVICE)

    snapshot = {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "device": DEVICE["host"],
        "interfaces": connection.send_command(
            "show ip interface brief"
        ),
        "bgp": connection.send_command(
            "show ip bgp summary"
        ),
        "ospf": connection.send_command(
            "show ip ospf neighbor"
        ),
        "hsrp": connection.send_command(
            "show standby brief"
        ),
        "port_channels": connection.send_command(
            "show etherchannel summary"
        ),
        "routes": connection.send_command(
            "show ip route summary"
        ),
        "cpu": connection.send_command(
            "show processes cpu | include CPU"
        ),
        "memory": connection.send_command(
            "show processes memory | include Processor"
        ),
    }

    connection.disconnect()

    return snapshot


def save_snapshot(snapshot, filename):
    """Save collected operational state to JSON."""

    with open(
        filename,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            snapshot,
            file,
            indent=4,
        )

    print(f"Snapshot saved: {filename}")


def load_snapshot(filename):
    """Load a previously collected snapshot."""

    with open(
        filename,
        "r",
        encoding="utf-8",
    ) as file:

        return json.load(file)


def compare_snapshots(pre, post):
    """Compare pre-change and post-change states."""

    checks = [
        "interfaces",
        "bgp",
        "ospf",
        "hsrp",
        "port_channels",
        "routes",
        "cpu",
        "memory",
    ]

    results = []

    for check in checks:

        if pre.get(check) == post.get(check):

            status = "PASS"

        else:

            status = "CHANGED"

        results.append({
            "check": check,
            "status": status,
        })

    return results


def generate_report(pre, post, results):
    """Generate the final validation report."""

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8",
    ) as report:

        report.write(
            "ENTERPRISE NETWORK CHANGE VALIDATION REPORT\n"
        )

        report.write(
            "=" * 50 + "\n\n"
        )

        report.write(
            f"Device: {pre['device']}\n"
        )

        report.write(
            f"Pre-change snapshot: {pre['timestamp']}\n"
        )

        report.write(
            f"Post-change snapshot: {post['timestamp']}\n\n"
        )

        for result in results:

            report.write(
                f"{result['check'].upper():20} "
                f"{result['status']}\n"
            )

    print(f"Validation report saved: {REPORT_FILE}")


def run_pre_change():
    """Capture network state before maintenance."""

    print("\nCollecting PRE-CHANGE snapshot...")

    snapshot = collect_snapshot()

    save_snapshot(
        snapshot,
        PRE_FILE,
    )


def run_post_change():
    """Capture state after maintenance and compare."""

    if not os.path.exists(PRE_FILE):

        print(
            f"ERROR: {PRE_FILE} does not exist."
        )

        print(
            "Run the pre-change collection first."
        )

        return

    print("\nCollecting POST-CHANGE snapshot...")

    post_snapshot = collect_snapshot()

    save_snapshot(
        post_snapshot,
        POST_FILE,
    )

    pre_snapshot = load_snapshot(
        PRE_FILE
    )

    results = compare_snapshots(
        pre_snapshot,
        post_snapshot,
    )

    generate_report(
        pre_snapshot,
        post_snapshot,
        results,
    )

    print("\nValidation Summary")
    print("-" * 35)

    for result in results:

        print(
            f"{result['check']:20} "
            f"{result['status']}"
        )


def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python pre-post-change-validation.py pre"
        )

        print(
            "python pre-post-change-validation.py post"
        )

        return

    mode = sys.argv[1].lower()

    if mode == "pre":

        run_pre_change()

    elif mode == "post":

        run_post_change()

    else:

        print(
            "Invalid mode. Use 'pre' or 'post'."
        )


if __name__ == "__main__":
    main()
