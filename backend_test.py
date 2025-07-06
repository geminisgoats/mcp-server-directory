import requests
import unittest
import json
import sys
from datetime import datetime

class MCPServerDirectoryAPITester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(MCPServerDirectoryAPITester, self).__init__(*args, **kwargs)
        self.base_url = "https://9d62fb2e-71bc-4234-b39e-8606f8363a98.preview.emergentagent.com/api"
        self.test_server_id = "1"  # Using the first server from seed data

    def test_01_root_endpoint(self):
        """Test the root API endpoint"""
        print("\n🔍 Testing root endpoint...")
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "MCP Server Directory API")
        print("✅ Root endpoint test passed")

    def test_02_get_all_servers(self):
        """Test getting all servers"""
        print("\n🔍 Testing get all servers endpoint...")
        response = requests.get(f"{self.base_url}/servers")
        self.assertEqual(response.status_code, 200)
        servers = response.json()
        self.assertIsInstance(servers, list)
        self.assertGreaterEqual(len(servers), 8)  # Should have at least 8 servers from seed data
        print(f"✅ Get all servers test passed - Found {len(servers)} servers")

    def test_03_get_server_by_id(self):
        """Test getting a specific server by ID"""
        print(f"\n🔍 Testing get server by ID endpoint for server {self.test_server_id}...")
        response = requests.get(f"{self.base_url}/servers/{self.test_server_id}")
        self.assertEqual(response.status_code, 200)
        server = response.json()
        self.assertEqual(server["id"], self.test_server_id)
        self.assertEqual(server["name"], "SEO Master Pro")  # From seed data
        print("✅ Get server by ID test passed")

    def test_04_filter_servers_by_category(self):
        """Test filtering servers by category"""
        print("\n🔍 Testing filter servers by category...")
        category = "SEO Analytics"
        response = requests.get(f"{self.base_url}/servers?category={category}")
        self.assertEqual(response.status_code, 200)
        servers = response.json()
        self.assertGreaterEqual(len(servers), 1)
        for server in servers:
            self.assertEqual(server["category"], category)
        print(f"✅ Filter by category test passed - Found {len(servers)} servers in {category}")

    def test_05_filter_servers_by_pricing_model(self):
        """Test filtering servers by pricing model"""
        print("\n🔍 Testing filter servers by pricing model...")
        pricing_model = "Freemium"
        response = requests.get(f"{self.base_url}/servers?pricing_model={pricing_model}")
        self.assertEqual(response.status_code, 200)
        servers = response.json()
        self.assertGreaterEqual(len(servers), 1)
        for server in servers:
            self.assertEqual(server["pricing_model"], pricing_model)
        print(f"✅ Filter by pricing model test passed - Found {len(servers)} {pricing_model} servers")

    def test_06_search_servers(self):
        """Test searching servers"""
        print("\n🔍 Testing search servers...")
        search_term = "SEO"
        response = requests.get(f"{self.base_url}/servers?search={search_term}")
        self.assertEqual(response.status_code, 200)
        servers = response.json()
        self.assertGreaterEqual(len(servers), 1)
        print(f"✅ Search servers test passed - Found {len(servers)} servers matching '{search_term}'")

    def test_07_get_featured_servers(self):
        """Test getting featured servers"""
        print("\n🔍 Testing get featured servers endpoint...")
        response = requests.get(f"{self.base_url}/featured-servers")
        self.assertEqual(response.status_code, 200)
        servers = response.json()
        self.assertGreaterEqual(len(servers), 1)
        for server in servers:
            self.assertTrue(server["is_featured"])
        print(f"✅ Get featured servers test passed - Found {len(servers)} featured servers")

    def test_08_get_sponsored_servers(self):
        """Test getting sponsored servers"""
        print("\n🔍 Testing get sponsored servers endpoint...")
        response = requests.get(f"{self.base_url}/sponsored-servers")
        self.assertEqual(response.status_code, 200)
        servers = response.json()
        self.assertGreaterEqual(len(servers), 1)
        for server in servers:
            self.assertTrue(server["is_sponsored"])
        print(f"✅ Get sponsored servers test passed - Found {len(servers)} sponsored servers")

    def test_09_get_categories(self):
        """Test getting all categories"""
        print("\n🔍 Testing get categories endpoint...")
        response = requests.get(f"{self.base_url}/categories")
        self.assertEqual(response.status_code, 200)
        categories = response.json()
        self.assertIsInstance(categories, list)
        self.assertGreaterEqual(len(categories), 8)  # Should have 8 categories from the enum
        print(f"✅ Get categories test passed - Found {len(categories)} categories")

    def test_10_track_click(self):
        """Test click tracking functionality"""
        print("\n🔍 Testing click tracking endpoint...")
        click_data = {
            "server_id": self.test_server_id,
            "user_ip": "127.0.0.1",
            "user_agent": "Test Agent",
            "click_type": "affiliate"
        }
        response = requests.post(f"{self.base_url}/track-click", json=click_data)
        self.assertEqual(response.status_code, 200)
        click = response.json()
        self.assertEqual(click["server_id"], self.test_server_id)
        self.assertEqual(click["click_type"], "affiliate")
        print("✅ Click tracking test passed")

    def test_11_get_server_stats(self):
        """Test getting server statistics"""
        print("\n🔍 Testing get server stats endpoint...")
        response = requests.get(f"{self.base_url}/stats/{self.test_server_id}")
        self.assertEqual(response.status_code, 200)
        stats = response.json()
        self.assertEqual(stats["server_id"], self.test_server_id)
        self.assertIn("total_clicks", stats)
        self.assertIn("affiliate_clicks", stats)
        print("✅ Get server stats test passed")

    def test_12_get_analytics(self):
        """Test getting overall analytics"""
        print("\n🔍 Testing get analytics endpoint...")
        response = requests.get(f"{self.base_url}/analytics")
        self.assertEqual(response.status_code, 200)
        analytics = response.json()
        self.assertIn("total_servers", analytics)
        self.assertIn("total_clicks", analytics)
        self.assertIn("featured_servers", analytics)
        self.assertIn("sponsored_servers", analytics)
        print("✅ Get analytics test passed")

def run_tests():
    """Run all API tests"""
    test_suite = unittest.TestLoader().loadTestsFromTestCase(MCPServerDirectoryAPITester)
    test_result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    return 0 if test_result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())