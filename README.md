# ZWiFi

ZWiFi is a script to set up a WiFi hotspot using `airbase-ng` and other networking tools on a Linux system.

## Dependencies

Ensure the following dependencies are installed on your system:

- `airmon-ng`
- `airbase-ng`
- `brctl`
- `iptables`
- `service`
- `isc-dhcp-server`

You can install these dependencies using your package manager. For example, on Debian-based systems:

```bash
sudo apt-get update
sudo apt-get install aircrack-ng bridge-utils iptables isc-dhcp-server
```

## Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/zwifi.git
cd zwifi
```

2. Run the script:

```bash
sudo python3 zwifi.py
```

3. The script will set up a WiFi hotspot with the SSID `FreeWiFi` on channel 6 using the `wlan0` interface. You can modify these values in the `main` function of `zwifi.py`.

## Stopping the Hotspot

To stop the hotspot, press `Ctrl+C`. The script will clean up and restore your network settings.

## License

This project is licensed under the MIT License.