import pulumi
import pulumi_aws as aws
import json
import random

"""
Advanced Pulumi Features Demo

This demonstrates capabilities that are difficult or impossible with traditional IaC tools:
- Complex conditional logic
- Loops and dynamic resource creation
- Rich data structures and transformations
- Integration with external APIs
- Advanced configuration patterns
- Dynamic scaling based on conditions
"""

print("🚀 Starting Advanced Pulumi Features Demo...")
print("This showcases programming capabilities that make Pulumi unique!")

# Configuration with type safety and defaults
config = pulumi.Config()
environment = config.get("environment") or "demo"
instance_count = config.get_int("instance_count") or 3
enable_monitoring = config.get_bool("enable_monitoring") or True
enable_backup = config.get_bool("enable_backup") or False
cost_optimization = config.get_bool("cost_optimization") or True

print(f"📊 Configuration: {environment} environment with {instance_count} instances")
print(f"🔍 Monitoring: {'✅ Enabled' if enable_monitoring else '❌ Disabled'}")
print(f"💾 Backup: {'✅ Enabled' if enable_backup else '❌ Disabled'}")

# Dynamic data sources - Get current AWS information
current_region = aws.get_region()
caller_identity = aws.get_caller_identity()
availability_zones = aws.get_availability_zones(state='available')

# Complex conditional logic - Environment-based configuration
def get_environment_config(env):
    """
    Complex configuration logic that would be very difficult in Terraform HCL
    """
    configs = {
        "dev": {
            "instance_type": "t3.micro",
            "min_size": 1,
            "max_size": 2,
            "enable_detailed_monitoring": False,
            "backup_retention": 7,
            "multi_az": False,
            "allowed_cidr": "0.0.0.0/0"  # Open for dev
        },
        "staging": {
            "instance_type": "t3.small", 
            "min_size": 2,
            "max_size": 4,
            "enable_detailed_monitoring": True,
            "backup_retention": 14,
            "multi_az": True,
            "allowed_cidr": "10.0.0.0/8"  # Restricted
        },
        "production": {
            "instance_type": "t3.medium",
            "min_size": 3,
            "max_size": 10,
            "enable_detailed_monitoring": True,
            "backup_retention": 30,
            "multi_az": True,
            "allowed_cidr": "10.0.0.0/8"  # Highly restricted
        }
    }
    
    # Apply cost optimization if enabled
    if cost_optimization and env != "production":
        config = configs.get(env, configs["dev"])
        if config["instance_type"] == "t3.medium":
            config["instance_type"] = "t3.small"
        elif config["instance_type"] == "t3.small":
            config["instance_type"] = "t3.micro"
        config["cost_optimized"] = True
    else:
        config = configs.get(env, configs["dev"])
        config["cost_optimized"] = False
    
    return config

env_config = get_environment_config(environment)
print(f"🎛️ Environment config: {json.dumps(env_config, indent=2)}")

# Create VPC with advanced configuration
advanced_vpc = aws.ec2.Vpc("advanced-demo-vpc",
    cidr_block="10.100.0.0/16",
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={
        "Name": f"advanced-demo-vpc-{environment}",
        "Environment": environment,
        "ManagedBy": "Pulumi-Advanced-Demo",
        "CostOptimized": str(env_config["cost_optimized"]),
        "Region": current_region.name,
        "Account": caller_identity.account_id
    }
)

# Advanced: Create subnets across multiple AZs using loops
subnets = []
route_table_associations = []

# Use list comprehension and enumerate - programming constructs!
selected_azs = availability_zones.names[:3] if env_config["multi_az"] else [availability_zones.names[0]]

print(f"🌐 Creating subnets across {len(selected_azs)} availability zones")

for i, az in enumerate(selected_azs):
    # Calculate CIDR dynamically
    cidr_block = f"10.100.{i+1}.0/24"
    
    subnet = aws.ec2.Subnet(f"advanced-subnet-{i}",
        vpc_id=advanced_vpc.id,
        cidr_block=cidr_block,
        availability_zone=az,
        map_public_ip_on_launch=True,
        tags={
            "Name": f"advanced-subnet-{i}-{az}",
            "Environment": environment,
            "AZ": az,
            "SubnetType": "Public",
            "CIDR": cidr_block
        }
    )
    subnets.append(subnet)

# Internet Gateway
advanced_igw = aws.ec2.InternetGateway("advanced-igw",
    vpc_id=advanced_vpc.id,
    tags={
        "Name": f"advanced-igw-{environment}",
        "Environment": environment
    }
)

# Route table with dynamic route configuration
routes = [
    {
        "cidr_block": "0.0.0.0/0",
        "gateway_id": advanced_igw.id
    }
]

# Add additional routes based on environment
if environment == "production":
    # In production, might have VPN or Direct Connect routes
    routes.append({
        "cidr_block": "192.168.0.0/16",
        "gateway_id": advanced_igw.id  # In real scenario, this would be VGW
    })

advanced_rt = aws.ec2.RouteTable("advanced-rt",
    vpc_id=advanced_vpc.id,
    routes=routes,
    tags={
        "Name": f"advanced-rt-{environment}",
        "Environment": environment,
        "RouteCount": str(len(routes))
    }
)

# Associate all subnets with route table using loops
for i, subnet in enumerate(subnets):
    association = aws.ec2.RouteTableAssociation(f"advanced-rt-assoc-{i}",
        subnet_id=subnet.id,
        route_table_id=advanced_rt.id
    )
    route_table_associations.append(association)

# Advanced security group with dynamic rules based on environment
base_security_rules = [
    {"port": 80, "protocol": "tcp", "description": "HTTP"},
    {"port": 443, "protocol": "tcp", "description": "HTTPS"}
]

# Add SSH with environment-specific restrictions
ssh_rule = {
    "port": 22, 
    "protocol": "tcp", 
    "description": "SSH",
    "cidr_blocks": [env_config["allowed_cidr"]]
}
base_security_rules.append(ssh_rule)

# Add monitoring port if monitoring is enabled
if enable_monitoring:
    base_security_rules.extend([
        {"port": 9090, "protocol": "tcp", "description": "Prometheus"},
        {"port": 3000, "protocol": "tcp", "description": "Grafana"}
    ])

# Add custom application ports based on instance count
if instance_count > 2:
    base_security_rules.append({"port": 8080, "protocol": "tcp", "description": "App Load Balancer Health Check"})

print(f"🔒 Creating security group with {len(base_security_rules)} rules")

advanced_sg = aws.ec2.SecurityGroup("advanced-sg",
    description="Advanced demo security group with dynamic rules",
    vpc_id=advanced_vpc.id,
    ingress=[
        {
            "from_port": rule["port"],
            "to_port": rule["port"],
            "protocol": rule["protocol"],
            "cidr_blocks": rule.get("cidr_blocks", ["0.0.0.0/0"]),
            "description": rule["description"]
        } for rule in base_security_rules
    ],
    egress=[{
        "from_port": 0,
        "to_port": 0,
        "protocol": "-1", 
        "cidr_blocks": ["0.0.0.0/0"]
    }],
    tags={
        "Name": f"advanced-sg-{environment}",
        "Environment": environment,
        "RuleCount": str(len(base_security_rules)),
        "MonitoringEnabled": str(enable_monitoring)
    }
)

# Get AMI dynamically with filters
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {"name": "name", "values": ["amzn2-ami-hvm-*"]},
        {"name": "architecture", "values": ["x86_64"]},
        {"name": "state", "values": ["available"]}
    ]
)

print(f"🖼️ Selected AMI: {ami.id}")



# Advanced: Create instances with complex logic and distribution
instances = []
load_balancer_targets = []

# Distribute instances across subnets evenly
for i in range(instance_count):
    subnet_index = i % len(subnets)
    
    # Generate unique instance configuration
    instance_config = {
        "name": f"advanced-instance-{i}",
        "subnet": subnets[subnet_index],
        "az": selected_azs[subnet_index],
        "monitoring": enable_monitoring and env_config["enable_detailed_monitoring"]
    }
    
    # Complex user data with environment-specific configuration
    user_data = generate_advanced_user_data(i, environment, instance_config, env_config)
    
    instance = aws.ec2.Instance(f"advanced-instance-{i}",
        instance_type=env_config["instance_type"],
        ami=ami.id,
        key_name="aws-365-keypair",
        security_groups=[advanced_sg.id],
        subnet_id=instance_config["subnet"].id,
        associate_public_ip_address=True,
        monitoring=instance_config["monitoring"],
        user_data=user_data,
        tags={
            "Name": f"advanced-instance-{i}",
            "Environment": environment,
            "InstanceNumber": str(i+1),
            "AZ": instance_config["az"],
            "ManagedBy": "Pulumi",
            "InstanceType": env_config["instance_type"],
            "MonitoringEnabled": str(instance_config["monitoring"]),
            "CostOptimized": str(env_config["cost_optimized"])
        }
    )
    instances.append(instance)

def generate_advanced_user_data(instance_num, env, config, env_config):
    """Generate advanced user data with dynamic content"""
    
    monitoring_setup = ""
    if enable_monitoring:
        monitoring_setup = """
# Install and configure monitoring
yum install -y amazon-cloudwatch-agent
cat <<EOF > /opt/aws/amazon-cloudwatch-agent/bin/config.json
{
    "metrics": {
        "namespace": "CustomApp",
        "metrics_collected": {
            "cpu": {"measurement": ["cpu_usage_idle", "cpu_usage_iowait"]},
            "disk": {"measurement": ["used_percent"], "resources": ["*"]},
            "mem": {"measurement": ["mem_used_percent"]}
        }
    }
}
EOF
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json -s
"""
    
    backup_setup = ""
    if enable_backup:
        backup_setup = """
# Setup backup scripts
mkdir -p /opt/backup
cat <<EOF > /opt/backup/backup.sh
#!/bin/bash
# Backup application data
tar -czf /opt/backup/app-backup-$(date +%Y%m%d).tar.gz /var/www/html/
# Keep only last 7 days of backups
find /opt/backup -name "*.tar.gz" -mtime +7 -delete
EOF
chmod +x /opt/backup/backup.sh
echo "0 2 * * * /opt/backup/backup.sh" | crontab -
"""
    
    return f"""#!/bin/bash
yum update -y
yum install -y httpd htop curl wget

# Install additional tools for {env} environment
{"yum install -y strace tcpdump" if env == "production" else ""}

systemctl start httpd
systemctl enable httpd

{monitoring_setup}
{backup_setup}

# Create advanced demo webpage
cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Advanced Pulumi Demo - Instance {instance_num + 1}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; padding: 20px;
        }}
        .container {{
            max-width: 1200px; margin: 0 auto;
            background: rgba(255,255,255,0.1); padding: 30px;
            border-radius: 20px; backdrop-filter: blur(15px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }}
        h1 {{
            font-size: 2.8rem; text-align: center; margin-bottom: 2rem;
            background: linear-gradient(45deg, #FFD700, #FFA500);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .grid {{
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px; margin: 2rem 0;
        }}
        .card {{
            background: rgba(255,255,255,0.15); padding: 25px;
            border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);
        }}
        .card h3 {{ color: #FFD700; margin-bottom: 15px; }}
        .highlight {{ color: #FFD700; font-weight: bold; }}
        .feature-list {{ list-style: none; padding: 0; }}
        .feature-list li {{ padding: 8px 0; }}
        .status-good {{ color: #4CAF50; }}
        .status-warning {{ color: #FF9800; }}
        .badge {{
            display: inline-block; padding: 5px 10px; margin: 3px;
            background: rgba(255,215,0,0.2); border-radius: 15px;
            font-size: 0.8rem; border: 1px solid rgba(255,215,0,0.3);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Advanced Pulumi Demo - Instance {instance_num + 1}/{instance_count}</h1>
        
        <div class="grid">
            <div class="card">
                <h3>🖥️ Instance Details</h3>
                <p><span class="highlight">Instance:</span> {instance_num + 1} of {instance_count}</p>
                <p><span class="highlight">Environment:</span> {env}</p>
                <p><span class="highlight">Instance Type:</span> {env_config["instance_type"]}</p>
                <p><span class="highlight">AZ:</span> {config["az"]}</p>
                <p><span class="highlight">Monitoring:</span> 
                   <span class="{'status-good' if config['monitoring'] else 'status-warning'}">
                   {'✅ Enabled' if config['monitoring'] else '❌ Disabled'}
                   </span>
                </p>
                <p><span class="highlight">Cost Optimized:</span> 
                   {'✅ Yes' if env_config['cost_optimized'] else '❌ No'}
                </p>
            </div>
            
            <div class="card">
                <h3>🌐 Network Information</h3>
                <p><span class="highlight">Public IP:</span> $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)</p>
                <p><span class="highlight">Private IP:</span> $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)</p>
                <p><span class="highlight">Instance ID:</span> $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>
                <p><span class="highlight">Region:</span> $(curl -s http://169.254.169.254/latest/meta-data/placement/region)</p>
            </div>
            
            <div class="card">
                <h3>⚡ Advanced Features</h3>
                <ul class="feature-list">
                    <li>🔄 Dynamic instance count: {instance_count}</li>
                    <li>🌐 Multi-AZ deployment: {'✅' if env_config['multi_az'] else '❌'}</li>
                    <li>🎛️ Environment-based config: ✅</li>
                    <li>🔍 Monitoring: {'✅' if enable_monitoring else '❌'}</li>
                    <li>💾 Backup: {'✅' if enable_backup else '❌'}</li>
                    <li>💰 Cost optimization: {'✅' if env_config['cost_optimized'] else '❌'}</li>
                </ul>
            </div>
            
            <div class="card">
                <h3>🏗️ Infrastructure Tags</h3>
                <div>
                    <span class="badge">Environment: {env}</span>
                    <span class="badge">Instance: {instance_num + 1}</span>
                    <span class="badge">AZ: {config['az']}</span>
                    <span class="badge">Monitoring: {'On' if config['monitoring'] else 'Off'}</span>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h3>🎯 Pulumi Programming Advantages</h3>
            <ul class="feature-list">
                <li>🔄 <strong>Real loops:</strong> Created {instance_count} instances with for loops</li>
                <li>🎯 <strong>Complex conditionals:</strong> Environment-specific configurations</li>
                <li>📊 <strong>Rich data structures:</strong> Nested objects and arrays</li>
                <li>🧮 <strong>Dynamic calculations:</strong> CIDR blocks, subnet distribution</li>
                <li>🎛️ <strong>Configuration management:</strong> Type-safe config with defaults</li>
                <li>🏗️ <strong>Component abstraction:</strong> Reusable infrastructure patterns</li>
            </ul>
        </div>
        
        <div style="text-align: center; margin-top: 2rem; padding: 20px; background: linear-gradient(45deg, rgba(0,255,0,0.2), rgba(0,200,0,0.3)); border-radius: 15px;">
            <h2>🎉 Advanced Infrastructure Deployed Successfully!</h2>
            <p><em>This demonstrates capabilities that are difficult or impossible with traditional IaC tools</em></p>
        </div>
    </div>
</body>
</html>
EOF

chown apache:apache /var/www/html/index.html
"""

# Advanced: Create Application Load Balancer if we have multiple instances
if instance_count > 1:
    print(f"⚖️ Creating Application Load Balancer for {instance_count} instances")
    
    # ALB
    alb = aws.lb.LoadBalancer("advanced-alb",
        load_balancer_type="application",
        subnets=[subnet.id for subnet in subnets],
        security_groups=[advanced_sg.id],
        enable_deletion_protection=False,  # For demo purposes
        tags={
            "Name": f"advanced-alb-{environment}",
            "Environment": environment,
            "InstanceCount": str(instance_count)
        }
    )
    
    # Target Group with health checks
    tg = aws.lb.TargetGroup("advanced-tg",
        port=80,
        protocol="HTTP",
        vpc_id=advanced_vpc.id,
        target_type="instance",
        health_check={
            "enabled": True,
            "path": "/",
            "port": "80",
            "protocol": "HTTP",
            "healthy_threshold": 2,
            "unhealthy_threshold": 3,
            "timeout": 10,
            "interval": 30,
            "matcher": "200"
        },
        tags={
            "Name": f"advanced-tg-{environment}",
            "Environment": environment
        }
    )
    
    # Attach instances to target group
    target_attachments = []
    for i, instance in enumerate(instances):
        attachment = aws.lb.TargetGroupAttachment(f"advanced-tg-attachment-{i}",
            target_group_arn=tg.arn,
            target_id=instance.id,
            port=80
        )
        target_attachments.append(attachment)
    
    # ALB Listener
    listener = aws.lb.Listener("advanced-listener",
        load_balancer_arn=alb.arn,
        port=80,
        protocol="HTTP",
        default_actions=[{
            "type": "forward",
            "target_group_arn": tg.arn
        }]
    )
    
    # Export load balancer information
    pulumi.export("load_balancer_info", {
        "dns_name": alb.dns_name,
        "url": alb.dns_name.apply(lambda dns: f"http://{dns}"),
        "zone_id": alb.zone_id,
        "target_count": len(target_attachments)
    })

# Advanced outputs with complex data structures and calculations
total_resources = len(instances) + len(subnets) + len(route_table_associations) + 4  # +4 for VPC, IGW, RT, SG
monthly_cost_estimate = calculate_monthly_cost(instances, env_config["instance_type"], enable_monitoring)

pulumi.export("advanced_deployment_summary", {
    "deployment_metadata": {
        "timestamp": pulumi.runtime.get_time(),
        "environment": environment,
        "region": current_region.name,
        "account": caller_identity.account_id,
        "pulumi_version": "3.x"
    },
    "infrastructure_stats": {
        "total_instances": instance_count,
        "total_subnets": len(subnets),
        "total_availability_zones": len(selected_azs),
        "total_resources_created": total_resources,
        "security_group_rules": len(base_security_rules)
    },
    "configuration": {
        "environment_config": env_config,
        "monitoring_enabled": enable_monitoring,
        "backup_enabled": enable_backup,
        "cost_optimization": cost_optimization,
        "multi_az_deployment": env_config["multi_az"]
    },
    "estimated_costs": {
        "monthly_estimate_usd": monthly_cost_estimate,
        "instance_type": env_config["instance_type"],
        "cost_optimized": env_config["cost_optimized"]
    }
})

# Export instance details with rich information
pulumi.export("instance_details", [
    {
        "instance_number": i + 1,
        "name": f"advanced-instance-{i}",
        "public_ip": instance.public_ip,
        "instance_id": instance.id,
        "availability_zone": selected_azs[i % len(selected_azs)],
        "subnet_cidr": f"10.100.{(i % len(subnets)) + 1}.0/24",
        "monitoring_enabled": enable_monitoring and env_config["enable_detailed_monitoring"],
        "urls": {
            "website": instance.public_ip.apply(lambda ip: f"http://{ip}"),
            "ssh": instance.public_ip.apply(lambda ip: f"ssh -i aws-365-keypair.pem ec2-user@{ip}")
        }
    }
    for i, instance in enumerate(instances)
])

# Advanced: Export environment comparison
pulumi.export("environment_comparison", {
    env: get_environment_config(env) 
    for env in ["dev", "staging", "production"]
})

# Export Pulumi advantages demonstrated
pulumi.export("pulumi_advantages_demonstrated", {
    "programming_constructs": [
        "Complex conditional logic (if/else, nested conditions)",
        "Loops and iterations (for loops, list comprehensions)",
        "Functions and methods (custom configuration logic)",
        "Rich data structures (nested dictionaries, lists)",
        "Dynamic calculations (CIDR blocks, resource distribution)"
    ],
    "infrastructure_capabilities": [
        "Dynamic resource creation based on parameters",
        "Environment-specific configurations",
        "Advanced tagging strategies",
        "Complex security group rule generation",
        "Load balancer with health checks",
        "Multi-AZ deployment logic"
    ],
    "developer_experience": [
        "Type-safe configuration with IntelliSense",
        "Compile-time error checking",
        "Debugging support in IDE",
        "Refactoring and code organization",
        "Unit testing capabilities",
        "Integration with version control"
    ]
})

def calculate_monthly_cost(instances, instance_type, monitoring):
    """Calculate estimated monthly costs"""
    # Simplified cost calculation for demo
    hourly_costs = {
        't3.micro': 0.0104,
        't3.small': 0.0208, 
        't3.medium': 0.0416,
        't3.large': 0.0832
    }
    
    base_cost = hourly_costs.get(instance_type, 0.0104) * 24 * 30 * len(instances)
    monitoring_cost = 0.30 * len(instances) if monitoring else 0  # CloudWatch costs
    
    return round(base_cost + monitoring_cost, 2)

print("✅ Advanced Pulumi demo infrastructure deployed successfully!")
print(f"📊 Created {total_resources} total resources across {len(selected_azs)} AZs")
print(f"💰 Estimated monthly cost: ${monthly_cost_estimate}")
print(f"🔧 Environment: {environment} ({'cost optimized' if env_config['cost_optimized'] else 'standard config'})")
print("🎯 This demonstrates programming capabilities impossible with traditional IaC tools!")

# Final summary export
pulumi.export("demo_summary", {
    "title": "Advanced Pulumi Features Demonstration",
    "key_achievements": [
        f"Deployed {instance_count} instances across {len(selected_azs)} availability zones",
        f"Applied environment-specific configuration for {environment}",
        f"Created {len(base_security_rules)} dynamic security group rules",
        f"Generated complex user data with conditional features",
        f"Implemented cost optimization logic",
        f"Demonstrated programming constructs impossible in HCL"
    ],
    "next_steps": [
        "Test load balancing across instances",
        "Verify monitoring and backup configurations", 
        "Scale the deployment by changing instance_count",
        "Switch environments by changing environment config",
        "Add additional features using programming logic"
    ],
    "presentation_talking_points": [
        "Show the complex conditional logic in get_environment_config()",
        "Highlight the dynamic security group rule generation",
        "Demonstrate the for loops creating resources",
        "Explain how this would be nearly impossible in Terraform",
        "Show the rich data structures in outputs",
        "Emphasize the IDE support and IntelliSense"
    ]
})