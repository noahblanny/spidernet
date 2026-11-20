# Architecture and limitations

SpiderNet uses an explicitly supplied IPv4 host or CIDR range. A bounded, concurrent TCP probe checks common ports (22, 80, 443, 445, 3389). Successful connections are treated as reachability evidence; reverse DNS is attempted. SQLite records observations and user-supplied classifications, while Flask renders a read-only dashboard.

## Important limitations
- **Not a comprehensive network scanner:** Devices with no open probed ports may be missed.
- **No automatic MAC discovery:** MAC fields are manually entered and should be verified.
- **No continuous monitoring:** Last seen is the time of the last successful scan, not a real-time online indicator.
- **No authentication:** The Flask server listens only on localhost by default.
- **No Suricata integration yet:** Correlation is a future enhancement.
- **Not the original project source:** This implementation was rebuilt for the portfolio based on the described SpiderNet project.

## Suggested validation
1. Scan a controlled subnet with a known listening TCP service.
2. Confirm the responsive host appears in `devices` and the dashboard.
3. Label the device and confirm classification persists.
4. Re-run a scan and verify `last_seen` updates.
5. Test a host with all probed ports filtered and document the false-negative limitation.
