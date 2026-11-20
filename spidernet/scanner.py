"""Bounded TCP reachability probing for authorized IPv4 networks."""
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor

PORTS = (22, 80, 443, 445, 3389)
MAX_ADDRESSES = 256

def addresses_for(target):
    network = ipaddress.ip_network(target, strict=False)
    if network.version != 4:
        raise ValueError("Only IPv4 is supported")
    if network.num_addresses > MAX_ADDRESSES:
        raise ValueError("Limit each scan to 256 addresses or fewer")
    if network.prefixlen == 32:
        return [str(network.network_address)]
    return [str(ip) for ip in network.hosts()]

def probe(ip):
    for port in PORTS:
        try:
            with socket.create_connection((ip, port), timeout=0.35):
                return (ip, resolve(ip))
        except (OSError, TimeoutError):
            continue
    return None

def resolve(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except (OSError, socket.herror):
        return None

def scan(target):
    addresses = addresses_for(target)
    with ThreadPoolExecutor(max_workers=16) as pool:
        results = [result for result in pool.map(probe, addresses) if result]
    return len(addresses), results
