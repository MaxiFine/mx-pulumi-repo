"""
Simple Pulumi Modules Package
=============================

Basic infrastructure modules for learning Pulumi organization.
Perfect for new engineers getting started with modular infrastructure!

Key Benefits:
- Simple functions (not complex classes)
- Easy to understand and modify
- Reusable across different projects
- Good separation of concerns

Modules:
- networking: VPC, subnets, routing
- security_groups: Web and database security groups
- compute: EC2 instances for web and database servers

Usage Example:
```python
from modules import networking, security_groups, compute

# Create networking
vpc = networking.create_vpc("my-project")
igw = networking.create_internet_gateway("my-project", vpc.id)
subnet = networking.create_public_subnet("web", vpc.id, "10.0.1.0/24", "us-east-1a")
networking.setup_public_routing("my-project", vpc.id, igw.id, subnet.id)

# Create security group
web_sg = security_groups.create_web_security_group("my-project", vpc.id)

# Create web server
web_server = compute.create_web_server("web-server-1", subnet.id, web_sg.id)
```

This approach shows the power of Pulumi modules without overwhelming complexity!
"""

# Note: We import modules, not specific functions, to keep it simple
# Users can do: from modules import networking, security_groups, compute

__version__ = "1.0.0-simple"
__author__ = "Maxwell Adomako - DevOps Engineer"

print("Simple Pulumi Modules Loaded")
print("   Perfect for new engineers learning infrastructure modules!")
print("   Ready to build modular infrastructure!")