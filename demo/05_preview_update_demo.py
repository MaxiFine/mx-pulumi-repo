"""
CORE CONCEPT 5: PREVIEW & UPDATE - Safe deployment workflow
==========================================================

This demo shows Pulumi's safe deployment workflow:
- Preview changes before applying (pulumi preview)
- Update infrastructure safely (pulumi up)
- Rollback capabilities (pulumi history, pulumi cancel)
- Watch mode for continuous updates (pulumi watch)
- Destroy workflow (pulumi destroy)

Demo Flow:
1. Initial preview and deployment
2. Make changes and show preview
3. Apply updates safely
4. Show rollback capabilities
5. Demonstrate destroy workflow
"""

import pulumi
import pulumi_aws as aws
import json

print("🔄 PREVIEW & UPDATE DEMO: Safe Deployment Workflow")
print("=" * 60)

# =======================
# DEPLOYMENT WORKFLOW SETUP
# =======================
print("🚀 1. SAFE DEPLOYMENT WORKFLOW DEMONSTRATION")

# Configuration for deployment demo
config = pulumi.Config()
deployment_version = config.get("deployment_version", "1.0")
enable_monitoring = config.get_bool("enable_monitoring", False)

print(f"   📋 Deployment Version: {deployment_version}")
print(f"   📊 Monitoring Enabled: {enable_monitoring}")

# Get AMI for consistency
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[{"name": "name", "values": ["amzn2-ami-hvm-*"]}]
)

# =======================
# INFRASTRUCTURE DEFINITION
# =======================
print("\n🏗️ 2. DEFINING INFRASTRUCTURE FOR PREVIEW/UPDATE DEMO")

# VPC for preview/update demo
vpc = aws.ec2.Vpc(
    "preview-update-vpc",
    cidr_block="10.200.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    tags={
        "Name": "preview-update-vpc",
        "Purpose": "PreviewUpdateDemo", 
        "Version": deployment_version,
        "LastUpdate": "TBD"  # Will be updated in subsequent deployments
    }
)

# Internet Gateway
igw = aws.ec2.InternetGateway(
    "preview-update-igw",
    vpc_id=vpc.id,
    tags={
        "Name": "preview-update-igw",
        "Purpose": "PreviewUpdateDemo",
        "Version": deployment_version
    }
)

# Subnet
subnet = aws.ec2.Subnet(
    "preview-update-subnet",
    vpc_id=vpc.id,
    cidr_block="10.200.1.0/24",
    availability_zone=aws.get_availability_zones().names[0],
    map_public_ip_on_launch=True,
    tags={
        "Name": "preview-update-subnet",
        "Purpose": "PreviewUpdateDemo",
        "Version": deployment_version
    }
)

# Route table
route_table = aws.ec2.RouteTable(
    "preview-update-rt",
    vpc_id=vpc.id,
    routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
    tags={
        "Name": "preview-update-rt", 
        "Purpose": "PreviewUpdateDemo",
        "Version": deployment_version
    }
)

aws.ec2.RouteTableAssociation(
    "preview-update-rt-assoc",
    subnet_id=subnet.id,
    route_table_id=route_table.id
)

# =======================
# SECURITY GROUP - WILL BE UPDATED IN DEMO
# =======================
print("\n🔒 3. SECURITY GROUP (WILL DEMONSTRATE UPDATES)")

# Base security group rules
base_ingress = [
    {
        "description": "HTTP Access",
        "from_port": 80,
        "to_port": 80,
        "protocol": "tcp", 
        "cidr_blocks": ["0.0.0.0/0"]
    }
]

# Add SSH if this is version 2.0 or higher
if float(deployment_version) >= 2.0:
    base_ingress.append({
        "description": "SSH Access - Added in v2.0",
        "from_port": 22,
        "to_port": 22,
        "protocol": "tcp",
        "cidr_blocks": ["0.0.0.0/0"]
    })
    print("   ✅ SSH access enabled (version >= 2.0)")

# Add HTTPS if this is version 3.0 or higher  
if float(deployment_version) >= 3.0:
    base_ingress.append({
        "description": "HTTPS Access - Added in v3.0",
        "from_port": 443,
        "to_port": 443,
        "protocol": "tcp",
        "cidr_blocks": ["0.0.0.0/0"]
    })
    print("   ✅ HTTPS access enabled (version >= 3.0)")

security_group = aws.ec2.SecurityGroup(
    "preview-update-sg",
    name="preview-update-sg",
    description=f"Security group for preview/update demo v{deployment_version}",
    vpc_id=vpc.id,
    ingress=base_ingress,
    egress=[{
        "from_port": 0,
        "to_port": 0,
        "protocol": "-1",
        "cidr_blocks": ["0.0.0.0/0"]
    }],
    tags={
        "Name": "preview-update-sg",
        "Purpose": "PreviewUpdateDemo",
        "Version": deployment_version,
        "RulesCount": str(len(base_ingress))
    }
)

# =======================
# S3 BUCKET - FOR UPDATE DEMO
# =======================
s3_bucket = aws.s3.Bucket(
    "preview-update-demo-bucket",
    tags={
        "Name": "preview-update-demo-bucket",
        "Purpose": "PreviewUpdateDemo",
        "Version": deployment_version
    }
)

# Optional: Add bucket policy if monitoring is enabled
if enable_monitoring:
    bucket_policy = aws.s3.BucketPolicy(
        "preview-update-bucket-policy",
        bucket=s3_bucket.id,
        policy=s3_bucket.id.apply(lambda bucket_name: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "cloudtrail.amazonaws.com"},
                    "Action": "s3:PutObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/logs/*",
                    "Condition": {
                        "StringEquals": {
                            "s3:x-amz-acl": "bucket-owner-full-control"
                        }
                    }
                }
            ]
        }))
    )
    print("   ✅ S3 bucket policy added (monitoring enabled)")

# =======================
# EC2 INSTANCE WITH DEPLOYMENT INFO  
# =======================
print("\n💻 4. EC2 INSTANCE WITH DEPLOYMENT WORKFLOW DEMO")

instance = aws.ec2.Instance(
    "preview-update-instance",
    instance_type="t2.micro",
    ami=ami.id,
    subnet_id=subnet.id,
    vpc_security_group_ids=[security_group.id],
    user_data=f"""#!/bin/bash
yum update -y
yum install -y httpd aws-cli git

systemctl start httpd
systemctl enable httpd

# Create deployment info page
cat > /var/www/html/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head><title>Preview & Update Demo v{deployment_version}</title></head>
<body style="font-family: Arial; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; min-height: 100vh;">
    <div style="max-width: 1000px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 40px; border-radius: 20px; backdrop-filter: blur(15px);">
        
        <h1>🔄 PREVIEW & UPDATE WORKFLOW DEMO</h1>
        <h2 style="color: #FFD700;">Version {deployment_version}</h2>
        
        <div style="background: rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #FFD700;">📋 Current Deployment Status:</h3>
            <ul>
                <li><strong>Deployment Version:</strong> {deployment_version}</li>
                <li><strong>Monitoring Enabled:</strong> {enable_monitoring}</li>
                <li><strong>Security Group Rules:</strong> {len(base_ingress)} rules</li>
                <li><strong>Instance Type:</strong> t2.micro</li>
                <li><strong>VPC CIDR:</strong> 10.200.0.0/16</li>
            </ul>
        </div>
        
        <div style="background: rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #FFD700;">🚀 Safe Deployment Workflow:</h3>
            <ol>
                <li><strong>Preview:</strong> <code>pulumi preview</code> - See changes before applying</li>
                <li><strong>Update:</strong> <code>pulumi up</code> - Apply changes safely</li>
                <li><strong>History:</strong> <code>pulumi history</code> - View deployment history</li>
                <li><strong>Rollback:</strong> <code>pulumi up --target-dependents</code> - Rollback if needed</li>
                <li><strong>Destroy:</strong> <code>pulumi destroy --preview</code> - Preview destruction</li>
            </ol>
        </div>
        
        <div style="background: rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #FFD700;">🔧 Try These Updates:</h3>
            <div style="background: rgba(0,255,0,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4>Version 2.0 Update:</h4>
                <code>pulumi config set deployment_version "2.0"</code><br>
                <code>pulumi preview</code> (see SSH rule will be added)<br>
                <code>pulumi up</code> (apply the change)
            </div>
            <div style="background: rgba(0,255,0,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4>Version 3.0 Update:</h4>
                <code>pulumi config set deployment_version "3.0"</code><br>
                <code>pulumi preview</code> (see HTTPS rule will be added)<br>
                <code>pulumi up</code> (apply the change)
            </div>
            <div style="background: rgba(255,255,0,0.1); padding: 15px; border-radius: 10px; margin: 10px 0;">
                <h4>Enable Monitoring:</h4>
                <code>pulumi config set enable_monitoring true</code><br>
                <code>pulumi preview</code> (see S3 bucket policy will be added)<br>
                <code>pulumi up</code> (apply the change)
            </div>
        </div>
        
        <div style="background: rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #FFD700;">⚡ Advanced Workflow Features:</h3>
            <ul>
                <li><strong>Watch Mode:</strong> <code>pulumi watch</code> - Auto-deploy on file changes</li>
                <li><strong>Targeted Updates:</strong> <code>pulumi up --target resource-name</code></li>
                <li><strong>Refresh State:</strong> <code>pulumi refresh</code> - Sync with reality</li>
                <li><strong>Cancel Deployment:</strong> <code>pulumi cancel</code> - Stop in-progress deployment</li>
                <li><strong>Stack History:</strong> <code>pulumi history</code> - See all deployments</li>
            </ul>
        </div>
        
        <div style="background: rgba(255,255,255,0.15); padding: 25px; border-radius: 15px; margin: 20px 0;">
            <h3 style="color: #FFD700;">🛡️ Safety Features:</h3>
            <ul>
                <li>✅ Preview shows exactly what will change</li>
                <li>✅ Confirmation required for destructive changes</li>
                <li>✅ Rollback capabilities with deployment history</li>
                <li>✅ Resource dependency management</li>
                <li>✅ Atomic updates (all or nothing)</li>
                <li>✅ State consistency checks</li>
            </ul>
        </div>
        
        <h3>🎯 Next Steps:</h3>
        <p>1. Run <code>pulumi preview</code> to see what this deployment will create</p>
        <p>2. Run <code>pulumi up</code> to deploy safely</p>
        <p>3. Try changing configuration and preview the updates</p>
        <p>4. Use <code>pulumi history</code> to track all changes</p>
        
        <p style="text-align: center; margin-top: 30px;"><strong>Safe deployments with confidence!</strong></p>
    </div>
</body>
</html>
EOF

# Create deployment log
cat > /tmp/deployment-log.txt << LOGEOF
Deployment Version: {deployment_version}
Timestamp: $(date)
Security Group Rules: {len(base_ingress)}
Monitoring Enabled: {enable_monitoring}
Instance Type: t2.micro
VPC CIDR: 10.200.0.0/16
LOGEOF

# Upload deployment log to S3 if bucket exists
aws s3 cp /tmp/deployment-log.txt s3://$(echo "{s3_bucket.id}" | tr -d '"')/deployment-v{deployment_version}-$(date +%Y%m%d-%H%M%S).log || echo "S3 upload failed - bucket might not exist yet"
""",
    tags={
        "Name": "preview-update-instance",
        "Purpose": "PreviewUpdateDemo",
        "Version": deployment_version,
        "DeploymentType": "preview-update-demo"
    }
)

print("   ✅ EC2 Instance defined with deployment workflow demo")

# =======================
# OUTPUTS FOR WORKFLOW DEMO
# =======================
print("\n📤 5. DEPLOYMENT WORKFLOW OUTPUTS AND COMMANDS")

pulumi.export("demo_type", "Preview & Update Workflow Demo")

# Current deployment info
pulumi.export("deployment_info", {
    "version": deployment_version,
    "monitoring_enabled": enable_monitoring,
    "security_rules_count": len(base_ingress),
    "timestamp": "deployment-time-will-be-set-on-apply"
})

# Workflow commands for demo
pulumi.export("workflow_commands", {
    "preview_changes": "pulumi preview",
    "apply_changes": "pulumi up", 
    "view_history": "pulumi history",
    "refresh_state": "pulumi refresh",
    "watch_mode": "pulumi watch",
    "cancel_deployment": "pulumi cancel",
    "destroy_preview": "pulumi destroy --preview",
    "destroy_apply": "pulumi destroy"
})

# Version upgrade demo
pulumi.export("version_upgrade_demo", {
    "current_version": deployment_version,
    "upgrade_to_v2": {
        "command": "pulumi config set deployment_version '2.0'",
        "change": "Adds SSH access (port 22)",
        "preview": "pulumi preview",
        "apply": "pulumi up"
    },
    "upgrade_to_v3": {
        "command": "pulumi config set deployment_version '3.0'", 
        "change": "Adds HTTPS access (port 443)",
        "preview": "pulumi preview",
        "apply": "pulumi up"
    },
    "enable_monitoring": {
        "command": "pulumi config set enable_monitoring true",
        "change": "Adds S3 bucket policy for monitoring",
        "preview": "pulumi preview", 
        "apply": "pulumi up"
    }
})

# Access information
pulumi.export("demo_access", {
    "instance_url": instance.public_ip.apply(lambda ip: f"http://{ip}"),
    "ssh_command": instance.public_ip.apply(lambda ip: f"ssh -i your-key.pem ec2-user@{ip}") if float(deployment_version) >= 2.0 else "SSH not available in v1.0",
    "s3_bucket": s3_bucket.id
})

# Safety features demonstration
pulumi.export("safety_features", {
    "preview_first": "Always run 'pulumi preview' before 'pulumi up'",
    "confirmation_required": "Destructive changes require confirmation",
    "atomic_updates": "Updates are atomic - all succeed or all fail",
    "rollback_available": "Use 'pulumi history' and target specific updates",
    "state_consistency": "State is always consistent with reality"
})

print("\n✅ PREVIEW & UPDATE DEMO complete!")
print("🔍 Run 'pulumi preview' to see what will be created")
print("🚀 Run 'pulumi up' to deploy safely")
print("📊 Run 'pulumi history' after deployment to see deployment history")
print("💡 Try changing deployment_version config and preview the changes!")
print("🌐 Visit the instance URL to see workflow information")