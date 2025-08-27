import pulumi
import pulumi_aws as aws
# from pulumi import export

# Get dynamic AZs
availability_zones = aws.get_availability_zones(state='available')
selected_az = availability_zones.names[0]

# Get AMI's dynamically
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

# Pulumi VPC Components
vpc = aws.ec2.Vpc('mx-pulumi-vpc',
    cidr_block='10.0.0.0/16',
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={
        'Name': 'mx-pulumi-vpc',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Pulumi Subnet Components
public_subnet = aws.ec2.Subnet('public-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    # availability_zone='us-east-1a',
    availability_zone=selected_az,  # dynamic az's implementation
    tags = {
        'Name': 'Public|Subnet',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
    )

# Pulumi Internet gateway
igw = aws.ec2.InternetGateway('igw',
    vpc_id=vpc.id,
    tags = {
        'Name': 'igw',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Pulumi Route Table
public_route_table = aws.ec2.RouteTable('public-route-table',
    vpc_id=vpc.id,
    routes=[
        {
            'cidr_block': '0.0.0.0/0',
            'gateway_id': igw.id
        }
    ],
    tags={
        'Name': 'Public|Route|Table',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Route Table Association
public_route_table_association = aws.ec2.RouteTableAssociation(
    'public-route-table-association',
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id,
    # internet_gateway_id=igw.id,
    tags = {
        'Name': 'public-route-table-association',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Pulumi Security Group
security_group = aws.ec2.SecurityGroup(
    'public-security-group',
    description='Enable HTTP access',
    vpc_id=vpc.id,
    ingress=[
        {
            'from_port': 80,
            'to_port': 80,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0']
        }
    ],
    egress=[
        {
            'from_port': 0,
            'to_port': 0,
            'protocol': '-1',
            'cidr_blocks': ['0.0.0.0/0']
        }
    ],
    tags={
        'Name': 'Public|Security|Group',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Pulumi EC2 Instance
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {
            "name": "name",
            # "values": ["amzn2-ami-hvm-*-x86_64-gp2"]
            "values": ["amzn2-ami-hvm-*"]
        }
    ]
)

user_data = """#!/bin/bash
sudo apt-get update
sudo apt-get install nginx -y
sudo systemctl enable nginx
sudo systemctl start nginx
cat <<EOF | sudo tee /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to My Website</title>
  <style>
    body {
      font-family: 'Arial', sans-serif;
      background-color: #f4f4f9;
      color: #333;
      margin: 0;
      padding: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      text-align: center;
    }
    .container {
      background: white;
      padding: 2rem;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    h1 {
      font-size: 2.5rem;
      margin-bottom: 1rem;
      color: #2c3e50;
    }
    p {
      font-size: 1.2rem;
      margin-bottom: 2rem;
    }
    a {
      text-decoration: none;
      color: white;
      background-color: #3498db;
      padding: 0.8rem 1.5rem;
      border-radius: 5px;
      transition: background-color 0.3s ease;
    }
    a:hover {
      background-color: #2980b9;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome to My Website</h1>
    <p>This is the homepage of my awesome website. Feel free to explore!</p>
    <a href="#">Get Started</a>
  </div>
</body>
</html>
EOF
sudo ufw allow 'Nginx HTTP'
sudo ufw allow 'Nginx HTTPS'
echo "Nginx installed successfully! You can access your server at http://$(curl -s ifconfig.me)"
"""

ec2_instance = aws.ec2.Instance(
    'webserver-instance',
    instance_type='t2.micro',
    # vpc_security_group_ids=[security_group.id],
    ami=ami.id,
    user_data=user_data,
    security_group_ids=[security_group.id],
    subnet_id=public_subnet.id,
    associate_public_ip_address=True,
    # public_route_table_association=public_route_table_association.id
    tags = {
        'Name': 'Public|Instance',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

pulumi.export('instance_ip', ec2_instance.public_ip)
pulumi.export('security_group_id', security_group.id)
pulumi.export('vpc_id', vpc.id)
pulumi.export('subnet_id', public_subnet.id)
pulumi.export('route_table_id', public_route_table.id)
pulumi.export('igw_id', igw.id)
pulumi.export('instance_ami', ami.id)
