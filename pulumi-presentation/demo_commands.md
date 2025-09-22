# Pulumi Demo Commands Reference

This comprehensive command reference provides all the commands needed for your Pulumi presentation demo.

## 📋 Table of Contents

- [Initial Setup](#initial-setup)
- [Basic Demo Commands](#basic-demo-commands)
- [Component Demo Commands](#component-demo-commands)  
- [Advanced Demo Commands](#advanced-demo-commands)
- [Testing Commands](#testing-commands)
- [Import Demo Commands](#import-demo-commands)
- [Resource Management](#resource-management)
- [Troubleshooting Commands](#troubleshooting-commands)
- [Cleanup Commands](#cleanup-commands)

## 🚀 Initial Setup

### Prerequisites Check
```powershell
# Verify installations
pulumi version
aws --version  
python --version

# Check AWS credentials
aws sts get-caller-identity
```

### Project Initialization
```powershell
# Navigate to demo directory
cd c:\Users\MaxwellAdomako\amalitech\learning-projects\mx-pulumi-repo\pulumi-presentation

# Login to Pulumi (local backend for demo)
pulumi login --local

# Create new stack for presentation
pulumi stack init presentation-demo

# Set AWS region
pulumi config set aws:region us-east-1
```

### Verify Setup
```powershell
# Check current stack
pulumi stack ls

# View current configuration
pulumi config

# Test AWS connectivity
aws ec2 describe-regions --output table
```

## 🏗️ Basic Demo Commands

### Demo 1: Basic Infrastructure (__main__.py)

#### Deploy Infrastructure
```powershell
# Preview what will be created
pulumi preview

# Deploy infrastructure (with confirmation)
pulumi up

# Deploy without confirmation (for scripted demo)
pulumi up --yes
```

#### Check Results
```powershell
# View all stack outputs
pulumi stack output

# View specific outputs
pulumi stack output website_url
pulumi stack output ssh_command
pulumi stack output infrastructure_details

# View in JSON format
pulumi stack output --json
```

#### Test Deployment
```powershell
# Test website (replace with actual IP)
curl http://$(pulumi stack output instance_ip)

# Get SSH command and test connectivity
$ssh_cmd = pulumi stack output ssh_command
Write-Host "SSH Command: $ssh_cmd"

# View infrastructure details
pulumi stack output infrastructure_details --json | ConvertFrom-Json
```

## 🔄 Component Demo Commands

### Demo 2: Component Resources (demo_components.py)

#### Switch to Component Demo
```powershell
# Deploy component-based infrastructure
pulumi up -f demo_components.py

# Or copy and replace main file temporarily
Copy-Item demo_components.py __main__.py.backup
Move-Item __main__.py __main__.py.original  
Move-Item demo_components.py __main__.py
pulumi up
```

#### View Multi-Environment Results
```powershell
# Check development environment
pulumi stack output development --json

# Check staging environment  
pulumi stack output staging --json

# Check production environment
pulumi stack output production --json

# View deployment summary
pulumi stack output deployment_summary --json

# View cost analysis
pulumi stack output cost_analysis --json
```

#### Test Multiple Environments
```powershell
# Get URLs for all environments
$dev_url = pulumi stack output development --json | ConvertFrom-Json | Select-Object -ExpandProperty website_url
$staging_url = pulumi stack output staging --json | ConvertFrom-Json | Select-Object -ExpandProperty website_url  
$prod_url = pulumi stack output production --json | ConvertFrom-Json | Select-Object -ExpandProperty website_url

Write-Host "Development: $dev_url"
Write-Host "Staging: $staging_url"
Write-Host "Production: $prod_url"

# Test each environment
curl $dev_url
curl $staging_url
curl $prod_url
```

## ⚡ Advanced Demo Commands

### Demo 3: Advanced Features (advanced_demo.py)

#### Configure Advanced Demo
```powershell
# Set configuration for advanced features
pulumi config set environment production
pulumi config set instance_count 5
pulumi config set enable_monitoring true
pulumi config set enable_backup true
pulumi config set cost_optimization true
```

#### Deploy Advanced Infrastructure
```powershell
# Switch to advanced demo
pulumi up -f advanced_demo.py

# View configuration being used
pulumi config

# Watch deployment progress
pulumi up --yes --logtostderr -v=3
```

#### View Advanced Results
```powershell
# View deployment summary
pulumi stack output advanced_deployment_summary --json | ConvertFrom-Json

# View instance details
pulumi stack output instance_details --json | ConvertFrom-Json

# View load balancer info (if created)
pulumi stack output load_balancer_info --json

# View Pulumi advantages demonstrated
pulumi stack output pulumi_advantages_demonstrated --json
```

#### Test Advanced Features
```powershell
# Test load balancer (if multiple instances)
$lb_url = pulumi stack output load_balancer_info --json | ConvertFrom-Json | Select-Object -ExpandProperty url
if ($lb_url) {
    Write-Host "Load Balancer URL: $lb_url"
    curl $lb_url
}

# Test individual instances
$instances = pulumi stack output instance_details --json | ConvertFrom-Json
foreach ($instance in $instances) {
    Write-Host "Testing instance $($instance.instance_number): $($instance.urls.website)"
    curl $instance.urls.website
}
```

## 🧪 Testing Commands

### Demo 4: Infrastructure Testing

#### Run Tests
```powershell
# Install testing dependencies
pip install pytest requests

# Run all tests with verbose output
python -m pytest test_infrastructure.py -v

# Run tests with detailed output
python -m pytest test_infrastructure.py -v -s

# Run specific test categories
python -m pytest test_infrastructure.py::TestInfrastructureConfiguration -v
python -m pytest test_infrastructure.py::TestPulumiSpecificFeatures -v
```

#### Run Direct Test Script
```powershell
# Run test demonstration directly
python test_infrastructure.py

# Capture output for presentation
python test_infrastructure.py > test_results.txt 2>&1
```

#### Integration Testing (with live infrastructure)
```powershell
# Enable integration tests (uncomment @skip decorator first)
# Edit test_infrastructure.py and remove @unittest.skip from TestLiveInfrastructure
python -m pytest test_infrastructure.py::TestLiveInfrastructure -v
```

## 📦 Import Demo Commands

### Demo 5: Resource Import

#### Prepare for Import Demo
```powershell
# Switch to import demo
pulumi up -f import_demo.py

# This creates some "existing" resources to demonstrate import
```

#### List Existing AWS Resources
```powershell
# List EC2 instances for import
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table

# List VPCs
aws ec2 describe-vpcs --query 'Vpcs[*].[VpcId,CidrBlock,Tags[?Key==`Name`].Value|[0]]' --output table

# List security groups  
aws ec2 describe-security-groups --query 'SecurityGroups[*].[GroupId,GroupName,VpcId]' --output table
```

#### Demonstrate Import Process
```powershell
# Show import commands (don't run these unless you have actual resources)
Write-Host "Import Commands Example:"
Write-Host "pulumi import aws:ec2/instance:Instance imported-instance i-1234567890abcdef0"
Write-Host "pulumi import aws:ec2/vpc:Vpc imported-vpc vpc-12345678"
Write-Host "pulumi import aws:ec2/securityGroup:SecurityGroup imported-sg sg-12345678"

# View import demonstration info
pulumi stack output import_demo_info --json
pulumi stack output import_best_practices --json
```

## 🎛️ Resource Management

### Targeted Updates
```powershell
# Update specific resource only
pulumi up --target urn:pulumi:presentation-demo::webserver::aws:ec2/instance:Instance::webserver-instance

# Preview changes for specific resource
pulumi preview --target urn:pulumi:presentation-demo::webserver::aws:ec2/instance:Instance::webserver-instance
```

### Dependency Management
```powershell
# Generate dependency graph
pulumi stack graph dependency-graph.png

# View resource dependencies
pulumi stack graph --dependency-edge-color blue
```

### Stack Management
```powershell
# View stack history
pulumi history

# View specific deployment
pulumi history --page-size 10

# Show stack info
pulumi stack --show-urns

# Export stack state
pulumi stack export > stack-backup.json

# Import stack state
pulumi stack import < stack-backup.json
```

## 🔍 Troubleshooting Commands

### Debug Information
```powershell
# Verbose logging
pulumi up --logtostderr -v=9

# Debug mode with detailed output
pulumi up --debug

# Dry run with diff
pulumi preview --diff

# Show detailed resource information
pulumi stack --show-secrets
```

### AWS Resource Verification
```powershell
# Check created instances
aws ec2 describe-instances --filters "Name=tag:ManagedBy,Values=Pulumi" --query 'Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress,Tags[?Key==`Name`].Value|[0]]' --output table

# Check VPCs
aws ec2 describe-vpcs --filters "Name=tag:ManagedBy,Values=Pulumi" --output table

# Check security groups
aws ec2 describe-security-groups --filters "Name=tag:ManagedBy,Values=Pulumi" --output table

# Check load balancers
aws elbv2 describe-load-balancers --query 'LoadBalancers[?contains(LoadBalancerName,`advanced`)]' --output table
```

### Common Issue Resolution
```powershell
# Refresh stack state
pulumi refresh

# Force update if stuck
pulumi up --refresh

# Skip pending operations
pulumi cancel

# Clear cached state
pulumi stack export | pulumi stack import --force
```

## 🧹 Cleanup Commands

### Incremental Cleanup
```powershell
# Destroy specific resources first
pulumi destroy --target urn:pulumi:presentation-demo::webserver::aws:ec2/instance:Instance::webserver-instance

# Destroy load balancer components
pulumi destroy --target aws:lb/loadBalancer:LoadBalancer::advanced-alb
```

### Complete Cleanup
```powershell
# Destroy all resources (with confirmation)
pulumi destroy

# Destroy all resources (without confirmation) 
pulumi destroy --yes

# Skip confirmation and force destroy
pulumi destroy --yes --skip-preview
```

### Stack Cleanup  
```powershell
# Remove stack after destroying resources
pulumi stack rm presentation-demo

# Remove stack forcefully
pulumi stack rm presentation-demo --force

# List all stacks to verify cleanup
pulumi stack ls
```

### AWS Manual Cleanup (if needed)
```powershell
# Find any remaining Pulumi resources
aws ec2 describe-instances --filters "Name=tag:ManagedBy,Values=Pulumi" --query 'Reservations[*].Instances[*].InstanceId' --output text

# Terminate any remaining instances
# aws ec2 terminate-instances --instance-ids i-1234567890abcdef0

# Delete VPCs (after all resources are deleted)
# aws ec2 delete-vpc --vpc-id vpc-12345678
```

## 📋 Demo Script Template

### Complete Demo Flow
```powershell
# === PULUMI PRESENTATION DEMO SCRIPT ===

# 1. SETUP
pulumi login --local
pulumi stack init presentation-demo  
pulumi config set aws:region us-east-1

# 2. BASIC DEMO
Write-Host "🚀 Demo 1: Basic Infrastructure"
pulumi preview
pulumi up --yes
pulumi stack output website_url
curl $(pulumi stack output instance_ip)

# 3. COMPONENT DEMO  
Write-Host "🏗️ Demo 2: Component Resources"
pulumi up -f demo_components.py --yes
pulumi stack output deployment_summary --json

# 4. ADVANCED DEMO
Write-Host "⚡ Demo 3: Advanced Features"
pulumi config set environment production
pulumi config set instance_count 3
pulumi up -f advanced_demo.py --yes
pulumi stack output advanced_deployment_summary --json

# 5. TESTING DEMO
Write-Host "🧪 Demo 4: Infrastructure Testing"
python test_infrastructure.py

# 6. IMPORT DEMO
Write-Host "📦 Demo 5: Import Capabilities"  
pulumi up -f import_demo.py --yes
pulumi stack output import_demo_info --json

# 7. CLEANUP
Write-Host "🧹 Cleanup"
pulumi destroy --yes
pulumi stack rm presentation-demo --force
```

## 🎤 Presentation Tips

### Command Preparation
```powershell
# Pre-stage commands in separate terminal windows
# Terminal 1: Basic demo
# Terminal 2: Component demo  
# Terminal 3: Testing demo
# Terminal 4: Import demo

# Use aliases for quick execution
Set-Alias -Name pup -Value "pulumi up --yes"
Set-Alias -Name ppreview -Value "pulumi preview"
Set-Alias -Name pout -Value "pulumi stack output"
```

### Live Demo Best Practices
1. **Pre-validate** all commands work
2. **Have backups** of working configurations
3. **Use fast regions** (us-east-1) for quick deployment
4. **Prepare cleanup scripts** for quick reset
5. **Test internet connectivity** beforehand
6. **Have AWS resources pre-warmed** if possible

### Emergency Fallback
```powershell
# If live demo fails, show pre-captured outputs
Get-Content demo_outputs.json | ConvertFrom-Json | ConvertTo-Json -Depth 10

# Show screenshots of working infrastructure
# Keep browser tabs open with working examples
```

---

**Good luck with your presentation! 🎉**

Remember: Practice the commands beforehand, have backups ready, and focus on the key differentiators that make Pulumi special!