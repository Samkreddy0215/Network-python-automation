# Network Python Automation

Python scripts for automating enterprise networking tasks.

## Topics
- SSH Automation
- Configuration Backups
- Network Monitoring
- Device Health Checks
- Log Collection
- Interface Validation
- VLAN Automation

## Technologies
- Python
- Netmiko
- Paramiko
- REST APIs
- Cisco IOS
- Palo Alto APIs

## Goals
- Reduce manual operations
- Improve operational efficiency
- Learn network automation

## Project Structure

docs/          → Technical documentation
configs/       → Sample configurations
scripts/       → Automation scripts
templates/     → Configuration templates
images/        → Network diagrams
README.md      → Project overview
LICENSE        → License information

## BGP Neighbor Health Check

### Features

- Connects to multiple Cisco routers
- Retrieves BGP neighbor information
- Checks neighbor state
- Identifies Idle and Active neighbors
- Displays prefixes received
- Collects neighbor uptime
- Generates CSV health reports

- ## Configuration Drift Checker

### Features

- Connects to Cisco devices using Netmiko
- Retrieves running configuration
- Compares against a baseline configuration
- Detects missing configuration lines
- Detects extra configuration lines
- Detects modified configuration
- Generates detailed drift reports

- ## OSPF Neighbor Health Check

### Features

- Connects to Cisco devices using Netmiko
- Retrieves OSPF neighbor information
- Detects neighbors not in FULL state
- Collects dead timer information
- Generates CSV health reports
- Displays neighbor health summary

- ## Interface Error Monitor

### Features

- Connects to Cisco devices using Netmiko
- Retrieves interface operational status
- Identifies interfaces that are up or down
- Generates CSV interface health reports
- Displays a health summary

## Automation Workflow

1. Load Device Inventory
2. Validate Reachability
3. Establish Secure SSH Sessions
4. Execute Operational Commands
5. Parse and Validate Output
6. Generate Reports
7. Archive Results and Logs

## VLAN Audit

### Features

- Connects to Cisco devices using Netmiko
- Retrieves VLAN information
- Collects VLAN ID, Name, and Status
- Generates CSV audit reports
- Supports enterprise VLAN auditing

## MAC Address Table Audit

### Features

- Connects to Cisco devices using Netmiko
- Retrieves MAC address table entries
- Collects VLAN, MAC address, type, and interface
- Generates CSV audit reports
- Displays MAC address summary

## CDP Neighbor Audit

### Features

- Connects to Cisco devices using Netmiko
- Retrieves CDP neighbor details
- Collects neighbor hostname
- Collects neighbor management IP
- Displays local and remote interfaces
- Generates CSV audit reports

## ARP Table Audit

### Features

- Connects to Cisco devices using Netmiko
- Retrieves ARP table entries
- Collects IP address, MAC address, interface, and entry type
- Generates CSV audit reports
- Displays ARP table summary

## LLDP Neighbor Audit

### Features

- Connects to Cisco and Arista devices using Netmiko
- Retrieves LLDP neighbor details
- Collects management IP information
- Collects platform/system description
- Displays local and remote interfaces
- Exports results to CSV

## Port-Channel Health Check

### Features

- Connects to Cisco devices using Netmiko
- Retrieves EtherChannel summary information
- Identifies Port-Channel status
- Lists member interfaces
- Generates CSV health reports
- Displays Port-Channel health summary

## HSRP Health Check

### Features

- Connects to Cisco devices using Netmiko
- Retrieves HSRP group information
- Identifies Active and Standby routers
- Detects abnormal HSRP states
- Generates CSV health reports
- Displays HSRP health summary

## VRRP Health Check

### Features

- Connects to Cisco devices using Netmiko
- Retrieves VRRP group information
- Identifies Master and Backup routers
- Detects abnormal VRRP states
- Generates CSV health reports
- Displays VRRP health summary

## Interface Utilization Monitor

### Features

- Connects to Cisco devices using Netmiko
- Collects interface input and output utilization
- Detects high-utilization interfaces
- Generates CSV utilization reports
- Displays interface utilization summary

## CPU and Memory Health Check

### Features

- Connects to Cisco devices using Netmiko
- Monitors CPU utilization
- Monitors memory utilization
- Identifies devices exceeding utilization thresholds
- Generates CSV health reports
- Displays CPU and memory health summary
