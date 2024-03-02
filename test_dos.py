from scapy.all import Ether, IP, TCP, sendp


def send_packets(target_ip, interface, N):
    '''
    Function to create and send packet

    Parameters
    ----------
    target_ip : string
        ip of the target machine
    interface : string
        network interface (e.g. eth0, wlan0)
    N : int
        number of packets
    '''
    packet = Ether() / IP(dst=target_ip) / TCP()

    for _ in range(N):
        sendp(packet, iface=interface)


TARGET_IP = ""
INTERFACE = "wlan0"
N         = 100

send_packets(TARGET_IP, INTERFACE, N)
