# 🚀 Pulumi Core Concepts Demo - Simple Guide

Welcome! This guide will help you run the Pulumi demo step-by-step, even if you're completely new to Pulumi.

## 🎯 What This Demo Shows

This demo teaches you Pulumi's 5 core concepts through hands-on examples:
1. **Stacks** - Manage multiple environments (dev, staging, prod)
2. **Resources** - Create cloud infrastructure components
3. **Configuration** - Handle secrets and parameters
4. **State** - Track infrastructure changes
5. **Preview & Update** - Deploy safely

## 📋 Prerequisites (What You Need)

Before starting, make sure you have:

### ✅ Required Software
- **Python 3.8+** installed
- **Pulumi CLI** installed ([Download here](https://www.pulumi.com/docs/get-started/install/))
- **AWS CLI** configured with credentials
- **Git** (optional, for cloning)

### ✅ AWS Setup
- AWS account with programmatic access
- AWS CLI configured: `aws configure`
- Sufficient permissions to create EC2, VPC, S3 resources

### ✅ Check Your Setup
```bash
python --version          # Should show 3.8 or higher
pulumi version           # Should show Pulumi CLI version
aws sts get-caller-identity  # Should show your AWS account
```

## 🚀 Quick Start (5 Minutes)

### Step 1: Navigate to Demo Directory
```bash
cd c:\Users\MaxwellAdomako\amalitech\learning-projects\mx-pulumi-repo\demo
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Your First Stack
```bash
# Create a development environment stack
pulumi stack init dev

# Set your AWS region
pulumi config set aws:region us-east-1
```

### Step 4: Deploy Your First Infrastructure
```bash
# Preview what will be created (safe - doesn't create anything yet)
pulumi preview

# Deploy the infrastructure (creates real AWS resources)
pulumi up
```

### Step 5: See Your Results
```bash
# View the outputs (including website URL)
pulumi stack output

# Visit the website URL shown in the output
```

### Step 6: Clean Up (Important!)
```bash
# Destroy the resources to avoid AWS charges
pulumi destroy

# Confirm by typing "yes"
```

## 📚 Running All 5 Core Concept Demos

The demo directory contains 5 different demonstrations. Here's how to run each one:

### 🏗️ Demo 1: STACKS (Currently Active)
**What it shows:** Same code managing different environments

```bash
# Already loaded in __main__.py
pulumi stack init dev
pulumi up

# Create staging environment
pulumi stack init staging
pulumi up

# Create production environment  
pulumi stack init prod
pulumi up

# Switch between environments
pulumi stack select dev
pulumi stack output
```

### 🔧 Demo 2: RESOURCES
**What it shows:** Different types of cloud resources and dependencies

```bash
# Switch to resources demo
copy 02_resources_demo.py __main__.py

# Deploy
pulumi up

# See all the different resources created
pulumi stack output
```

### ⚙️ Demo 3: CONFIGURATION
**What it shows:** Configuration management and secrets

```bash
# Switch to configuration demo
copy 03_configuration_demo.py __main__.py

# Set up configuration
pulumi config set app_name "MyDemoApp"
pulumi config set instance_count 2
pulumi config set --secret db_password "super-secret-password"

# Set environment variable (Windows PowerShell)
$env:ENVIRONMENT = "demo"

# Deploy
pulumi up

# View configuration
pulumi config
```

### 📊 Demo 4: STATE
**What it shows:** How Pulumi tracks infrastructure changes

```bash
# Switch to state demo
copy 04_state_demo.py __main__.py

# Deploy
pulumi up

# View current state
pulumi stack export

# Try making manual changes in AWS Console, then:
pulumi refresh    # Detect changes
pulumi up        # Restore desired state
```

### 🔄 Demo 5: PREVIEW & UPDATE
**What it shows:** Safe deployment workflow

```bash
# Switch to preview/update demo
copy 05_preview_update_demo.py __main__.py

# Start with version 1.0
pulumi config set deployment_version "1.0"
pulumi preview    # See what will be created
pulumi up        # Deploy

# Upgrade to version 2.0 (adds SSH)
pulumi config set deployment_version "2.0"  
pulumi preview    # See what will change
pulumi up        # Apply changes

# Upgrade to version 3.0 (adds HTTPS)
pulumi config set deployment_version "3.0"
pulumi preview    # See what will change
pulumi up        # Apply changes

# View deployment history
pulumi history
```

## 🆘 Troubleshooting

### Problem: "pulumi: command not found"
**Solution:** Install Pulumi CLI
```bash
# Windows (PowerShell as Administrator)
choco install pulumi

# Or download from: https://www.pulumi.com/docs/get-started/install/
```

### Problem: "No valid credential sources found"
**Solution:** Configure AWS credentials
```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, Region, and Output format
```

### Problem: "ModuleNotFoundError: No module named 'pulumi_aws'"
**Solution:** Install Python dependencies
```bash
pip install -r requirements.txt
```

### Problem: "Stack already exists"
**Solution:** Use existing stack or create with different name
```bash
# List existing stacks
pulumi stack ls

# Select existing stack
pulumi stack select existing-stack-name

# Or create with different name
pulumi stack init my-unique-stack-name
```

### Problem: Resources still exist after `pulumi destroy`
**Solution:** Force cleanup
```bash
# Try destroy again
pulumi destroy --yes

# If still stuck, manually delete in AWS Console, then:
pulumi refresh
pulumi destroy --yes
```

## 💰 Cost Information

These demos use minimal AWS resources:
- **EC2 t2.micro instances** (~$0.012/hour)
- **VPCs, Subnets, Security Groups** (Free)
- **S3 buckets** (Free tier: 5GB storage)

**Estimated cost per demo:** Less than $0.05/hour

**Important:** Always run `pulumi destroy` after each demo to avoid ongoing charges!

## 🎯 Next Steps After Demos

1. **Understand the concepts** - Each demo has a web interface explaining what it does
2. **Try modifications** - Change configuration values and see what happens
3. **Explore outputs** - Use `pulumi stack output` to see resource details
4. **Check AWS Console** - See your resources in the AWS web interface
5. **Move to Best Practices** - After core concepts, explore production patterns

## 📞 Need Help?

- **Pulumi Documentation:** https://www.pulumi.com/docs/
- **AWS Free Tier:** https://aws.amazon.com/free/
- **Pulumi Community:** https://slack.pulumi.com/

## 🏁 Success Checklist

After completing all demos, you should understand:
- ✅ How to manage multiple environments with stacks
- ✅ How Pulumi creates and manages cloud resources
- ✅ How to handle configuration and secrets securely
- ✅ How Pulumi tracks infrastructure state
- ✅ How to deploy changes safely with preview/update

**Congratulations! You're now ready to use Pulumi for Infrastructure as Code!** 🎉

---

**Remember:** Each demo creates real AWS resources. Always clean up with `pulumi destroy` to avoid charges!