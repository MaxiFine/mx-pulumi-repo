"""
CORE CONCEPT 1: STACKS - Environment-specific deployments
========================================================

This demo shows how Pulumi uses stacks to manage multiple environments
with the same infrastructure code but different configurations.

Demo Flow:
1. Run: pulumi stack init dev
2. Run: pulumi stack init staging  
3. Run: pulumi stack init prod
4. Switch between stacks and deploy different configurations
"""

import pulumi
import pulumi_aws as aws

# Get current stack name - this is KEY for environment-specific behavior
stack_name = pulumi.get_stack()

print(f"🏗️  Deploying to STACK: {stack_name}")

# Stack-specific configurations
# Different configurations based on stack name
stack_configs = {
    "dev": {
        "instance_type": "t2.micro",
        "instance_count": 1,
        "environment": "development",
        "enable_monitoring": False
    },
    "staging": {
        "instance_type": "t3.small", 
        "instance_count": 2,
        "environment": "staging",
        "enable_monitoring": True
    },
    "prod": {
        "instance_type": "t3.medium",
        "instance_count": 3, 
        "environment": "production",
        "enable_monitoring": True
    }
}

# Get configuration for current stack (defaults to dev if not found)
config = stack_configs.get(stack_name, stack_configs["dev"])

print(f"📋 Configuration for {stack_name}:")
print(f"   - Instance Type: {config['instance_type']}")
print(f"   - Instance Count: {config['instance_count']}")
print(f"   - Environment: {config['environment']}")
print(f"   - Monitoring: {config['enable_monitoring']}")

# Get latest AMI
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
)

# Create VPC with stack-specific naming
vpc = aws.ec2.Vpc(
    f"{stack_name}-vpc",
    cidr_block="10.0.0.0/16", 
    enable_dns_hostnames=True,
    tags={
        "Name": f"{stack_name}-vpc",
        "Environment": config["environment"],
        "Stack": stack_name,
        "ManagedBy": "Pulumi-Stacks-Demo"
    }
)

# Internet Gateway
igw = aws.ec2.InternetGateway(
    f"{stack_name}-igw",
    vpc_id=vpc.id,
    tags={"Name": f"{stack_name}-igw", "Stack": stack_name}
)

# Subnet 
subnet = aws.ec2.Subnet(
    f"{stack_name}-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone=aws.get_availability_zones().names[0],
    map_public_ip_on_launch=True,
    tags={"Name": f"{stack_name}-subnet", "Stack": stack_name}
)

# Route Table
route_table = aws.ec2.RouteTable(
    f"{stack_name}-rt",
    vpc_id=vpc.id,
    routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    tags={"Name": f"{stack_name}-rt", "Stack": stack_name}
)

# Associate route table
aws.ec2.RouteTableAssociation(
    f"{stack_name}-rt-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# Security Group with stack-specific rules
security_group = aws.ec2.SecurityGroup(
    f"{stack_name}-sg",
    description=f"Security group for {stack_name} environment",
    vpc_id=vpc.id,
    ingress=[
        {"from_port": 80, "to_port": 80, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]},
        {"from_port": 22, "to_port": 22, "protocol": "tcp", "cidr_blocks": ["0.0.0.0/0"]}
    ],
    tags={"Name": f"{stack_name}-sg", "Stack": stack_name}
)

# Create multiple instances based on stack configuration
instances = []
for i in range(config["instance_count"]):
    instance = aws.ec2.Instance(
        f"{stack_name}-instance-{i+1}",
        instance_type=config["instance_type"],
        ami=ami.id,
        subnet_id=subnet.id,
        vpc_security_group_ids=[security_group.id],
        user_data=f"""#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

cat > /var/www/html/index.html << EOF
<!DOCTYPE html>
<html>
<head><title>Stack Demo - {stack_name.upper()}</title></head>
<body style="font-family: Arial; margin: 40px; background: #f0f8ff;">
    <h1>🏗️ STACK DEMO: {stack_name.upper()}</h1>
    <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2>Current Stack Configuration:</h2>
        <ul>
            <li><strong>Stack Name:</strong> {stack_name}</li>
            <li><strong>Environment:</strong> {config['environment']}</li>
            <li><strong>Instance Type:</strong> {config['instance_type']}</li>
            <li><strong>Instance Count:</strong> {config['instance_count']}</li>
            <li><strong>Instance Number:</strong> {i+1}</li>
            <li><strong>Monitoring Enabled:</strong> {config['enable_monitoring']}</li>
        </ul>
        
        <h3>Stack Concept Demonstration:</h3>
        <p>✅ Same code, different configurations per stack</p>
        <p>✅ Environment isolation through stacks</p>
        <p>✅ Independent state management</p>
        <p>✅ Easy environment promotion workflow</p>
        
        <p><em>This instance was deployed using Pulumi Stacks!</em></p>
    </div>
</body>
</html>
EOF
""",
        tags={
            "Name": f"{stack_name}-instance-{i+1}",
            "Environment": config["environment"], 
            "Stack": stack_name,
            "InstanceNumber": str(i+1)
        }
    )
    instances.append(instance)

# Export stack-specific outputs
pulumi.export("stack_name", stack_name)
pulumi.export("environment", config["environment"])
pulumi.export("instance_count", config["instance_count"])
pulumi.export("instance_type", config["instance_type"])

# Export instance URLs
pulumi.export("instance_urls", [
    instance.public_ip.apply(lambda ip: f"http://{ip}") 
    for instance in instances
])

# Export SSH commands for each instance
pulumi.export("ssh_commands", [
    instance.public_ip.apply(lambda ip: f"ssh -i your-key.pem ec2-user@{ip}")
    for instance in instances
])

print(f"✅ {stack_name.upper()} stack configuration deployed!")
print("🚀 Run 'pulumi stack output' to see all outputs")
print("🔄 Try switching stacks: pulumi stack select <stack-name>")