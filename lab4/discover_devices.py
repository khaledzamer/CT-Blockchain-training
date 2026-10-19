"""
Lab 4 - Who is on my network?

Run this on YOUR LAPTOP (not in Codespaces - a Codespace is a cloud
machine and cannot see the classroom network).

    python discover_devices.py

Only standard Python is used - nothing to install.
Only scan the training network you were given permission to scan.
"""

import ipaddress
import platform
import re
import shutil
import socket
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

SYSTEM = platform.system()


def my_ip():
    # No packet is actually sent - this just asks the OS which interface it would use
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()


def ping(ip):
    if SYSTEM == "Windows":
        cmd = ["ping", "-n", "1", "-w", "500", ip]
    elif SYSTEM == "Darwin":
        cmd = ["ping", "-c", "1", "-W", "500", ip]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", ip]
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Windows returns success even for "Destination host unreachable", so check for a real reply
    return result.returncode == 0 and (SYSTEM != "Windows" or "TTL=" in result.stdout.upper())


def normalize_mac(mac):
    parts = re.split(r"[:-]", mac)
    return ":".join(p.zfill(2) for p in parts).lower()


def read_arp_table():
    # Newer Linux systems may not have "arp" - "ip neigh" shows the same table
    cmd = ["arp", "-a"] if shutil.which("arp") else ["ip", "neigh"]
    try:
        output = subprocess.run(cmd, capture_output=True, text=True).stdout
    except FileNotFoundError:
        return {}
    table = {}
    for line in output.splitlines():
        ip = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", line)
        mac = re.search(r"([0-9a-fA-F]{1,2}(?:[:-][0-9a-fA-F]{1,2}){5})", line)
        if ip and mac:
            table[ip.group(1)] = normalize_mac(mac.group(1))
    return table


def hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except OSError:
        return "-"


def main():
    if not shutil.which("ping"):
        sys.exit("The 'ping' command was not found. Are you running this on your laptop (not Codespaces)?")
    try:
        me = my_ip()
    except OSError:
        sys.exit("No network found. Connect to the training Wi-Fi and try again.")
    network = ipaddress.ip_network(me + "/24", strict=False)
    print(f"My IP address : {me}")
    print(f"Scanning      : {network}  (this takes about 30 seconds)\n")

    hosts = [str(h) for h in network.hosts()]
    with ThreadPoolExecutor(max_workers=64) as pool:
        replied = {ip for ip, ok in zip(hosts, pool.map(ping, hosts)) if ok}

    # Devices that ignore ping still show up in the ARP table once we tried to reach them
    arp = {ip: mac for ip, mac in read_arp_table().items() if ipaddress.ip_address(ip) in network}
    found = sorted(replied | set(arp) | {me}, key=ipaddress.ip_address)

    print(f"{'IP address':<16} {'MAC address':<18} {'Ping':<5} Hostname")
    print("-" * 70)
    for ip in found:
        mac = arp.get(ip, "(this laptop)" if ip == me else "-")
        print(f"{ip:<16} {mac:<18} {'yes' if ip in replied else 'no':<5} {hostname(ip)}")

    print(f"\nTotal devices found: {len(found)}")
    print("Tip: look up the first 6 characters of a MAC at https://maclookup.app to see the maker.")


if __name__ == "__main__":
    main()
