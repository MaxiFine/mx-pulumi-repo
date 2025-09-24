"""
Simple Modular Infrastructure Demo
==================================

This shows how to organize Pulumi code into simple, reusable modules.
Perfect for new engineers to understand Infrastructure as Code organization!

🎯 KEY LESSON: Break your infrastructure into logical pieces!
"""

import pulumi
from modules import networking, security_groups, compute

# Get current stack name
stack_name = pulumi.get_stack()
print(f"\n🚀 SIMPLE MODULAR DEMO - Stack: {stack_name}")
print("=" * 50)

# Project name for consistent naming
project_name = f"simple-demo-{stack_name}"

# 1. CREATE NETWORKING (VPC, Subnets, Internet Access)
print("1️⃣  Creating networking components...")

# Create VPC
vpc = networking.create_vpc(project_name, "10.0.0.0/16")

# Create Internet Gateway  
igw = networking.create_internet_gateway(project_name, vpc.id)

# Create public subnet for web servers
web_subnet = networking.create_public_subnet(
    f"{project_name}-web",
    vpc.id,
    "10.0.1.0/24",
    "us-east-1a"
)

# Create private subnet for databases (optional)
db_subnet = networking.create_private_subnet(
    f"{project_name}-db", 
    vpc.id,
    "10.0.2.0/24",
    "us-east-1a"
)

# Setup internet routing for public subnet
networking.setup_public_routing(project_name, vpc.id, igw.id, web_subnet.id)

# 2. CREATE SECURITY GROUPS
print("2️⃣  Creating security groups...")

# Web server security group (HTTP, HTTPS, SSH)
web_sg = security_groups.create_web_security_group(project_name, vpc.id)

# Database security group (MySQL from web servers only)  
db_sg = security_groups.create_database_security_group(project_name, vpc.id, web_sg.id)

# 3. CREATE COMPUTE RESOURCES
print("3️⃣  Creating compute resources...")

# Stack-specific configuration (same modules, different setups!)
if stack_name == "dev":
    print("   📋 DEV Environment: 1 web server only")
    
    # Single web server for development
    web_server = compute.create_web_server(
        f"{project_name}-web",
        web_subnet.id,
        web_sg.id
    )
    
    # Export dev outputs
    pulumi.export("web_url", web_server.public_ip.apply(lambda ip: f"http://{ip}"))
    pulumi.export("server_count", 1)

elif stack_name == "staging":
    print("   📋 STAGING Environment: 2 web servers + database")
    
    # Multiple web servers for load testing
    web_servers = compute.create_multiple_instances(
        f"{project_name}-web",
        count=2,
        subnet_ids=[web_subnet.id],  # Could add more subnets here
        security_group_id=web_sg.id
    )
    
    # Database server in private subnet
    db_server = compute.create_database_server(
        f"{project_name}-db",
        db_subnet.id,
        db_sg.id
    )
    
    # Export staging outputs
    web_urls = [server.public_ip.apply(lambda ip: f"http://{ip}") for server in web_servers]
    pulumi.export("web_urls", web_urls)
    pulumi.export("database_private_ip", db_server.private_ip)
    pulumi.export("server_count", len(web_servers))

elif stack_name == "prod":
    print("   📋 PRODUCTION Environment: 3 web servers + database")
    
    # Production setup with multiple web servers
    web_servers = compute.create_multiple_instances(
        f"{project_name}-web",
        count=3,
        subnet_ids=[web_subnet.id],
        security_group_id=web_sg.id
    )
    
    # Database server
    db_server = compute.create_database_server(
        f"{project_name}-db",
        db_subnet.id, 
        db_sg.id
    )
    
    # Export production outputs
    web_urls = [server.public_ip.apply(lambda ip: f"http://{ip}") for server in web_servers]
    pulumi.export("web_urls", web_urls)
    pulumi.export("database_private_ip", db_server.private_ip)
    pulumi.export("server_count", len(web_servers))
    
else:
    print("   📋 DEFAULT: Simple 1 web server demo")
    
    # Default: just one web server
    web_server = compute.create_web_server(
        f"{project_name}-web",
        web_subnet.id,
        web_sg.id
    )
    
    pulumi.export("web_url", web_server.public_ip.apply(lambda ip: f"http://{ip}"))
    pulumi.export("server_count", 1)

# Common exports for all stacks
pulumi.export("vpc_id", vpc.id)
pulumi.export("stack_name", stack_name)
pulumi.export("project_name", project_name)

# Module demonstration info
pulumi.export("modules_used", [
    "networking - VPC, subnets, routing", 
    "security_groups - Web and DB security",
    "compute - EC2 web and database servers"
])

print(f"✅ {stack_name.upper()} infrastructure deployed successfully!")
print("🔄 Same modules, different configurations!")
print("=" * 50)