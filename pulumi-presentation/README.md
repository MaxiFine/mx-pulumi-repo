# Pulumi Infrastructure as Code Presentation Demo

Welcome to the comprehensive Pulumi demo collection for DevOps presentations! This repository contains multiple demonstration files showcasing Pulumi's capabilities and advantages over traditional IaC tools like Terraform.

## 📋 Table of Contents

- [Overview](#overview)
- [Demo Files](#demo-files)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Presentation Structure](#presentation-structure)
- [Demo Commands](#demo-commands)
- [Key Advantages](#key-advantages)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This demo collection demonstrates:

1. **What is Pulumi** - Modern Infrastructure as Code using real programming languages
2. **Why Pulumi** - Developer-friendly approach with familiar tooling
3. **Problem Solving** - Complex infrastructure logic made simple
4. **vs Terraform** - Direct comparison of capabilities and developer experience

## 📁 Demo Files

### Core Demos

| File | Description | Key Features |
|------|-------------|--------------|
| `__main__.py` | Basic infrastructure demo | VPC, EC2, Security Groups, Dynamic AMI |
| `components/webserver_component.py` | Reusable component | ComponentResource pattern, encapsulation |
| `demo_components.py` | Multi-environment deployment | Component reuse, environment-specific configs |
| `test_infrastructure.py` | Infrastructure testing | Unit tests, validation, compliance checks |
| `import_demo.py` | Resource import capabilities | Import existing resources, migration scenarios |
| `advanced_demo.py` | Complex programming features | Loops, conditionals, rich data structures |

### Supporting Files

- `components/__init__.py` - Python package initialization
- `README.md` - This file
- `demo_commands.md` - Comprehensive command reference
- `requirements.txt` - Python dependencies

## 🔧 Prerequisites

### Software Requirements

- **Python 3.7+** - For running Pulumi programs
- **Pulumi CLI** - Install from [pulumi.com](https://www.pulumi.com/docs/get-started/install/)
- **AWS CLI** - Configured with appropriate credentials
- **Git** - For version control

### AWS Setup

1. **AWS Account** with appropriate permissions
2. **AWS CLI configured** with credentials
3. **EC2 Key Pair** named `aws-365-keypair` (or update the key name in code)
4. **Appropriate IAM permissions** for EC2, VPC, Load Balancer resources

### Python Dependencies

```bash
pip install pulumi pulumi-aws requests pytest
```

## 🚀 Quick Start

### 1. Initialize Pulumi

```powershell
# Navigate to the demo directory
cd c:\Users\MaxwellAdomako\amalitech\learning-projects\mx-pulumi-repo\pulumi-presentation

# Login to Pulumi (use local backend for demo)
pulumi login --local

# Create a new stack
pulumi stack init presentation-demo

# Set AWS region
pulumi config set aws:region us-east-1
```

### 2. Run Basic Demo

```powershell
# Preview infrastructure changes
pulumi preview

# Deploy infrastructure
pulumi up

# Check outputs
pulumi stack output
```

### 3. Test the Deployment

```powershell
# Get website URL and test
$website_url = pulumi stack output website_url
curl $website_url

# Get SSH command
pulumi stack output ssh_command
```

## 🎤 Presentation Structure

### Part 1: Introduction (10 minutes)
- What is Pulumi?
- Why choose Pulumi?
- Problems it solves
- Demo: `__main__.py` - Basic infrastructure

### Part 2: Advanced Features (15 minutes)
- Component resources: `demo_components.py`
- Programming constructs: `advanced_demo.py`
- Infrastructure testing: `test_infrastructure.py`

### Part 3: Migration & Import (10 minutes)
- Import existing resources: `import_demo.py`
- Migration strategies
- Comparison with Terraform

### Part 4: Q&A and Discussion (10 minutes)
- Team questions
- Implementation planning
- Next steps

## 🎯 Key Advantages Demonstrated

### Programming Language Benefits
```python
# ✅ Pulumi: Real loops and conditionals
for i in range(instance_count):
    if environment == "production":
        instance_type = "t3.large"
    else:
        instance_type = "t3.micro"
```

```hcl
# ❌ Terraform: Limited logic
count = var.instance_count
# Complex conditionals are difficult in HCL
```

### Rich Data Structures
```python
# ✅ Pulumi: Complex nested structures
environment_config = {
    "dev": {
        "instance_type": "t3.micro",
        "subnets": [
            {"cidr": "10.0.1.0/24", "az": "us-east-1a"},
            {"cidr": "10.0.2.0/24", "az": "us-east-1b"}
        ]
    }
}
```

### Infrastructure Testing
```python
# ✅ Pulumi: Real unit tests
def test_vpc_cidr_configuration(self):
    actual_cidr = "10.0.0.0/16"
    self.assertEqual(actual_cidr, self.expected_vpc_cidr)
```

## 📋 Demo Commands Reference

### Basic Operations
```powershell
# Preview changes
pulumi preview

# Deploy infrastructure  
pulumi up

# View stack outputs
pulumi stack output

# Destroy resources
pulumi destroy
```

### Configuration Management
```powershell
# Set configuration values
pulumi config set environment prod
pulumi config set instance_count 5
pulumi config set enable_monitoring true

# View configuration
pulumi config
```

### Advanced Operations
```powershell
# Target specific resources
pulumi up --target urn:pulumi:presentation-demo::webserver::aws:ec2/instance:Instance::webserver-instance

# Generate dependency graph
pulumi stack graph dependency-graph.png

# View stack history
pulumi history

# Export stack state
pulumi stack export > stack-state.json
```

### Testing Commands
```powershell
# Run infrastructure tests
python test_infrastructure.py

# Run with pytest for better output
python -m pytest test_infrastructure.py -v
```

## 🆚 Pulumi vs Terraform Comparison

| Feature | Pulumi | Terraform |
|---------|--------|-----------|
| **Languages** | Python, TypeScript, Go, C#, Java | HCL (proprietary) |
| **IDE Support** | Full IntelliSense, debugging | Basic syntax highlighting |
| **Testing** | Unit tests, integration tests | Limited validation |
| **Logic** | Real programming constructs | Limited conditional logic |
| **State** | Pulumi Service or self-managed | State files |
| **Learning Curve** | Familiar languages | New DSL to learn |
| **Ecosystem** | NPM, PyPI, etc. | Terraform modules only |

## 🛠️ Troubleshooting

### Common Issues

#### 1. Import Errors
```
Import "pulumi" could not be resolved
```
**Solution**: Install dependencies
```powershell
pip install pulumi pulumi-aws
```

#### 2. AWS Permissions
```
Error: creating EC2 Instance: UnauthorizedOperation
```
**Solution**: Ensure AWS credentials have EC2 permissions

#### 3. Key Pair Not Found
```
Error: The key pair 'aws-365-keypair' does not exist
```
**Solution**: Create key pair or update the key name in code

#### 4. Resource Already Exists
```
Error: A resource with the given name already exists
```
**Solution**: Use different resource names or destroy existing stack

### Debug Commands
```powershell
# Verbose logging
pulumi up --logtostderr -v=9

# Debug mode
pulumi up --debug

# Check AWS resources
aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table
```

## 📚 Additional Resources

### Pulumi Documentation
- [Pulumi Docs](https://www.pulumi.com/docs/)
- [AWS Provider](https://www.pulumi.com/registry/packages/aws/)
- [Component Resources](https://www.pulumi.com/docs/intro/concepts/resources/components/)

### AWS Documentation
- [EC2 User Guide](https://docs.aws.amazon.com/ec2/)
- [VPC User Guide](https://docs.aws.amazon.com/vpc/)
- [IAM Permissions](https://docs.aws.amazon.com/ec2/latest/userguide/iam-policies-for-amazon-ec2.html)

## 🚀 Next Steps After Presentation

1. **Team Training** - Schedule Pulumi workshops
2. **Pilot Project** - Start with non-critical infrastructure
3. **Migration Planning** - Strategy for existing Terraform code
4. **CI/CD Integration** - Implement automated deployments
5. **Best Practices** - Establish coding standards and review processes

## 📝 Presentation Talking Points

### Opening Hook
*"Today we'll see how to manage infrastructure using Python instead of learning yet another domain-specific language. Who here has struggled with Terraform's HCL syntax?"*

### Key Demos to Highlight
1. **Live coding** - Show IDE support with IntelliSense
2. **Error handling** - Compare Pulumi vs Terraform error messages  
3. **Testing** - Run actual unit tests on infrastructure
4. **Reusability** - Deploy multiple environments with one component

### Closing Statement
*"Pulumi brings infrastructure management into the modern development workflow. Same tools, same languages, same testing frameworks - but for your infrastructure."*

---

**Good luck with your presentation! 🎉**

For questions or support, refer to [Pulumi Community](https://slack.pulumi.com/) or [GitHub Issues](https://github.com/pulumi/pulumi/issues).