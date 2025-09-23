import pulumi
import pulumi_aws as aws

# Simple Demo: Basic Infrastructure as Code with Pulumi
print("Deploying Pulumi Demo Infrastructure...")

# Get dynamic AZs
availability_zones = aws.get_availability_zones(state='available')
selected_az = availability_zones.names[0]

# Get AMI dynamically
dynamic_ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {
            "name": "name", 
            "values": ["amzn2-ami-hvm-*"]
        }
    ]
)

# Create VPC
vpc = aws.ec2.Vpc(
    'presentation-vpc',
    cidr_block='10.0.0.0/16',
    enable_dns_hostnames=True,
    tags={
        'Name': 'presentation-vpc',
        'Environment': 'demo'
    }
)

# Internet Gateway
igw = aws.ec2.InternetGateway(
    'presentation-igw',
    vpc_id=vpc.id,
    tags={'Name': 'presentation-igw'}
)

# Public Subnet
public_subnet = aws.ec2.Subnet(
    'public-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    availability_zone=selected_az,
    map_public_ip_on_launch=True,
    tags={
        'Name': 'public-subnet',
        'Environment': 'demo'
    }
)

# Route Table
public_route_table = aws.ec2.RouteTable(
    'public-route-table',
    vpc_id=vpc.id,
    routes=[
        {
            'cidr_block': '0.0.0.0/0',
            'gateway_id': igw.id
        }
    ],
    tags={
        'Name': 'public-route-table',
        'Environment': 'demo'
    }
)

# Route Table Association
public_route_table_association = aws.ec2.RouteTableAssociation(
    'public-route-table-association',
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id,
)

# Security Group
security_group = aws.ec2.SecurityGroup(
    'demo-security-group',
    description='Enable HTTP and SSH access',
    vpc_id=vpc.id,
    ingress=[
        {
            'from_port': 80,
            'to_port': 80,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0']
        },
        {
            'from_port': 22,
            'to_port': 22,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0']
        }
    ],
    tags={
        'Name': 'demo-security-group',
        'Environment': 'demo'
    }
)

# User Data Script (simple)
user_data_script = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Simple HTML page
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Pulumi Demo Server</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { color: #8A2BE2; }
        .info { background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pulumi Demo Server</h1>
        <div class="info">
            <h3>Infrastructure Status: DEPLOYED</h3>
            <p>This server was created using Pulumi Infrastructure as Code!</p>
            <ul>
                <li>VPC with custom CIDR</li>
                <li>Public subnet with Internet Gateway</li>
                <li>Security group with HTTP/SSH access</li>
                <li>EC2 instance with dynamic AMI</li>
                <li>Auto-configured web server</li>
            </ul>
        </div>
        <div class="info">
            <h3>Pulumi Benefits</h3>
            <ul>
                <li>Real programming languages (Python, TypeScript, Go)</li>
                <li>IDE support and debugging</li>
                <li>Strong type safety</li>
                <li>Reusable components</li>
                <li>Multi-cloud support</li>
            </ul>
        </div>
        <p><strong>Demo completed successfully!</strong></p>
    </div>
</body>
</html>
EOF
"""

# EC2 Instance
instance = aws.ec2.Instance(
    'demo-instance',
    instance_type='t2.micro',
    ami=dynamic_ami.id,
    subnet_id=public_subnet.id,
    vpc_security_group_ids=[security_group.id],
    user_data=user_data_script,
    tags={
        'Name': 'pulumi-demo-instance',
        'Environment': 'demo'
    }
)

# Outputs
pulumi.export('instance_id', instance.id)
pulumi.export('public_ip', instance.public_ip)
pulumi.export('public_dns', instance.public_dns)
pulumi.export('website_url', instance.public_ip.apply(lambda ip: f"http://{ip}"))
pulumi.export('ssh_command', instance.public_ip.apply(lambda ip: f"ssh -i your-key.pem ec2-user@{ip}"))

print("Deployment complete! Check the outputs for connection details.")