"""
Code to find possible dos attack
"""
import os
import time
from collections import defaultdict
from scapy.all import sniff, IP


def packet_callback(packet):
    ''' Function to block ip address
    '''

    # Store ip address
    src_ip = packet[IP].src
    # This syntax will rise an error with a normal dictionary (packet_count = {})
    # With a normal dictionary you must first create the entry and then add 1
    packet_count[src_ip] += 1

    # Compute time interval
    current_time  = time.time()
    time_interval = current_time - start_time[0]

    # If we recive more than one packet per second
    if time_interval >= 1:

        # Loop over all ip found
        for ip, count in packet_count.items():

            # Compute the rate
            packet_rate = count / time_interval
            print(f"IP: {ip}, Packet rate: {packet_rate}")

            # Blocking ip with high rate
            if packet_rate > Rate_th and ip not in blocked_ips:
                print(f"Blocking IP: {ip}, packet rate: {packet_rate}")
                # Uncomment to block
                #os.system(f"iptables -A INPUT -s {ip} -j DROP")
                blocked_ips.append(ip)

        # Clear for the next iteration
        packet_count.clear()
        start_time[0] = current_time


# Number of packet per second that can be accepted
Rate_th = int(input("Rate above which to block the IP: "))

if os.geteuid() != 0:
    print("Some functionalities requires root privileges")
    exit()

packet_count = defaultdict(int)
# It must be in a list otherwise the function packet_callback won't read it
start_time   = [time.time()]
blocked_ips  = []

print("Start sniffing network traffic...")
sniff(filter="ip", prn=packet_callback)
