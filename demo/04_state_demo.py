"""
CORE CONCEPT 4: STATE - How Pulumi tracks infrastructure changes
==============================================================

This demo shows how Pulumi state management works:
- State storage (local vs cloud)
- State tracking of resource changes
- Import existing resources into state
- State inspection and manipulation
- Drift detection

Demo Flow:
1. Show initial state creation
2. Make changes and show state diff
3. Import existing resource
4. Show state inspection commands
"""

import pulumi
import pulumi_aws as aws
import json

print("📊 STATE DEMO: Understanding Pulumi State Management")
print("=" * 60)

# =======================
# STATE TRACKING SETUP
# =======================
print("💾 1. STATE MANAGEMENT DEMONSTRATION")

# Create some resources to track in state
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
)

# Resource 1: VPC (will be tracked in state)
vpc = aws.ec2.Vpc(
    "state-demo-vpc",
    cidr_block="10.100.0.0/16",  # Different CIDR for state demo
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "state-demo-vpc",
        "Purpose": "StateDemo",
        "StateTracking": "managed-by-pulumi"
    }
)
print("   ✅ VPC resource defined (will be tracked in state)")

# Resource 2: Internet Gateway 
igw = aws.ec2.InternetGateway(
    "state-demo-igw", 
    vpc_id=vpc.id,
    tags={
        "Name": "state-demo-igw",
        "Purpose": "StateDemo",
        "StateTracking": "managed-by-pulumi"
    }
)
print("   ✅ Internet Gateway defined (depends on VPC state)")

# Resource 3: Subnet
subnet = aws.ec2.Subnet(
    "state-demo-subnet",
    vpc_id=vpc.id,
    cidr_block="10.100.1.0/24",
    availability_zone=aws.get_availability_zones().names[0],
    map_public_ip_on_launch=True,
    tags={
        "Name": "state-demo-subnet", 
        "Purpose": "StateDemo",
        "StateTracking": "managed-by-pulumi"
    }
)

# Route table and association
route_table = aws.ec2.RouteTable(
    "state-demo-rt",
    vpc_id=vpc.id,
    routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    tags={
        "Name": "state-demo-rt",
        "Purpose": "StateDemo"
    }
)

aws.ec2.RouteTableAssociation(
    "state-demo-rt-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# =======================
# DEMONSTRATING STATE CHANGES
# =======================
print("\n🔄 2. DEMONSTRATING STATE CHANGE TRACKING")

# Security Group - we'll modify this to show state changes
security_group = aws.ec2.SecurityGroup(
    "state-demo-sg",
    name="state-demo-sg",
    description="Security group for state demo - Version 1",
    vpc_id=vpc.id,
    ingress=[
        {
            "description": "HTTP - Initial State",
            "from_port": 80,
            "to_port": 80, 
            "protocol": "tcp",
            "cidr_blocks": ["0.0.0.0/0"]
        }
        # Note: SSH rule intentionally missing initially
        # Add it later to demonstrate state changes
    ],
    egress=[{
        "from_port": 0,
        "to_port": 0,
        "protocol": "-1", 
        "cidr_blocks": ["0.0.0.0/0"]
    }],
    tags={
        "Name": "state-demo-sg",
        "Purpose": "StateDemo",
        "Version": "1.0",
        "StateDemo": "initial-version"
    }
)
print("   ✅ Security Group defined (Version 1.0 - only HTTP)")

# =======================
# S3 Bucket for state demo  
# =======================
s3_bucket = aws.s3.Bucket(
    "state-demo-bucket",
    tags={
        "Name": "state-demo-bucket",
        "Purpose": "StateDemo",
        "StateTracking": "managed-by-pulumi"
    }
)

# Bucket versioning configuration
bucket_versioning = aws.s3.BucketVersioning(
    "state-demo-bucket-versioning",
    bucket=s3_bucket.id,
    versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
        status="Enabled"
    )
)

print("   ✅ S3 Bucket with versioning (state tracking enabled)")

# =======================
# EC2 INSTANCE WITH STATE DEMO
# =======================
instance = aws.ec2.Instance(
    "state-demo-instance",
    instance_type="t2.micro",
    ami=ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[security_group.id],
    user_data="""#!/bin/bash
yum update -y
yum install -y httpd aws-cli

systemctl start httpd
systemctl enable httpd

# Create demo page about state management
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>State Management Demo</title></head>
<body style="font-family: Arial; margin: 40px; background: #f0f0f0;">
    <h1>📊 PULUMI STATE MANAGEMENT DEMO</h1>
    <div style="background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
        
        <h2>Current Infrastructure State:</h2>
        <div style="background: #e8f4fd; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>📦 Resources in Pulumi State:</h3>
            <ul>
                <li>✅ VPC (10.100.0.0/16)</li>
                <li>✅ Internet Gateway</li>
                <li>✅ Public Subnet (10.100.1.0/24)</li>
                <li>✅ Route Table & Association</li>
                <li>✅ Security Group (HTTP only - Version 1.0)</li>
                <li>✅ EC2 Instance (this server!)</li>
                <li>✅ S3 Bucket with versioning</li>
            </ul>
        </div>
        
        <div style="background: #fff2e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>🔄 State Management Features:</h3>
            <ul>
                <li><strong>State Tracking:</strong> Pulumi knows about all these resources</li>
                <li><strong>Drift Detection:</strong> Can detect manual changes</li>
                <li><strong>Resource Import:</strong> Can adopt existing resources</li>
                <li><strong>Dependency Tracking:</strong> Knows resource relationships</li>
                <li><strong>Change Planning:</strong> Preview before applying changes</li>
            </ul>
        </div>
        
        <div style="background: #e8f8e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>🛠️ State Commands to Try:</h3>
            <ul>
                <li><code>pulumi stack export</code> - Export current state</li>
                <li><code>pulumi state delete &lt;resource&gt;</code> - Remove from state</li>
                <li><code>pulumi import &lt;type&gt; &lt;name&gt; &lt;id&gt;</code> - Import existing</li>
                <li><code>pulumi refresh</code> - Sync state with reality</li>
                <li><code>pulumi preview</code> - See what would change</li>
            </ul>
        </div>
        
        <div style="background: #ffe8e8; padding: 15px; border-radius: 5px; margin: 10px 0;">
            <h3>⚠️ State Change Demo:</h3>
            <p>To see state changes in action:</p>
            <ol>
                <li>Manually modify a resource in AWS Console</li>
                <li>Run <code>pulumi refresh</code> to detect drift</li>
                <li>Run <code>pulumi up</code> to restore desired state</li>
                <li>Or update the Pulumi code and run <code>pulumi preview</code></li>
            </ol>
        </div>
        
        <h3>💾 State Storage:</h3>
        <p>This demo uses <strong>local state</strong> storage.</p>
        <p>For teams, use <strong>cloud state</strong>: <code>pulumi login</code></p>
        
        <p><strong>State makes infrastructure reliable and predictable!</strong></p>
    </div>
</body>
</html>
EOF

# Create a state info file
cat > /tmp/state-info.json << STATEEOF
{
    "message": "This instance is tracked in Pulumi state",
    "vpc": "state-demo-vpc", 
    "subnet": "state-demo-subnet",
    "security_group": "state-demo-sg",
    "purpose": "State management demonstration",
    "state_features": [
        "Resource tracking",
        "Dependency management", 
        "Change detection",
        "Import capability",
        "State export/import"
    ]
}
STATEEOF

# Upload to S3 to demonstrate S3 bucket state tracking
aws s3 cp /tmp/state-info.json s3://$(cat > /tmp/get-bucket-name.py << GETBUCKET
import boto3
import json

# Get the bucket name from tags
ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

# Find our demo bucket
buckets = s3.list_buckets()
for bucket in buckets['Buckets']:
    try:
        tags = s3.get_bucket_tagging(Bucket=bucket['Name'])
        for tag in tags['TagSet']:
            if tag['Key'] == 'Purpose' and tag['Value'] == 'StateDemo':
                print(bucket['Name'])
                break
    except:
        continue
GETBUCKET
python3 /tmp/get-bucket-name.py)/state-info.json || echo "S3 upload failed - that's ok for demo"
""",
    tags={
        "Name": "state-demo-instance",
        "Purpose": "StateDemo", 
        "StateTracking": "managed-by-pulumi",
        "Version": "1.0"
    }
)

print("   ✅ EC2 Instance defined (tracked in state)")

# =======================
# STATE INFORMATION OUTPUTS
# =======================
print("\n📤 3. STATE INFORMATION AND COMMANDS")

pulumi.export("demo_type", "State Management Demo")

# Export state information
pulumi.export("state_info", {
    "stack_name": pulumi.get_stack(),
    "project_name": pulumi.get_project(),
    "resources_managed": 7,  # VPC, IGW, Subnet, RT, RT-Assoc, SG, Instance, S3, S3-Versioning
    "state_storage": "local",  # or "cloud" if using pulumi login
})

# Resource state tracking info
pulumi.export("resources_in_state", {
    "vpc": {
        "logical_name": "state-demo-vpc",
        "type": "aws:ec2/vpc:Vpc",
        "physical_id": vpc.id
    },
    "internet_gateway": {
        "logical_name": "state-demo-igw", 
        "type": "aws:ec2/internetGateway:InternetGateway",
        "physical_id": igw.id
    },
    "subnet": {
        "logical_name": "state-demo-subnet",
        "type": "aws:ec2/subnet:Subnet", 
        "physical_id": subnet.id
    },
    "security_group": {
        "logical_name": "state-demo-sg",
        "type": "aws:ec2/securityGroup:SecurityGroup",
        "physical_id": security_group.id
    },
    "ec2_instance": {
        "logical_name": "state-demo-instance",
        "type": "aws:ec2/instance:Instance",
        "physical_id": instance.id
    },
    "s3_bucket": {
        "logical_name": "state-demo-bucket",
        "type": "aws:s3/bucket:Bucket",
        "physical_id": s3_bucket.id
    }
})

# State management commands for demo
pulumi.export("state_commands", {
    "export_state": "pulumi stack export",
    "import_state": "pulumi stack import --file state.json",
    "view_resources": "pulumi stack --show-urns",
    "refresh_state": "pulumi refresh",
    "preview_changes": "pulumi preview",
    "import_resource": "pulumi import aws:s3/bucket:Bucket imported-bucket bucket-name"
})

# Demo URLs and access
pulumi.export("demo_access", {
    "instance_url": instance.public_ip.apply(lambda ip: f"http://{ip}"),
    "ssh_command": instance.public_ip.apply(lambda ip: f"ssh -i your-key.pem ec2-user@{ip}"),
    "s3_bucket": s3_bucket.id
})

# State change demo instructions
pulumi.export("state_change_demo", {
    "step1": "Manually change security group in AWS Console",
    "step2": "Run 'pulumi refresh' to detect drift", 
    "step3": "Run 'pulumi up' to restore desired state",
    "step4": "Or modify code and run 'pulumi preview' to see planned changes"
})

print("\n✅ STATE DEMO complete!")
print("📊 Run 'pulumi stack export' to see current state")
print("🔍 Run 'pulumi stack --show-urns' to see resource URNs")
print("🌐 Visit instance URL to see state management info")
print("💡 Try manual changes in AWS Console, then run 'pulumi refresh' to see drift detection!")