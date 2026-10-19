# Lab 4 – Who Is on My Network? (Device Identification)

> ⚠️ Do this lab **on your own laptop**, not in Codespaces.
> Codespaces runs in the cloud and cannot see the classroom Wi-Fi.
>
> Only scan the training network your instructor gave you. Scanning other
> networks without permission may be illegal.

**Why this matters for blockchain:** a blockchain is a network of peers (nodes).
Before you trust a network, you should know who is on it.

---

## Part A – Built-in commands (5 minutes)

### 1. Find your own IP address and gateway

| Windows (Command Prompt) | macOS / Linux (Terminal) |
|---|---|
| `ipconfig` | `ifconfig` or `ip addr` |

Write down:
- My IP address: `____________`
- Default gateway (the router): `____________`

### 2. See the devices your laptop already knows

```
arp -a
```

Works on Windows, macOS and Linux. Each line is a device: **IP address + MAC address**.

### 3. Ping the router

```
ping <your gateway IP>
```

(On macOS/Linux press `Ctrl + C` to stop.)

---

## Part B – Scan the whole network (5 minutes)

Download `lab4/discover_devices.py` to your laptop and run:

```
python discover_devices.py
```

(Use `python3` on macOS/Linux if `python` doesn't work.)

The script pings every address on your network and prints a table:

```
IP address       MAC address        Ping  Hostname
----------------------------------------------------------------------
192.168.1.1      a4:2b:b0:12:34:56  yes   router.local
192.168.1.23     (this laptop)      yes   my-laptop
192.168.1.40     3c:22:fb:ab:cd:ef  no    -
```

**Ping = no** but still listed? That device has a firewall that blocks ping, but it still had to answer at the network level (ARP), so it is still visible.

---

## Part C – Identify the devices (5 minutes)

1. Copy the first 6 characters of a MAC address (for example `a4:2b:b0`).
2. Look it up at https://maclookup.app to see the manufacturer (Apple, Samsung, Cisco…).
3. Fill in the table:

| # | IP address | Manufacturer | My guess (phone, laptop, router, printer…) |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## Discussion questions

1. How many devices did you find? Did everyone in the class get the same number? Why or why not?
2. Which device is the router? How do you know?
3. Some phones show a "random" MAC address. Why would a phone do that?
4. A blockchain node can see the IP addresses of the peers it connects to. What privacy risk does that create?
