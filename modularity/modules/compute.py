"""
Simple Compute Module
=====================

Basic EC2 instance functions for web servers and databases.
Simple and easy to understand!
"""

import pulumi_aws as aws


def get_latest_ami():
    """
    Get the latest Amazon Linux 2 AMI.
    
    Returns:
        AMI data
    """
    return aws.ec2.get_ami(
        most_recent=True,
        owners=["amazon"],
        filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
    )


def create_web_server(name: str, subnet_id, security_group_id, key_name: str = None):
    """
    Create a simple web server with Apache installed.
    
    Args:
        name: Name for the server
        subnet_id: Subnet ID to launch in
        security_group_id: Security group ID
        key_name: Optional EC2 key pair name
    
    Returns:
        EC2 instance
    """
    # Get latest AMI
    ami = get_latest_ami()
    
    # User data script to install Apache
    user_data = f"""#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

# Create simple webpage
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Simple Modular Demo - {name}</title>
    <style>
        body {{ 
            font-family: Arial; 
            text-align: center; 
            margin: 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 40px;
            border-radius: 20px;
        }}
        .highlight {{ color: #FFD700; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Modular Pulumi Demo</h1>
        <h2 class="highlight">Server: {name}</h2>
        
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 class="highlight">Created with Simple Modules:</h3>
            <p>✅ Networking module - VPC, subnets, routing</p>
            <p>✅ Security Groups module - Web server security</p>
            <p>✅ Compute module - This web server!</p>
        </div>
        
        <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin: 20px 0;">
            <h3 class="highlight">Why Pulumi Modules?</h3>
            <p>📦 <strong>Reusable</strong> - Same code, different environments</p>
            <p>🔧 <strong>Simple</strong> - Easy functions, not complex classes</p>
            <p>🐍 <strong>Python</strong> - Real programming language benefits</p>
            <p>🎯 <strong>Organized</strong> - Separate concerns into modules</p>
        </div>
        
        <p style="margin-top: 30px;">
            <strong>Infrastructure as Code made simple! 🎉</strong>
        </p>
    </div>
</body>
</html>
EOF

# Set proper permissions
chown apache:apache /var/www/html/index.html
"""
    
    # Create EC2 instance
    instance = aws.ec2.Instance(
        f"{name}-instance",
        instance_type="t2.micro",
        ami=ami.id,
        subnet_id=subnet_id,
        vpc_security_group_ids=[security_group_id],
        key_name=key_name,
        user_data=user_data,
        tags={
            "Name": name,
            "Type": "WebServer"
        }
    )
    
    print(f"✅ Web server created: {name}")
    print(f"   Instance type: t2.micro")
    print(f"   AMI: {ami.id}")
    return instance


def create_database_server(name: str, subnet_id, security_group_id, key_name: str = None):
    """
    Create a simple database server with MySQL.
    
    Args:
        name: Name for the server
        subnet_id: Subnet ID to launch in (usually private)
        security_group_id: Security group ID
        key_name: Optional EC2 key pair name
    
    Returns:
        EC2 instance
    """
    # Get latest AMI
    ami = get_latest_ami()
    
    # User data script to install MySQL
    user_data = f"""#!/bin/bash
yum update -y
yum install -y mysql-server
systemctl start mysqld
systemctl enable mysqld

# Create demo database
mysql -e "CREATE DATABASE IF NOT EXISTS demo_app;"
mysql -e "CREATE TABLE IF NOT EXISTS demo_app.users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50));"
mysql -e "INSERT INTO demo_app.users (name) VALUES ('Demo User from {name}');"

echo "Database setup completed on {name}" > /var/log/db-setup.log
"""
    
    # Create EC2 instance
    instance = aws.ec2.Instance(
        f"{name}-instance",
        instance_type="t2.micro",
        ami=ami.id,
        subnet_id=subnet_id,
        vpc_security_group_ids=[security_group_id],
        key_name=key_name,
        user_data=user_data,
        tags={
            "Name": name,
            "Type": "Database"
        }
    )
    
    print(f"✅ Database server created: {name}")
    print(f"   Instance type: t2.micro")
    print(f"   MySQL will be installed automatically")
    return instance


def create_multiple_instances(base_name: str, count: int, subnet_ids: list, security_group_id, key_name: str = None):
    """
    Create multiple web server instances across subnets.
    
    Args:
        base_name: Base name for instances (will add -1, -2, etc.)
        count: Number of instances to create
        subnet_ids: List of subnet IDs to distribute instances
        security_group_id: Security group ID
        key_name: Optional EC2 key pair name
    
    Returns:
        List of EC2 instances
    """
    instances = []
    
    for i in range(count):
        # Use different subnets for distribution
        subnet_id = subnet_ids[i % len(subnet_ids)]
        instance_name = f"{base_name}-{i+1}"
        
        instance = create_web_server(
            name=instance_name,
            subnet_id=subnet_id,
            security_group_id=security_group_id,
            key_name=key_name
        )
        
        instances.append(instance)
    
    print(f"✅ Created {count} instances with base name: {base_name}")
    return instances