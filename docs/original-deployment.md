# Original Spider-Net deployment — evidence notes

## Source of these observations

Three screenshots captured in September 2026 show the **original** Spider-Net environment. They are distinct from the clean Python/Flask/SQLite implementation currently in this repository.

## Original dashboard

The captured web UI is labeled **Spider-Net — Network device inventory**. It includes:

- Cards showing **18 Devices Online**, **16 Known Devices**, and **26 Unknown Devices** at the time of capture
- Device name, IPv4 address, MAC address, online status, first-seen timestamp, last-seen timestamp
- A **Rename** input and **Save** button on each visible device row

These counts are **historical observations from the screenshot**. The three counters need not sum to the same total because they measure different categories.

## Infrastructure screenshot

The Proxmox console screenshot shows:

- Proxmox VE **9.2.20** on host `homeweb`
- VM **101 (`spidernet`)**, alongside the separate Spider-Sense and Suricata VMs
- Original project files including `app.py`, `scanner.py`, `devices.db`, `names.json`, `spidernet-scanner.service`, and `spidernet-web.service`
- A `spidernet-scanner.service` unit shown as **active (running)** at capture time
- A `spidernet-web.service` unit shown as **enabled**; the screenshot does not establish that it was actively running at that particular instant

## Differences from the code in this repository

| Capability | Original screenshot evidence | Current portfolio implementation |
| --- | --- | --- |
| Flask dashboard | Visible | Implemented |
| IP address inventory | Visible | Implemented |
| MAC address inventory | Visible | Manual entry only |
| Device rename from web UI | Visible | CLI labeling only |
| Online/known/unknown dashboard cards | Visible | Stored inventory and known/unknown counts; no live online-state tracking |
| First/last seen | Visible | Stored timestamps for responsive probes |
| Background systemd scanner | Visible as running | Not included; scans invoked through CLI |
| Suricata integration | Not established by screenshots | Not implemented |

## Privacy handling

The original images include local IP addresses, MAC identifiers, device names, Proxmox management details, and console output. Only heavily sanitized images should be used in a public README. Mask identifiers with **opaque redaction**, not soft blur, and never publish the unredacted original.

## Next engineering steps

1. Add tested automatic ARP/MAC collection for authorized local subnets.
2. Add device rename functionality to the dashboard with CSRF protection and authentication before remote access.
3. Add scan scheduling and service definitions with secure execution permissions.
4. Add a meaningful online/offline state model and clarify stale data.
5. Publish reproducible tests and screenshots from a synthetic inventory.
