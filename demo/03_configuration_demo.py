"""
CORE CONCEPT 3: CONFIGURATION - Secrets, parameters, and environment variables
============================================================================

This demo shows how Pulumi handles configuration management:
- Config values (pulumi config set)
- Secrets (pulumi config set --secret) 
- Environment variables
- Default values and required config
- Type conversion and validation

Setup Commands to Run First:
1. pulumi config set app_name "MyDemoApp"
2. pulumi config set instance_count 2
3. pulumi config set enable_https true  
4. pulumi config set --secret db_password "super-secret-password"
5. pulumi config set --secret api_key "secret-api-key-12345"
6. export ENVIRONMENT="demo"  (or set ENVIRONMENT=demo on Windows)

Demo Flow:
1. Show different ways to get configuration
2. Show secrets handling
3. Show default values and validation
4. Show configuration in infrastructure
"""

import pulumi
import pulumi_aws as aws
import os

print("⚙️ CONFIGURATION DEMO: Managing Parameters, Secrets & Environment Variables")
print("=" * 80)

# =======================
# CONFIGURATION SETUP
# =======================
config = pulumi.Config()

print("📋 1. READING CONFIGURATION VALUES")

# Required configuration (will fail if not set)
try:
    app_name = config.require("app_name")
    print(f"   ✅ App Name (required): {app_name}")
except pulumi.ConfigMissingError as e:
    print(f"   ❌ Missing required config: {e}")
    app_name = "DefaultApp"

# Optional configuration with defaults
instance_count = config.get_int("instance_count", 1)  # Default to 1
print(f"   ✅ Instance Count (with default): {instance_count}")

enable_https = config.get_bool("enable_https", False)  # Default to False
print(f"   ✅ Enable HTTPS (boolean): {enable_https}")

# Configuration with type conversion
allowed_cidrs = config.get("allowed_cidrs", "10.0.0.0/8,172.16.0.0/12")
cidr_list = [cidr.strip() for cidr in allowed_cidrs.split(",")]
print(f"   ✅ Allowed CIDRs (parsed): {cidr_list}")

# =======================
# SECRETS CONFIGURATION  
# =======================
print("\n🔒 2. READING SECRETS (Encrypted Configuration)")

# Required secret
try:
    db_password = config.require_secret("db_password")
    print("   ✅ Database Password (secret): *** ENCRYPTED ***")
except pulumi.ConfigMissingError:
    print("   ❌ Missing required secret: db_password")
    db_password = "default-insecure-password"

# Optional secret
api_key = config.get_secret("api_key", "default-api-key")
print("   ✅ API Key (secret): *** ENCRYPTED ***")

# =======================
# ENVIRONMENT VARIABLES
# =======================
print("\n🌍 3. READING ENVIRONMENT VARIABLES")

environment = os.environ.get("ENVIRONMENT", "development")
print(f"   ✅ Environment (from ENV): {environment}")

aws_region = os.environ.get("AWS_REGION", "us-east-1")  
print(f"   ✅ AWS Region (from ENV): {aws_region}")

# Custom environment variable
deployment_mode = os.environ.get("DEPLOYMENT_MODE", "standard")
print(f"   ✅ Deployment Mode (from ENV): {deployment_mode}")

# =======================
# CONFIGURATION VALIDATION
# =======================
print("\n✅ 4. CONFIGURATION VALIDATION")

# Validate instance count
if instance_count < 1 or instance_count > 10:
    raise ValueError(f"instance_count must be between 1 and 10, got {instance_count}")
print(f"   ✅ Instance count validation passed: {instance_count}")

# Validate environment
valid_environments = ["development", "staging", "production", "demo"]
if environment not in valid_environments:
    raise ValueError(f"Environment must be one of {valid_environments}, got {environment}")
print(f"   ✅ Environment validation passed: {environment}")

# =======================
# CONFIGURATION-DRIVEN INFRASTRUCTURE
# =======================
print("\n🏗️ 5. USING CONFIGURATION TO DRIVE INFRASTRUCTURE")

# Get AMI
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
)

# VPC with configuration-driven naming
vpc = aws.ec2.Vpc(
    f"{app_name}-{environment}-vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    tags={
        "Name": f"{app_name}-{environment}-vpc",
        "Application": app_name,
        "Environment": environment,
        "ManagedBy": "Pulumi-Config-Demo"
    }
)

# Subnets based on configuration
igw = aws.ec2.InternetGateway(
    f"{app_name}-{environment}-igw",
    vpc_id=vpc.id,
    tags={
        "Name": f"{app_name}-{environment}-igw",
        "Application": app_name,
        "Environment": environment
    }
)

subnet = aws.ec2.Subnet(
    f"{app_name}-{environment}-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    availability_zone=aws.get_availability_zones().names[0],
    map_public_ip_on_launch=True,
    tags={
        "Name": f"{app_name}-{environment}-subnet",
        "Application": app_name,
        "Environment": environment
    }
)

# Route table
route_table = aws.ec2.RouteTable(
    f"{app_name}-{environment}-rt",
    vpc_id=vpc.id,
    routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    tags={
        "Name": f"{app_name}-{environment}-rt",
        "Application": app_name,
        "Environment": environment
    }
)

aws.ec2.RouteTableAssociation(
    f"{app_name}-{environment}-rt-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# Security Group with configuration-driven rules
sg_ingress = [
    {"from_port": 22, "to_port": 22, "protocol": "tcp", "cidr_blocks": cidr_list, "description": "SSH"}
]

# Add HTTP always
sg_ingress.append({
    "from_port": 80, "to_port": 80, "protocol": "tcp", 
    "cidr_blocks": ["0.0.0.0/0"], "description": "HTTP"
})

# Add HTTPS only if configured
if enable_https:
    sg_ingress.append({
        "from_port": 443, "to_port": 443, "protocol": "tcp",
        "cidr_blocks": ["0.0.0.0/0"], "description": "HTTPS"
    })

security_group = aws.ec2.SecurityGroup(
    f"{app_name}-{environment}-sg",
    name=f"{app_name}-{environment}-sg",
    description=f"Security group for {app_name} {environment}",
    vpc_id=vpc.id,
    ingress=sg_ingress,
    egress=[{"from_port": 0, "to_port": 0, "protocol": "-1", "cidr_blocks": ["0.0.0.0/0"]}],
    tags={
        "Name": f"{app_name}-{environment}-sg",
        "Application": app_name,
        "Environment": environment
    }
)

# =======================
# CONFIGURATION-DRIVEN INSTANCES
# =======================
print(f"\n💻 6. CREATING {instance_count} INSTANCES BASED ON CONFIGURATION")

instances = []
for i in range(instance_count):
    # User data script that uses configuration and secrets
    user_data = pulumi.Output.all(db_password, api_key).apply(lambda args: f"""#!/bin/bash
yum update -y
yum install -y httpd

# Create application config file using secrets
cat > /etc/app-config.conf << 'APPCONF'
[database]
password={args[0]}

[api]
key={args[1]}
APPCONF

# Restrict access to config file
chmod 600 /etc/app-config.conf

systemctl start httpd
systemctl enable httpd

cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Configuration Demo - {app_name}</title></head>
<body style="font-family: Arial; margin: 40px; background: #f0f8ff;">
    <h1>⚙️ CONFIGURATION DEMO</h1>
    <div style="background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        <h2>Instance {i+1} - Configuration Values Used:</h2>
        
        <div style="background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>📋 Regular Configuration:</h3>
            <ul>
                <li><strong>App Name:</strong> {app_name}</li>
                <li><strong>Environment:</strong> {environment}</li>
                <li><strong>Instance Count:</strong> {instance_count}</li>
                <li><strong>HTTPS Enabled:</strong> {enable_https}</li>
                <li><strong>Allowed CIDRs:</strong> {", ".join(cidr_list)}</li>
            </ul>
        </div>
        
        <div style="background: #ffe8e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>🔒 Secrets Configuration:</h3>
            <ul>
                <li><strong>Database Password:</strong> *** ENCRYPTED IN PULUMI CONFIG ***</li>
                <li><strong>API Key:</strong> *** ENCRYPTED IN PULUMI CONFIG ***</li>
            </ul>
            <p><em>Secrets are encrypted at rest and in transit!</em></p>
        </div>
        
        <div style="background: #e8f8e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>🌍 Environment Variables:</h3>
            <ul>
                <li><strong>ENVIRONMENT:</strong> {environment}</li>
                <li><strong>AWS_REGION:</strong> {aws_region}</li>
                <li><strong>DEPLOYMENT_MODE:</strong> {deployment_mode}</li>
            </ul>
        </div>
        
        <div style="background: #fff8e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>✅ Configuration Features Demonstrated:</h3>
            <ul>
                <li>✅ Required vs Optional configuration</li>
                <li>✅ Type conversion (string, int, bool)</li>
                <li>✅ Default values</li>
                <li>✅ Configuration validation</li>
                <li>✅ Encrypted secrets management</li>
                <li>✅ Environment variable integration</li>
                <li>✅ Configuration-driven infrastructure</li>
            </ul>
        </div>
        
        <h3>🚀 How This Works:</h3>
        <ol>
            <li>Set config: <code>pulumi config set app_name "MyApp"</code></li>
            <li>Set secrets: <code>pulumi config set --secret db_password "secret"</code></li>
            <li>Set environment: <code>export ENVIRONMENT="demo"</code></li>
            <li>Deploy: <code>pulumi up</code></li>
        </ol>
        
        <p><strong>Configuration makes your infrastructure flexible and reusable!</strong></p>
    </div>
</body>
</html>
EOF
""")

    instance = aws.ec2.Instance(
        f"{app_name}-{environment}-instance-{i+1}",
        instance_type="t2.micro",
        ami=ami.id,
        subnet_id=subnet.id,
        vpc_security_group_ids=[security_group.id],
        user_data=user_data,
        tags={
            "Name": f"{app_name}-{environment}-instance-{i+1}",
            "Application": app_name,
            "Environment": environment,
            "InstanceNumber": str(i+1),
            "ConfigDemo": "true"
        }
    )
    instances.append(instance)

# =======================
# OUTPUTS WITH CONFIGURATION DATA
# =======================
print("\n📤 7. EXPORTING CONFIGURATION INFORMATION")

pulumi.export("demo_type", "Configuration Demo")

# Export configuration values (non-secrets only!)
pulumi.export("configuration_used", {
    "app_name": app_name,
    "environment": environment,
    "instance_count": instance_count,
    "enable_https": enable_https,
    "allowed_cidrs": cidr_list,
    "aws_region": aws_region,
    "deployment_mode": deployment_mode
})

# Export secrets info (but not actual values!)
pulumi.export("secrets_configured", {
    "db_password_configured": True,
    "api_key_configured": True,
    "note": "Secret values are encrypted and not shown in outputs"
})

# Export instance information
pulumi.export("instances", {
    "count": len(instances),
    "instance_ids": [instance.id for instance in instances],
    "public_ips": [instance.public_ip for instance in instances],
    "urls": [instance.public_ip.apply(lambda ip: f"http://{ip}") for instance in instances]
})

# Configuration commands for demo
pulumi.export("demo_commands", {
    "view_config": "pulumi config",
    "set_regular_config": "pulumi config set app_name 'MyNewApp'",
    "set_secret_config": "pulumi config set --secret db_password 'new-secret'",
    "remove_config": "pulumi config rm app_name",
    "copy_config": "pulumi config cp <source-stack> <target-stack>"
})

print("\n✅ CONFIGURATION DEMO complete!")
print("📋 Run 'pulumi config' to see all configuration")
print("🔍 Run 'pulumi stack output' to see configuration usage")
print("🌐 Visit the instance URLs to see configuration in action")
print("\n💡 Try changing configuration values and run 'pulumi up' to see updates!")