"""Unit tests for target and port validation."""
import unittest
from utils.validators import parse_local_network, parse_ports, parse_private_target


class ValidatorTests(unittest.TestCase):
    def test_private_target_accepted(self):
        self.assertEqual(str(parse_private_target("192.168.1.10")), "192.168.1.10")

    def test_public_target_rejected(self):
        with self.assertRaises(ValueError):
            parse_private_target("8.8.8.8")

    def test_ipv6_rejected(self):
        with self.assertRaises(ValueError):
            parse_private_target("::1")

    def test_local_network_must_contain_device(self):
        self.assertEqual(str(parse_local_network("192.168.1.0/24", "192.168.1.5")), "192.168.1.0/24")
        with self.assertRaises(ValueError):
            parse_local_network("192.168.2.0/24", "192.168.1.5")

    def test_network_size_limited(self):
        with self.assertRaises(ValueError):
            parse_local_network("10.0.0.0/16", "10.0.0.5")

    def test_port_count_and_range_limited(self):
        self.assertEqual(parse_ports("80,443,80"), [80, 443])
        with self.assertRaises(ValueError):
            parse_ports(",".join(str(p) for p in range(1, 34)))
        with self.assertRaises(ValueError):
            parse_ports("0")


if __name__ == "__main__":
    unittest.main()
