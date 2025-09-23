"""
CORE CONCEPT 2: RESOURCES - Cloud infrastructure components  
=========================================================

This demo shows different types of Pulumi resources and their relationships.

Resource Types Demonstrated:
- Physical Resources (VPC, EC2, S3)
- Logical Resources (Security Groups, Route Tables)
- Data Sources (AMI lookup, AZ lookup)
- Custom Resources (ComponentResources)

Demo Flow:
1. Show resource creation with dependencies
2. Show resource properties and outputs
3. Show resource relationships and dependencies
"""

import pulumi
import pulumi_aws as aws

print("🏗️ RESOURCES DEMO: Understanding Pulumi Resource Types")
print("=" * 60)

# =======================
# DATA SOURCES (Read-only resources)
# =======================
print("📖 1. DATA SOURCES - Reading existing cloud resources")

# Data source: Get available AZs
azs = aws.get_availability_zones(state="available")
print(f"   Found {len(azs.names)} availability zones")

# Data source: Get latest AMI
ami_data = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
)
print(f"   Latest AMI: {ami_data.id}")

# Data source: Get current AWS account info
caller_identity = aws.get_caller_identity()
print(f"   AWS Account: {caller_identity.account_id}")

# =======================  
# PHYSICAL RESOURCES (Create real AWS resources)
# =======================
print("\n🏗️ 2. PHYSICAL RESOURCES - Creating real cloud infrastructure")

# Resource 1: VPC (Virtual Private Cloud)
vpc = aws.ec2.Vpc(
    "resources-demo-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "resources-demo-vpc",
        "ResourceType": "Physical",
        "Demo": "Resources"
    }
)
print("   ✅ VPC resource defined")

# Resource 2: Internet Gateway  
igw = aws.ec2.InternetGateway(
    "resources-demo-igw",
    vpc_id=vpc.id,  # 🔗 DEPENDENCY: IGW depends on VPC
    tags={"Name": "resources-demo-igw", "ResourceType": "Physical"}
)
print("   ✅ Internet Gateway resource defined (depends on VPC)")

# Resource 3: Subnets in different AZs
subnets = []
for i, az in enumerate(azs.names[:2]):  # Create 2 subnets
    subnet = aws.ec2.Subnet(
        f"resources-demo-subnet-{i+1}",
        vpc_id=vpc.id,  # 🔗 DEPENDENCY: Subnet depends on VPC
        cidr_block=f"10.0.{i+1}.0/24",
        availability_zone=az,
        map_public_ip_on_launch=True,
        tags={
            "Name": f"resources-demo-subnet-{i+1}",
            "ResourceType": "Physical",
            "AZ": az
        }
    )
    subnets.append(subnet)
print(f"   ✅ {len(subnets)} Subnet resources defined")

# Resource 4: S3 Bucket
s3_bucket = aws.s3.Bucket(
    "resources-demo-bucket",
    tags={
        "Name": "resources-demo-bucket",
        "ResourceType": "Physical",
        "Purpose": "Demo"
    }
)
print("   ✅ S3 Bucket resource defined")

# =======================
# LOGICAL RESOURCES (AWS constructs)
# =======================
print("\n🔧 3. LOGICAL RESOURCES - AWS logical constructs")

# Logical Resource 1: Security Group
security_group = aws.ec2.SecurityGroup(
    "resources-demo-sg",
    name="resources-demo-sg",
    description="Security group for resources demo",
    vpc_id=vpc.id,  # 🔗 DEPENDENCY: SG depends on VPC
    ingress=[
        {
            "description": "HTTP",
            "from_port": 80,
            "to_port": 80,
            "protocol": "tcp",
            "cidr_blocks": ["0.0.0.0/0"]
        },
        {
            "description": "SSH", 
            "from_port": 22,
            "to_port": 22,
            "protocol": "tcp",
            "cidr_blocks": ["10.0.0.0/16"]  # Only from VPC
        }
    ],
    egress=[{
        "from_port": 0,
        "to_port": 0,
        "protocol": "-1",
        "cidr_blocks": ["0.0.0.0/0"]
    }],
    tags={
        "Name": "resources-demo-sg",
        "ResourceType": "Logical"
    }
)
print("   ✅ Security Group logical resource defined")

# Logical Resource 2: Route Table
route_table = aws.ec2.RouteTable(
    "resources-demo-rt",
    vpc_id=vpc.id,  # 🔗 DEPENDENCY: RT depends on VPC
    routes=[
        {
            "cidr_block": "0.0.0.0/0",
            "gateway_id": igw.id  # 🔗 DEPENDENCY: Route depends on IGW
        }
    ],
    tags={
        "Name": "resources-demo-rt", 
        "ResourceType": "Logical"
    }
)
print("   ✅ Route Table logical resource defined")

# Logical Resource 3: Route Table Associations
rt_associations = []
for i, subnet in enumerate(subnets):
    assoc = aws.ec2.RouteTableAssociation(
        f"resources-demo-rt-assoc-{i+1}",
        subnet_id=subnet.id,       # 🔗 DEPENDENCY: depends on subnet
        route_table_id=route_table.id  # 🔗 DEPENDENCY: depends on route table
    )
    rt_associations.append(assoc)
print(f"   ✅ {len(rt_associations)} Route Table Association resources defined")

# =======================
# COMPUTE RESOURCES
# =======================
print("\n💻 4. COMPUTE RESOURCES - EC2 instances with all dependencies")

# Create EC2 instances in each subnet
instances = []
for i, subnet in enumerate(subnets):
    instance = aws.ec2.Instance(
        f"resources-demo-instance-{i+1}",
        instance_type="t2.micro",
        ami=ami_data.id,  # 🔗 DEPENDENCY: uses data source
        subnet_id=subnet.id,  # 🔗 DEPENDENCY: depends on subnet
        vpc_security_group_ids=[security_group.id],  # 🔗 DEPENDENCY: depends on SG
        user_data=f"""#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Resources Demo - Instance {i+1}</title></head>
<body style="font-family: Arial; margin: 40px; background: #f5f5f5;">
    <h1>🏗️ RESOURCES DEMO</h1>
    <div style="background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2>Instance {i+1} Resource Information:</h2>
        
        <h3>📊 Resource Dependencies Demonstrated:</h3>
        <div style="background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>Physical Resources Created:</h4>
            <ul>
                <li>✅ VPC (10.0.0.0/16)</li>
                <li>✅ Internet Gateway</li>
                <li>✅ Subnets in multiple AZs</li>
                <li>✅ EC2 Instances</li>
                <li>✅ S3 Bucket</li>
            </ul>
        </div>
        
        <div style="background: #fff2e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>Logical Resources Created:</h4>
            <ul>
                <li>✅ Security Groups with rules</li>
                <li>✅ Route Tables with routes</li> 
                <li>✅ Route Table Associations</li>
            </ul>
        </div>
        
        <div style="background: #e8f8e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h4>Data Sources Used:</h4>
            <ul>
                <li>📖 Latest Amazon Linux AMI</li>
                <li>📖 Available Availability Zones</li>
                <li>📖 AWS Account Information</li>
            </ul>
        </div>
        
        <h3>🔗 Resource Dependency Chain:</h3>
        <p><code>VPC → IGW → Subnets → Route Table → Associations → Security Group → EC2 Instance</code></p>
        
        <p><strong>This shows how Pulumi automatically handles resource dependencies!</strong></p>
    </div>
</body>
</html>
EOF
""",
        tags={
            "Name": f"resources-demo-instance-{i+1}",
            "ResourceType": "Compute",
            "SubnetNumber": str(i+1),
            "Demo": "Resources"
        }
    )
    instances.append(instance)

print(f"   ✅ {len(instances)} EC2 Instance resources defined")

# =======================
# OUTPUTS - Show resource properties
# =======================
print("\n📤 5. RESOURCE OUTPUTS - Extracting resource properties")

# Export resource information to demonstrate different resource types
pulumi.export("demo_type", "Resources Demo")

# Data Source outputs
pulumi.export("data_sources", {
    "availability_zones": azs.names,
    "ami_id": ami_data.id,
    "ami_description": ami_data.description,
    "account_id": caller_identity.account_id,
    "region": aws.get_region().name
})

# Physical Resource outputs  
pulumi.export("physical_resources", {
    "vpc_id": vpc.id,
    "vpc_cidr": "10.0.0.0/16", 
    "igw_id": igw.id,
    "subnet_ids": [subnet.id for subnet in subnets],
    "s3_bucket_name": s3_bucket.id
})

# Logical Resource outputs
pulumi.export("logical_resources", {
    "security_group_id": security_group.id,
    "route_table_id": route_table.id,
    "route_table_associations": len(rt_associations)
})

# Compute Resource outputs
pulumi.export("compute_resources", {
    "instance_ids": [instance.id for instance in instances],
    "instance_public_ips": [instance.public_ip for instance in instances],
    "instance_urls": [instance.public_ip.apply(lambda ip: f"http://{ip}") for instance in instances]
})

# Resource dependency demonstration
pulumi.export("dependency_demo", {
    "explanation": "Notice how resources depend on each other",
    "dependency_chain": [
        "1. VPC created first",
        "2. IGW attached to VPC", 
        "3. Subnets created in VPC",
        "4. Route Table created for VPC",
        "5. Route Table associated with Subnets",
        "6. Security Group created for VPC",
        "7. EC2 Instances launched in Subnets with Security Group"
    ]
})

print("\n✅ RESOURCES DEMO complete!")
print("🔍 Run 'pulumi stack output' to see all resource information")
print("🌐 Check the instance URLs to see the resource demo page")
print("📊 Notice how Pulumi handled all the resource dependencies automatically!")