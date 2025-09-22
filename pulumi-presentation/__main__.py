import pulumi
import pulumi_aws as aws

# Demo: Enhanced Infrastructure as Code with Pulumi
print("🚀 Deploying Enhanced Pulumi Demo Infrastructure...")

# Get dynamic AZs - Show Pulumi's dynamic capabilities
availability_zones = aws.get_availability_zones(state='available')
selected_az = availability_zones.names[0]

# Get AMI's dynamically - Better than hardcoding AMI IDs
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
        'Environment': 'presentation',
        'owner': 'mx-devops',
        'ManagedBy': 'Pulumi'
    }
)

# Pulumi Subnet Components
public_subnet = aws.ec2.Subnet('public-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    availability_zone=selected_az,  # dynamic az's implementation
    map_public_ip_on_launch=True,  # Added for demo
    tags = {
        'Name': 'Public|Subnet',
        'Environment': 'presentation',
        'owner': 'mx-devops'
    }
)

# Pulumi Internet gateway
igw = aws.ec2.InternetGateway('igw',
    vpc_id=vpc.id,
    tags = {
        'Name': 'igw',
        'Environment': 'presentation',
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
        'Environment': 'presentation',
        'owner': 'mx-devops'
    }
)

# Route Table Association
public_route_table_association = aws.ec2.RouteTableAssociation(
    'public-route-table-association',
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id,
)

# Enhanced Security Group for Demo
security_group = aws.ec2.SecurityGroup(
    'public-security-group',
    description='Enable HTTP, HTTPS and SSH access for demo',
    vpc_id=vpc.id,
    ingress=[
        {
            'from_port': 80,
            'to_port': 80,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0'],
            'description': 'HTTP access'
        },
        {
            'from_port': 443,
            'to_port': 443,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0'],
            'description': 'HTTPS access'
        },
        {
            'from_port': 22,
            'to_port': 22,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0'],  # Restrict this in production
            'description': 'SSH access for demo'
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
        'Environment': 'presentation',
        'owner': 'mx-devops'
    }
)

# Enhanced user script with dynamic content for demo
user_script = """#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Create dynamic demo webpage
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pulumi Demo Server</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      color: white;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .container {
      max-width: 900px;
      width: 90%;
      background: rgba(255,255,255,0.1);
      padding: 40px;
      border-radius: 20px;
      backdrop-filter: blur(15px);
      box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
      border: 1px solid rgba(255,255,255,0.2);
    }
    h1 {
      font-size: 3rem;
      text-align: center;
      margin-bottom: 2rem;
      text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
      background: linear-gradient(45deg, #FFD700, #FFA500);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 25px;
      margin: 2rem 0;
    }
    .info-card {
      background: rgba(255,255,255,0.15);
      padding: 25px;
      border-radius: 15px;
      border: 1px solid rgba(255,255,255,0.2);
      transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .info-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    }
    .info-card h3 {
      color: #FFD700;
      margin-bottom: 15px;
      font-size: 1.3rem;
    }
    .highlight {
      color: #FFD700;
      font-weight: bold;
    }
    .status-banner {
      text-align: center;
      font-size: 1.3rem;
      margin-top: 2rem;
      padding: 20px;
      background: linear-gradient(45deg, rgba(0,255,0,0.2), rgba(0,200,0,0.3));
      border-radius: 10px;
      border: 2px solid rgba(0,255,0,0.4);
    }
    .demo-features {
      list-style: none;
      padding: 0;
    }
    .demo-features li {
      padding: 8px 0;
      border-bottom: 1px solid rgba(255,255,255,0.1);
    }
    .demo-features li:last-child {
      border-bottom: none;
    }
    .tech-stack {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-top: 15px;
    }
    .tech-badge {
      background: rgba(255,215,0,0.2);
      padding: 5px 12px;
      border-radius: 20px;
      font-size: 0.85rem;
      border: 1px solid rgba(255,215,0,0.3);
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🚀 Pulumi Demo Server</h1>
    
    <div class="info-grid">
      <div class="info-card">
        <h3>🖥️ Server Information</h3>
        <p><span class="highlight">Hostname:</span> $(hostname)</p>
        <p><span class="highlight">Instance ID:</span> $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>
        <p><span class="highlight">Instance Type:</span> $(curl -s http://169.254.169.254/latest/meta-data/instance-type)</p>
        <p><span class="highlight">AMI ID:</span> $(curl -s http://169.254.169.254/latest/meta-data/ami-id)</p>
      </div>
      
      <div class="info-card">
        <h3>🌐 Network Details</h3>
        <p><span class="highlight">Private IP:</span> $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)</p>
        <p><span class="highlight">Public IP:</span> $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)</p>
        <p><span class="highlight">Availability Zone:</span> $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)</p>
        <p><span class="highlight">Region:</span> $(curl -s http://169.254.169.254/latest/meta-data/placement/region)</p>
      </div>
      
      <div class="info-card">
        <h3>🚀 Deployment Info</h3>
        <p><span class="highlight">Deployed At:</span> $(date)</p>
        <p><span class="highlight">Managed By:</span> Pulumi IaC</p>
        <p><span class="highlight">Environment:</span> Presentation Demo</p>
        <p><span class="highlight">VPC:</span> Custom VPC (10.0.0.0/16)</p>
      </div>
      
      <div class="info-card">
        <h3>✅ Infrastructure Features</h3>
        <ul class="demo-features">
          <li>🏗️ Custom VPC with public subnet</li>
          <li>🌐 Internet Gateway & Route Tables</li>
          <li>🔒 Security Groups (HTTP, HTTPS, SSH)</li>
          <li>🖥️ EC2 Instance with web server</li>
          <li>🎯 Dynamic AMI selection</li>
          <li>📍 Auto AZ selection</li>
        </ul>
      </div>
      
      <div class="info-card">
        <h3>🛠️ Technology Stack</h3>
        <div class="tech-stack">
          <span class="tech-badge">Pulumi</span>
          <span class="tech-badge">Python</span>
          <span class="tech-badge">AWS</span>
          <span class="tech-badge">EC2</span>
          <span class="tech-badge">VPC</span>
          <span class="tech-badge">Apache HTTP</span>
        </div>
      </div>
      
      <div class="info-card">
        <h3>💡 Pulumi Advantages</h3>
        <ul class="demo-features">
          <li>🐍 Real programming languages</li>
          <li>🔄 Dynamic resource configuration</li>
          <li>🧪 Unit testable infrastructure</li>
          <li>📦 Reusable components</li>
          <li>🎯 IDE support & debugging</li>
        </ul>
      </div>
    </div>
    
    <div class="status-banner">
      <strong>🎉 Infrastructure Successfully Deployed!</strong><br>
      <em>Powered by Pulumi Infrastructure as Code</em>
    </div>
  </div>
</body>
</html>
EOF

# Set proper permissions
chown apache:apache /var/www/html/index.html
"""

# EC2 Instance with enhanced configuration
ec2_instance = aws.ec2.Instance(
    'webserver-instance',
    instance_type='t3.micro',
    ami=dynamic_ami.id,
    key_name='aws-365-keypair',  # Make sure this key pair exists
    user_data=user_script,
    security_groups=[security_group.id],
    subnet_id=public_subnet.id,
    associate_public_ip_address=True,
    tags = {
        'Name': 'Pulumi|Demo|Instance',
        'Environment': 'presentation',
        'owner': 'mx-devops',
        'ManagedBy': 'Pulumi',
        'Purpose': 'Demo'
    }
)

# Enhanced exports for demo purposes
pulumi.export('instance_ip', ec2_instance.public_ip)
pulumi.export('website_url', ec2_instance.public_ip.apply(lambda ip: f"http://{ip}"))
pulumi.export('ssh_command', ec2_instance.public_ip.apply(lambda ip: f"ssh -i aws-365-keypair.pem ec2-user@{ip}"))

# Infrastructure details for demo
pulumi.export('infrastructure_details', {
    'vpc_id': vpc.id,
    'vpc_cidr': '10.0.0.0/16',
    'subnet_id': public_subnet.id,
    'subnet_cidr': '10.0.1.0/24',
    'security_group_id': security_group.id,
    'route_table_id': public_route_table.id,
    'igw_id': igw.id,
    'availability_zone': selected_az
})

# Demo metadata
pulumi.export('demo_info', {
    'ami_id': dynamic_ami.id,
    'region': aws.get_region().name,
    'account_id': aws.get_caller_identity().account_id,
    'deployment_time': pulumi.Output.concat("Deployed at: ", str(pulumi.runtime.get_time())),
    'pulumi_version': '3.x',
    'language': 'Python'
})

# Quick access commands for demo
pulumi.export('quick_commands', {
    'test_website': ec2_instance.public_ip.apply(lambda ip: f"curl http://{ip}"),
    'ssh_access': ec2_instance.public_ip.apply(lambda ip: f"ssh -i aws-365-keypair.pem ec2-user@{ip}"),
    'check_status': ec2_instance.public_ip.apply(lambda ip: f"curl -I http://{ip}"),
    'view_logs': "sudo tail -f /var/log/httpd/access_log"
})

print("✅ Enhanced Pulumi demo infrastructure defined successfully!")
print("Run 'pulumi up' to deploy and 'pulumi stack output' to see results.")