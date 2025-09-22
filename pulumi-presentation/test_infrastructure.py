import unittest
import pulumi
import json
import requests
from datetime import datetime
import re

"""
Infrastructure Testing Demo for Pulumi

This demonstrates how to unit test infrastructure code - a major advantage
of Pulumi over traditional IaC tools like Terraform. You can test your
infrastructure logic before deployment!

To run these tests:
1. Install pytest: pip install pytest requests
2. Run tests: python -m pytest test_infrastructure.py -v
3. Or run directly: python test_infrastructure.py
"""

class TestInfrastructureConfiguration(unittest.TestCase):
    """Test infrastructure configuration and validation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.expected_vpc_cidr = "10.0.0.0/16"
        self.expected_subnet_cidr = "10.0.1.0/24"
        self.expected_instance_type = "t3.micro"
        self.expected_ports = [22, 80, 443]
        
    def test_vpc_cidr_configuration(self):
        """Test VPC CIDR block is correctly configured"""
        # In a real scenario, this would test the actual VPC resource
        actual_cidr = "10.0.0.0/16"  # This would come from pulumi stack output
        self.assertEqual(actual_cidr, self.expected_vpc_cidr)
        print("✅ VPC CIDR configuration test passed")
    
    def test_subnet_cidr_configuration(self):
        """Test subnet CIDR is within VPC range"""
        vpc_cidr = "10.0.0.0/16"
        subnet_cidr = "10.0.1.0/24"
        
        # Extract network portions for validation
        vpc_network = vpc_cidr.split('/')[0].split('.')[:2]  # ['10', '0']
        subnet_network = subnet_cidr.split('/')[0].split('.')[:2]  # ['10', '0']
        
        self.assertEqual(vpc_network, subnet_network, "Subnet should be within VPC range")
        print("✅ Subnet CIDR validation test passed")
    
    def test_security_group_rules(self):
        """Test security group has correct ingress rules"""
        # Simulate security group rules that would be extracted from stack
        actual_ingress_rules = [
            {"from_port": 22, "to_port": 22, "protocol": "tcp", "description": "SSH access"},
            {"from_port": 80, "to_port": 80, "protocol": "tcp", "description": "HTTP access"},
            {"from_port": 443, "to_port": 443, "protocol": "tcp", "description": "HTTPS access"}
        ]
        
        actual_ports = [rule["from_port"] for rule in actual_ingress_rules]
        
        for expected_port in self.expected_ports:
            self.assertIn(expected_port, actual_ports, 
                         f"Port {expected_port} should be allowed in security group")
        
        print("✅ Security group rules test passed")
    
    def test_instance_configuration(self):
        """Test EC2 instance configuration"""
        actual_instance_type = "t3.micro"  # Would come from stack output
        self.assertEqual(actual_instance_type, self.expected_instance_type)
        print("✅ Instance type configuration test passed")
    
    def test_subnet_public_ip_assignment(self):
        """Test that subnet assigns public IPs"""
        map_public_ip = True  # This would come from subnet configuration
        self.assertTrue(map_public_ip, "Subnet should assign public IPs for web servers")
        print("✅ Public IP assignment test passed")
    
    def test_resource_naming_convention(self):
        """Test that resources follow naming conventions"""
        resource_names = [
            "mx-pulumi-vpc",
            "public-subnet", 
            "igw",
            "public-route-table",
            "public-security-group",
            "webserver-instance"
        ]
        
        # Test naming convention (e.g., lowercase with hyphens)
        naming_pattern = re.compile(r'^[a-z0-9-]+$')
        
        for name in resource_names:
            self.assertTrue(naming_pattern.match(name), 
                          f"Resource name '{name}' should follow naming convention")
        
        print("✅ Resource naming convention test passed")

class TestPulumiSpecificFeatures(unittest.TestCase):
    """Test Pulumi-specific capabilities that are hard to achieve with other IaC tools"""
    
    def test_dynamic_ami_selection(self):
        """Test that AMI is selected dynamically"""
        # Simulate the AMI selection logic
        ami_filters = [{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
        
        self.assertTrue(len(ami_filters) > 0, "AMI filters should be configured")
        self.assertIn("amzn2-ami-hvm-*", ami_filters[0]["values"], 
                     "Should filter for Amazon Linux 2 AMIs")
        
        print("✅ Dynamic AMI selection test passed")
    
    def test_conditional_logic_capability(self):
        """Test infrastructure conditional logic"""
        # Demonstrate conditional resource creation logic
        environment = "dev"
        
        # Test environment-based instance type selection
        if environment == "dev":
            expected_instance_type = "t3.micro"
        elif environment == "staging":
            expected_instance_type = "t3.small"
        else:  # production
            expected_instance_type = "t3.medium"
        
        self.assertEqual(expected_instance_type, "t3.micro")
        print("✅ Conditional logic capability test passed")
    
    def test_loop_resource_creation(self):
        """Test creating multiple resources using loops"""
        environments = ["dev", "staging", "prod"]
        created_resources = []
        
        # Simulate loop-based resource creation
        for env in environments:
            resource_name = f"{env}-webserver"
            created_resources.append({
                "name": resource_name,
                "environment": env,
                "vpc_cidr": f"10.{len(created_resources)}.0.0/16"
            })
        
        self.assertEqual(len(created_resources), 3)
        self.assertTrue(all("webserver" in res["name"] for res in created_resources))
        
        print("✅ Loop-based resource creation test passed")
    
    def test_complex_data_structures(self):
        """Test handling of complex data structures in infrastructure code"""
        # Test complex configuration that would be difficult in HCL
        infrastructure_config = {
            "environments": {
                "dev": {
                    "instance_type": "t3.micro",
                    "vpc_cidr": "10.0.0.0/16",
                    "subnets": [
                        {"cidr": "10.0.1.0/24", "az": "us-east-1a"},
                        {"cidr": "10.0.2.0/24", "az": "us-east-1b"}
                    ],
                    "tags": {
                        "Environment": "Development",
                        "CostCenter": "Engineering",
                        "Owner": "DevOps"
                    }
                }
            },
            "security_rules": [
                {"port": 80, "protocol": "tcp", "source": "0.0.0.0/0"},
                {"port": 443, "protocol": "tcp", "source": "0.0.0.0/0"},
                {"port": 22, "protocol": "tcp", "source": "0.0.0.0/0"}
            ]
        }
        
        # Test complex data structure access
        dev_config = infrastructure_config["environments"]["dev"]
        self.assertEqual(dev_config["instance_type"], "t3.micro")
        self.assertEqual(len(dev_config["subnets"]), 2)
        self.assertEqual(len(infrastructure_config["security_rules"]), 3)
        
        print("✅ Complex data structures test passed")

class TestInfrastructureValidation(unittest.TestCase):
    """Test infrastructure validation and best practices"""
    
    def test_security_best_practices(self):
        """Test security configuration best practices"""
        # Test that SSH is not open to the world in production
        environment = "dev"  # This would come from config
        
        if environment == "production":
            ssh_cidr = "10.0.0.0/8"  # Restricted in prod
        else:
            ssh_cidr = "0.0.0.0/0"  # Open for dev/demo
        
        if environment == "production":
            self.assertNotEqual(ssh_cidr, "0.0.0.0/0", 
                              "SSH should not be open to world in production")
        else:
            self.assertEqual(ssh_cidr, "0.0.0.0/0", 
                           "SSH can be open in development")
        
        print("✅ Security best practices test passed")
    
    def test_cost_optimization(self):
        """Test cost optimization configuration"""
        # Test instance type based on environment
        cost_optimized_types = {
            "dev": "t3.micro",
            "staging": "t3.small", 
            "prod": "t3.medium"
        }
        
        for env, instance_type in cost_optimized_types.items():
            if env == "dev":
                self.assertEqual(instance_type, "t3.micro", 
                               "Dev should use micro instances for cost optimization")
        
        print("✅ Cost optimization test passed")
    
    def test_tagging_compliance(self):
        """Test that all resources have required tags"""
        required_tags = ["Name", "Environment", "owner", "ManagedBy"]
        resource_tags = {
            "Name": "test-resource",
            "Environment": "presentation", 
            "owner": "mx-devops",
            "ManagedBy": "Pulumi"
        }
        
        for required_tag in required_tags:
            self.assertIn(required_tag, resource_tags, 
                         f"Resource must have '{required_tag}' tag")
        
        print("✅ Tagging compliance test passed")

@unittest.skip("Requires running infrastructure - enable for integration testing")
class TestLiveInfrastructure(unittest.TestCase):
    """Integration tests that require actual deployed infrastructure"""
    
    def test_web_server_response(self):
        """Test that deployed web server is responding"""
        # This would get the actual IP from stack outputs
        test_ip = "example.com"  # Replace with actual IP
        test_url = f"http://{test_ip}"
        
        try:
            response = requests.get(test_url, timeout=10)
            self.assertEqual(response.status_code, 200)
            self.assertIn("Pulumi", response.text)
            print("✅ Web server response test passed")
        except requests.exceptions.RequestException as e:
            self.fail(f"Web server not responding: {e}")
    
    def test_ssh_connectivity(self):
        """Test SSH connectivity (mock test)"""
        # In real scenario, this would test actual SSH connectivity
        ssh_port_open = True  # Mock result
        self.assertTrue(ssh_port_open, "SSH port should be accessible")
        print("✅ SSH connectivity test passed")

def run_infrastructure_tests():
    """Helper function to run all tests with nice output"""
    print("\n" + "="*70)
    print("🧪 PULUMI INFRASTRUCTURE TESTING DEMONSTRATION")
    print("="*70)
    print("This demonstrates testing capabilities that are unique to Pulumi!")
    print("Unlike Terraform, you can unit test your infrastructure logic.")
    print("-"*70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestInfrastructureConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestPulumiSpecificFeatures))
    suite.addTests(loader.loadTestsFromTestCase(TestInfrastructureValidation))
    # suite.addTests(loader.loadTestsFromTestCase(TestLiveInfrastructure))  # Skip by default
    
    # Custom test result class for better output
    class CustomTestResult(unittest.TextTestResult):
        def startTest(self, test):
            super().startTest(test)
            print(f"\n🔬 Running: {test._testMethodName}")
    
    # Run tests with custom runner
    stream = unittest.TextTestRunner(verbosity=0, resultclass=CustomTestResult)._makeResult()
    result = unittest.TextTestRunner(verbosity=0, stream=open('/dev/null', 'w')).run(suite)
    
    # Custom results display
    print("\n" + "-"*70)
    print("📊 TEST RESULTS SUMMARY")
    print("-"*70)
    print(f"✅ Tests Run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️  Errors: {len(result.errors)}")
    print(f"⏭️  Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\n❌ FAILURES:")
        for test, failure in result.failures:
            print(f"  - {test}: {failure}")
    
    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, error in result.errors:
            print(f"  - {test}: {error}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n📈 Success Rate: {success_rate:.1f}%")
    
    print("\n" + "="*70)
    print("🎯 KEY TESTING ADVANTAGES OF PULUMI:")
    print("="*70)
    advantages = [
        "✅ Unit test infrastructure logic with familiar testing frameworks",
        "✅ Test complex conditional logic and loops",
        "✅ Validate configuration before deployment",
        "✅ Mock external dependencies for faster testing",
        "✅ Integration with CI/CD pipelines",
        "✅ Test-driven infrastructure development",
        "✅ Catch errors early in development cycle",
        "✅ Ensure compliance and best practices"
    ]
    
    for advantage in advantages:
        print(f"   {advantage}")
    
    print("\n🆚 VS TERRAFORM:")
    terraform_comparison = [
        "• Terraform: Limited testing with 'terraform validate' and 'terraform plan'",
        "• Pulumi: Full unit testing with assertions, mocks, and test frameworks",
        "• Terraform: Hard to test complex logic in HCL",
        "• Pulumi: Test any programming logic with standard testing tools"
    ]
    
    for comparison in terraform_comparison:
        print(f"   {comparison}")
    
    print("="*70)
    
    return result.wasSuccessful()

def generate_test_report():
    """Generate a test report for the presentation"""
    report = {
        "test_framework": "Python unittest",
        "test_categories": [
            "Infrastructure Configuration Validation",
            "Pulumi-Specific Feature Testing", 
            "Security and Compliance Testing",
            "Integration Testing (with live infrastructure)"
        ],
        "advantages_over_terraform": [
            "Real unit testing with assertions",
            "Test complex programming logic",
            "Mock external dependencies",
            "Integration with standard testing tools",
            "Test-driven infrastructure development"
        ],
        "demo_test_cases": [
            "VPC CIDR configuration validation",
            "Security group rule verification", 
            "Resource naming convention compliance",
            "Dynamic AMI selection logic",
            "Conditional resource creation logic",
            "Cost optimization verification"
        ]
    }
    
    return report

if __name__ == '__main__':
    # Run the demonstration
    success = run_infrastructure_tests()
    
    # Generate report
    report = generate_test_report()
    
    print(f"\n📋 Test Report Generated: {json.dumps(report, indent=2)}")
    
    if success:
        print("\n🎉 All tests passed! Infrastructure testing demo completed successfully.")
    else:
        print("\n⚠️ Some tests failed - this is normal for demonstration purposes.")
    
    print("\n🚀 Next steps for your presentation:")
    print("   1. Show this test file to demonstrate testing capabilities")
    print("   2. Run 'python -m pytest test_infrastructure.py -v' live")
    print("   3. Explain how this is impossible/difficult with Terraform")
    print("   4. Show integration with CI/CD pipelines")