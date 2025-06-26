# IoT Endpoint Firewall with MUD & IPTables

This project implements a system to secure IoT devices on a home network by restricting their communications to only approved endpoints. The system is built around the Manufacturer Usage Description (MUD) framework standardized in [RFC 8520](https://datatracker.ietf.org/doc/html/rfc8520), and it aims to enforce endpoint restrictions using a home router script and dynamically generated IPTables firewall rules.

> 🛡️ Designed at Columbia University's Internet Real-Time Lab (Fall 2019)

## 🔍 Motivation

As IoT devices proliferate in homes and businesses, they introduce new security challenges. These devices are often:

* Underpowered and unable to run traditional security software
* Designed for non-technical users (e.g., unchanged default passwords)
* Poorly maintained and rarely patched

These factors make IoT devices easy targets for malware and botnets (e.g., the [Mirai Botnet](https://www.cloudflare.com/learning/ddos/mirai-botnet/)), which can cause massive disruptions to internet infrastructure.

The MUD architecture offers a promising solution by allowing each IoT device to specify the endpoints it should communicate with. However, adoption is limited. This project extends the MUD idea by enabling firewall rule generation both for:

* Devices that provide a MUD URL (per RFC 8520), and
* Devices without MUD support, using a community-sourced MUD-like server.

## 🧠 Project Architecture

This project has two core components:

### 1. **Router Script**

A Python script running on a DD-WRT router:

* Monitors DHCP traffic to detect new devices
* Classifies devices as IoT vs general-purpose (based on DHCP fields and MAC address)
* Retrieves a MUD or MUD-like file:

  * From the device itself (via DHCP option 161), or
  * From a MUD-like Crowd-Source Server (MCS)
* Translates the MUD rules into outbound IPTables firewall rules
* Maintains a persistent database of known devices and rules (MongoDB)
* Supports DNS resolution and automatic rule updates as IPs for domains change

### 2. **MUD-like Crowd-Source Server (MCS)**

A proposed distributed system where academic labs and institutions contribute and host MUD-like files for IoT devices that don’t support MUD. Though not implemented in this repo, the router script is designed with future MCS integration in mind.

## 💪 Testing Tools

To validate the router script, the following tools were developed:

* **IoT Traffic Generator**: Simulates DHCP and network traffic from a configurable IoT device (e.g., Amazon Echo). Tests both allowed and blocked endpoints using a real or hosted MUD file.
* **DNS Resolution Test**: Simulates a device connecting to a domain whose IP changes rapidly (e.g., Amazon S3) to test dynamic DNS rule updates.

## ✅ Features

* Prevents communication with forbidden endpoints
* Automatically applies MUD or MUD-like policies
* Modular codebase (PacketHandler, FirewallManager, DeviceChain, DatabaseManager)
* Memory-leak free and built for long runtimes
* Restores firewall state on reboot from persistent database
* Partial handling of dynamic DNS (intercepts DNS requests, not responses)

## 📁 Repository Structure

```
.
├── MUDfiles/                     # Example MUD JSON files for various IoT devices
│   ├── AmazonEcho.json
│   ├── HueBulb.json
│   ├── NetatmoWeatherStation.json
│   ├── RingDoorbell.json
│   └── TribySpeaker.json
├── README.md                     # Project documentation
├── Router/                       # Core router scripts
│   ├── DatabaseManager.py        # MongoDB interface
│   ├── DeviceChain.py            # IPTables chain management per device
│   ├── FirewallManager.py        # IPTables firewall rules management
│   ├── PacketHandler.py          # DHCP & DNS packet parsing
│   ├── PacketHandlerUtils.py     # Helper utilities for packet handling
│   ├── gmud_decode.py            # MUD file parsing and decoding
│   └── sniffer.py                # Packet sniffing logic
├── TestTools/                   # Testing and simulation utilities
│   ├── README.md
│   ├── gmud_decode.py            # Duplicate or testing MUD parser
│   ├── test.py                   # Test scripts
│   ├── test_devices.py           # Test device definitions and MUD mappings
│   └── test_utils.py             # Utility functions for tests

```

## 🚀 Getting Started

### Prerequisites

* Python 2.7/3.x
* DD-WRT or OpenWRT router with Python support
* [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or local MongoDB instance
* [Scapy](https://scapy.net/) for packet sniffing
* Dependencies:

  * `scapy`
  * `dnspython`
  * `mongoengine`
  * `ssl`
  * `urllib2`

### Quick Start

1. **Set up MongoDB:**

   * Create a cluster (e.g. on Atlas)
   * Whitelist router IP
   * Replace the `dbURL` in `sniffer.py` with your connection string

2. **Run Router Script:**

   ```bash
   python sniffer.py
   ```

3. **Simulate Device (on another machine):**

   ```bash
   sudo python test.py HueBulb.json
   ```

## 🧐 Known Limitations

* Incomplete support for MCS (device identification remains in development)
* DNS interception uses request sniffing only (cannot fully resolve IP discrepancies)
* DNS mappings are sometimes out of sync with the device’s actual resolution results

## 🔬 Future Work

* Move MongoDB to run locally on the router
* Fully integrate MCS for legacy devices
* Implement DNS response interception for higher fidelity
* Extend firewalling to include inbound traffic (optional)

## 🧑‍💻 Author

**Gabriel Brown**
🔪 Columbia Internet Real-Time Lab
📧 [gb2582@columbia.edu](mailto:gb2582@columbia.edu)
📝 [Technical Report (PDF)](./IRT_final_report.pdf)

## 📜 License

This project was originally developed for academic research at Columbia University. Licensing TBD.
