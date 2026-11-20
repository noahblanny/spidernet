"""SpiderNet command-line interface."""
import argparse
import ipaddress
from . import storage
from .scanner import scan

def main():
    parser = argparse.ArgumentParser(description="SpiderNet authorized network inventory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    scanner = sub.add_parser("scan")
    scanner.add_argument("target", help="IPv4 host or CIDR on an authorized network")
    sub.add_parser("devices")
    label = sub.add_parser("label")
    label.add_argument("ip")
    label.add_argument("--name", required=True)
    label.add_argument("--known", action="store_true")
    label.add_argument("--mac", help="Optional manually verified MAC address")
    serve = sub.add_parser("serve")
    serve.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    storage.initialize()

    if args.command == "init":
        print(f"Database initialized: {storage.db_path()}")
    elif args.command == "scan":
        checked, found = scan(args.target)
        for ip, hostname in found:
            storage.record_device(ip, hostname)
            print(f"Responsive: {ip} {hostname or ''}")
        storage.record_scan(args.target, checked, len(found))
        print(f"Checked {checked} addresses; {len(found)} responded on configured TCP ports.")
        print("No response does not prove a device is offline.")
    elif args.command == "devices":
        for item in storage.list_devices():
            print(f"{item['ip']:16} {item['friendly_name'] or item['hostname'] or '-':30} {'known' if item['known'] else 'unknown'}")
    elif args.command == "label":
        ip = str(ipaddress.IPv4Address(args.ip))
        if not storage.label_device(ip, args.name, args.known, args.mac):
            parser.error("Device not found; scan or import it first")
        print(f"Updated {ip}")
    elif args.command == "serve":
        from .web import create_app
        create_app().run(host="127.0.0.1", port=args.port, debug=False)

if __name__ == "__main__":
    main()
