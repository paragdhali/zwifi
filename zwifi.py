import os
import subprocess
import time

def run_command(command):
    """ Run a shell command and return output """
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"Error: {process.stderr}")
    return process.stdout

def setup_monitor_mode(interface):
    print(f"Setting up monitor mode on {interface}...")
    run_command(f"airmon-ng check kill")
    run_command(f"airmon-ng start {interface}")
    return f"{interface}mon"

def start_airbase_ng(mon_interface, ssid):
    print(f"Starting airbase-ng on {mon_interface} with SSID {ssid}...")
    return subprocess.Popen(f"airbase-ng -e '{ssid}' -c 6 {mon_interface}", shell=True)

def configure_bridge():
    print("Configuring bridge...")
    run_command("brctl addbr br0")
    run_command("brctl addif br0 eth0")  # Adjust if using a different wired interface
    run_command("ip link set br0 up")
    run_command("ip addr add 192.168.1.1/24 dev br0")
    
    print("Enabling NAT...")
    run_command("echo 1 > /proc/sys/net/ipv4/ip_forward")
    run_command("iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
    run_command("iptables -A FORWARD -i br0 -o eth0 -j ACCEPT")
    run_command("iptables -A FORWARD -i eth0 -o br0 -m state --state RELATED,ESTABLISHED -j ACCEPT")

def start_dhcp_server():
    print("Starting DHCP server...")
    dhcp_config = """default-lease-time 600;
max-lease-time 7200;
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8;
} """
    with open("/etc/dhcp/dhcpd.conf", "w") as f:
        f.write(dhcp_config)
    run_command("service isc-dhcp-server restart")

def main():
    interface = "wlan0"  # Change if needed
    ssid = "FreeWiFi"  # Change your SSID
    
    mon_interface = setup_monitor_mode(interface)
    airbase_process = start_airbase_ng(mon_interface, ssid)
    time.sleep(5)
    
    configure_bridge()
    start_dhcp_server()
    
    print("WiFi Hotspot is running...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping hotspot...")
        airbase_process.terminate()
        run_command("airmon-ng stop wlan0mon")
        run_command("brctl delbr br0")
        run_command("iptables -t nat -F")
        run_command("echo 0 > /proc/sys/net/ipv4/ip_forward")
        run_command("service isc-dhcp-server stop")
        print("Hotspot stopped.")

if __name__ == "__main__":
    main()
