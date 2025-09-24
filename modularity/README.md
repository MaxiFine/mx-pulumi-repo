# 📦 Simple Pulumi Modules Demo

## 🎯 For New Engineers Learning Pulumi

This project shows **how to organize your Pulumi code into simple, reusable modules**. Perfect for engineers new to Infrastructure as Code!

## 🧩 Why Use Modules?

Instead of putting everything in one big file:
```python
# ❌ Everything in one file - hard to manage
vpc = aws.ec2.Vpc("vpc", cidr_block="10.0.0.0/16")
subnet = aws.ec2.Subnet("subnet", vpc_id=vpc.id, cidr_block="10.0.1.0/24")
sg = aws.ec2.SecurityGroup("sg", vpc_id=vpc.id, ingress=[...])
instance = aws.ec2.Instance("instance", subnet_id=subnet.id, ...)
# 100+ more lines...
```

We split it into logical modules:
```python
# ✅ Organized into modules - easy to understand
from modules import networking, security_groups, compute

vpc = networking.create_vpc("my-project")
web_sg = security_groups.create_web_security_group("my-project", vpc.id)
web_server = compute.create_web_server("web-1", subnet.id, web_sg.id)
```

## 📁 Simple Project Structure

```
modularity/
├── __main__.py              # Main deployment file
├── Pulumi.yaml             # Project configuration
├── README.md               # This file
└── modules/                # Our reusable modules
    ├── networking.py       # VPC, subnets, internet gateway
    ├── security_groups.py  # Security group functions
    └── compute.py          # EC2 instance functions
```

## 🔧 Module Overview

### 1. **Networking Module** (`modules/networking.py`)
Simple functions for network setup:
- `create_vpc()` - Creates VPC with DNS support
- `create_public_subnet()` - Creates subnet with public IPs
- `create_private_subnet()` - Creates private subnet
- `setup_public_routing()` - Adds internet access

### 2. **Security Groups Module** (`modules/security_groups.py`)
Common security group patterns:
- `create_web_security_group()` - Allows HTTP, HTTPS, SSH
- `create_database_security_group()` - MySQL access from web servers only
- `create_custom_security_group()` - Custom ports

### 3. **Compute Module** (`modules/compute.py`)
Server creation functions:
- `create_web_server()` - Apache web server with demo page
- `create_database_server()` - MySQL database server
- `create_multiple_instances()` - Multiple servers for scaling

## 🚀 How to Use

### Quick Start
```bash
cd modularity
pip install -r requirements.txt
pulumi stack init dev
pulumi up
```

### Different Environments (Same Code!)

**Development** (1 server):
```bash
pulumi stack init dev
pulumi up
# Creates: 1 web server only
```

**Staging** (2 servers + database):
```bash
pulumi stack init staging
pulumi up  
# Creates: 2 web servers + 1 database
```

**Production** (3 servers + database):
```bash
pulumi stack init prod
pulumi up
# Creates: 3 web servers + 1 database
```

## 💡 Key Learning Points

### ✅ **Module Benefits**
1. **Organization** - Each module handles one concern
2. **Reusability** - Use same functions across projects
3. **Simplicity** - Easy functions, not complex classes
4. **Teamwork** - Different people can work on different modules

### ✅ **Same Code, Different Results**
The magic happens in `__main__.py`:
```python
if stack_name == "dev":
    # Create 1 server
    web_server = compute.create_web_server(...)
elif stack_name == "prod":
    # Create 3 servers  
    web_servers = compute.create_multiple_instances(..., count=3)
```

### ✅ **Real Programming Benefits**
- **Functions** - Reuse code easily
- **Variables** - Store and reuse values  
- **Loops** - Create multiple resources
- **Conditions** - Different logic per environment
- **Comments** - Document your infrastructure

## 🎮 Live Demo Script

### 1. **Show the Problem**
*"Imagine all your infrastructure in one 500-line file... 😱"*

### 2. **Show the Solution**
```bash
# Show clean module structure
ls modules/
cat modules/networking.py  # Simple, focused functions
```

### 3. **Deploy Different Environments**
```bash
# Same code, different results!
pulumi stack init dev
pulumi up -y        # 1 server

pulumi stack init prod  
pulumi up -y        # 3 servers + database

pulumi stack ls     # Show both stacks
```

### 4. **Show Running Infrastructure**
```bash
pulumi stack output web_url    # Dev URL
pulumi stack select prod
pulumi stack output web_urls   # Prod URLs (multiple)
```

## 🆚 Before vs After

| **Before Modules** | **After Modules** |
|-------------------|------------------|
| 1 giant file | 3 focused files |
| Copy/paste code | Reuse functions |
| Hard to find things | Organized by purpose |
| Scary to change | Safe to modify |
| One person working | Team can collaborate |

## 🔍 What Each Stack Shows

- **Dev Stack**: Minimal setup (1 server) for development
- **Staging Stack**: Multi-tier (2 servers + DB) for testing  
- **Prod Stack**: High availability (3 servers + DB) for production

**Same modules, different configurations!** 🎯

## 🎤 Presentation Talking Points

### **Opening**
*"Who has seen a 500-line CloudFormation template? 🙋‍♂️ Let's fix that with modules!"*

### **Key Messages**
1. **"Organization Matters"** - Show messy vs clean code
2. **"Reuse Everything"** - Same function used multiple times
3. **"Easy to Understand"** - New team members can contribute quickly
4. **"Python Power"** - Real programming language benefits

### **Demo Flow**
1. Show messy single-file approach (2 minutes)
2. Show organized module structure (2 minutes)
3. Deploy dev environment (1 minute)
4. Switch to prod stack and deploy (2 minutes)
5. Compare results - same code, different infrastructure! (1 minute)

## 🛠️ For Your Team

After this demo, your team can:
- ✅ Organize infrastructure code logically  
- ✅ Reuse components across projects
- ✅ Work on different modules simultaneously
- ✅ Understand and modify infrastructure easily

## 💫 Next Steps

1. **Try It**: Deploy the dev stack and explore the code
2. **Modify It**: Add your own functions to modules  
3. **Extend It**: Create modules for databases, load balancers, etc.
4. **Use It**: Apply this pattern to your real infrastructure

---

## 🎓 Perfect for Learning

This demo is designed specifically for engineers who are:
- 🆕 New to Pulumi
- 🔰 Learning Infrastructure as Code
- 🤝 Working in teams
- 📚 Want to understand best practices

**No complex classes or advanced patterns - just simple, useful functions!** ✨

---

*Built with ❤️ for new engineers learning Pulumi*