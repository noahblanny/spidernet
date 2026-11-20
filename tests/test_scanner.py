import unittest
from spidernet.scanner import addresses_for

class ScannerTests(unittest.TestCase):
    def test_single_ip(self):
        self.assertEqual(addresses_for("192.0.2.10"), ["192.0.2.10"])

    def test_small_network(self):
        self.assertEqual(addresses_for("192.0.2.0/30"), ["192.0.2.1", "192.0.2.2"])

    def test_reject_large_scan(self):
        with self.assertRaises(ValueError):
            addresses_for("10.0.0.0/16")

    def test_reject_ipv6(self):
        with self.assertRaises(ValueError):
            addresses_for("2001:db8::1")

if __name__ == "__main__":
    unittest.main()
