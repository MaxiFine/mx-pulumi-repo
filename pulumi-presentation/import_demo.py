import pulumi
import pulumi_aws as aws
import json

"""
Pulumi Resource Import Demonstration

This demonstrates Pulumi's ability to import existing AWS resources into Pulumi management,
similar to Terraform's import functionality but with better integration and error handling.

This is particularly useful for:
1. Migrating from manual AWS Console management to IaC
2. Taking over resources created by other tools
3. Integrating with existing infrastructure
4. Brownfield infrastructure management
"""

def demonstrate_import_process():
    """Show the import process and commands"""
    
    print("="*80)
    print("📦 PULUMI RESOURCE IMPORT DEMONSTRATION")
    print("="*80)
    print("Pulumi can import existing AWS resources just like Terraform!")
    print("But with better error messages and IDE integration.")
    print("-"*80)
    
    import_examples = {
        "EC2 Instance": {
            "description": "Import an existing EC2 instance",
            "command": "pulumi import aws:ec2/instance:Instance my-imported-instance i-1234567890abcdef0",
            "prerequisites": [
                "Find the instance ID in AWS Console or CLI",
                "Ensure you have proper AWS permissions",
                "Have the Pulumi program ready to define the resource"
            ],
            "code_example": '''
# After import command, define the resource in your code:
imported_instance = aws.ec2.Instance("my-imported-instance",
    instance_type="t3.micro",
    ami="ami-0abcdef1234567890",
    key_name="my-keypair",
    vpc_security_group_ids=["sg-12345678"],
    subnet_id="subnet-12345678",
    # Pulumi will sync the state with AWS
    opts=pulumi.ResourceOptions(
        import_="i-1234567890abcdef0"
    )
)'''
        },
        
        "VPC": {
            "description": "Import an existing VPC",
            "command": "pulumi import aws:ec2/vpc:Vpc my-imported-vpc vpc-12345678",
            "prerequisites": [
                "Get VPC ID from AWS Console",
                "Check VPC CIDR block and settings",
                "Plan for dependent resources (subnets, route tables, etc.)"
            ],
            "code_example": '''
# Import VPC and define in code:
imported_vpc = aws.ec2.Vpc("my-imported-vpc",
    cidr_block="172.31.0.0/16",  # Must match existing VPC
    enable_dns_support=True,
    enable_dns_hostnames=True,
    tags={"Name": "My-Imported-VPC"},
    opts=pulumi.ResourceOptions(import_="vpc-12345678")
)'''
        },
        
        "Security Group": {
            "description": "Import an existing security group",
            "command": "pulumi import aws:ec2/securityGroup:SecurityGroup my-imported-sg sg-12345678",
            "prerequisites": [
                "Note security group ID and VPC association",
                "Document existing ingress/egress rules",
                "Check for dependencies from other resources"
            ],
            "code_example": '''
# Import security group:
imported_sg = aws.ec2.SecurityGroup("my-imported-sg",
    name="my-existing-sg",
    description="Imported security group",
    vpc_id="vpc-12345678",  # Must reference correct VPC
    ingress=[
        {
            "from_port": 80,
            "to_port": 80,
            "protocol": "tcp",
            "cidr_blocks": ["0.0.0.0/0"]
        }
    ],
    opts=pulumi.ResourceOptions(import_="sg-12345678")
)'''
        },
        
        "Subnet": {
            "description": "Import an existing subnet",
            "command": "pulumi import aws:ec2/subnet:Subnet my-imported-subnet subnet-12345678",
            "prerequisites": [
                "Get subnet ID and availability zone",
                "Check CIDR block and VPC association",
                "Note public IP assignment settings"
            ],
            "code_example": '''
# Import subnet:
imported_subnet = aws.ec2.Subnet("my-imported-subnet",
    vpc_id="vpc-12345678",
    cidr_block="172.31.1.0/24",  # Must match existing
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    tags={"Name": "Imported-Subnet"},
    opts=pulumi.ResourceOptions(import_="subnet-12345678")
)'''
        }
    }
    
    for resource_type, details in import_examples.items():
        print(f"\n🔄 {resource_type} Import:")
        print(f"   Description: {details['description']}")
        print(f"   Command: {details['command']}")
        print(f"   Prerequisites:")
        for prereq in details['prerequisites']:
            print(f"   • {prereq}")
        print(f"   Code Example:{details['code_example']}")
        print("-" * 60)

def show_import_workflow():
    """Demonstrate the typical import workflow"""
    
    print("\n📋 TYPICAL IMPORT WORKFLOW:")
    print("="*50)
    
    workflow_steps = [
        {
            "step": 1,
            "title": "Identify Resources to Import",
            "actions": [
                "List existing resources in AWS Console",
                "Use AWS CLI: aws ec2 describe-instances",
                "Document resource IDs and configurations",
                "Plan import order (dependencies matter!)"
            ],
            "command": "aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,Tags[?Key==`Name`].Value|[0]]' --output table"
        },
        {
            "step": 2, 
            "title": "Prepare Pulumi Program",
            "actions": [
                "Create Pulumi project if needed",
                "Write resource definitions matching AWS state",
                "Use pulumi preview to check for issues",
                "Prepare for import command"
            ],
            "command": "pulumi new aws-python  # if creating new project"
        },
        {
            "step": 3,
            "title": "Execute Import Commands",
            "actions": [
                "Run pulumi import for each resource",
                "Start with foundational resources (VPC, etc.)",
                "Import dependent resources in correct order",
                "Verify import success"
            ],
            "command": "pulumi import aws:ec2/vpc:Vpc imported-vpc vpc-12345678"
        },
        {
            "step": 4,
            "title": "Sync and Validate",
            "actions": [
                "Run pulumi up to sync state",
                "Check for any configuration drift",
                "Validate resources are managed by Pulumi",
                "Test changes to ensure control"
            ],
            "command": "pulumi up  # Should show no changes if properly imported"
        },
        {
            "step": 5,
            "title": "Manage Going Forward",
            "actions": [
                "Resources now managed by Pulumi",
                "Can modify through code changes",
                "Use pulumi destroy to clean up",
                "Integrate with CI/CD pipelines"
            ],
            "command": "pulumi up  # Apply changes through code"
        }
    ]
    
    for step_info in workflow_steps:
        print(f"\n{step_info['step']}. {step_info['title']}")
        print("-" * 30)
        for action in step_info['actions']:
            print(f"   • {action}")
        print(f"   Command: {step_info['command']}")

def create_import_demo_resources():
    """
    Create some resources to demonstrate import capabilities
    These simulate resources that might exist and need importing
    """
    
    print("\n🏗️ Creating demo resources to simulate import scenario...")
    
    # Create a "pre-existing" VPC that we'll pretend to import
    demo_vpc = aws.ec2.Vpc("demo-existing-vpc",
        cidr_block="172.31.0.0/16",
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags={
            "Name": "Demo-Existing-VPC",
            "Origin": "Simulated-Existing-Resource",
            "Purpose": "Import-Demo",
            "Created": "Manual-Process"  # Simulate manual creation
        }
    )
    
    # Get availability zones
    az = aws.get_availability_zones(state='available')
    
    # Create a "pre-existing" subnet
    demo_subnet = aws.ec2.Subnet("demo-existing-subnet",
        vpc_id=demo_vpc.id,
        cidr_block="172.31.1.0/24",
        availability_zone=az.names[0],
        map_public_ip_on_launch=True,
        tags={
            "Name": "Demo-Existing-Subnet",
            "Origin": "Simulated-Existing-Resource",
            "Purpose": "Import-Demo"
        }
    )
    
    # Create a "pre-existing" security group
    demo_sg = aws.ec2.SecurityGroup("demo-existing-sg",
        name="demo-existing-security-group",
        description="Simulated existing security group for import demo",
        vpc_id=demo_vpc.id,
        ingress=[
            {
                "from_port": 80,
                "to_port": 80,
                "protocol": "tcp",
                "cidr_blocks": ["0.0.0.0/0"],
                "description": "HTTP access"
            },
            {
                "from_port": 22,
                "to_port": 22, 
                "protocol": "tcp",
                "cidr_blocks": ["10.0.0.0/8"],
                "description": "SSH from internal"
            }
        ],
        egress=[{
            "from_port": 0,
            "to_port": 0,
            "protocol": "-1",
            "cidr_blocks": ["0.0.0.0/0"]
        }],
        tags={
            "Name": "Demo-Existing-SG",
            "Origin": "Simulated-Existing-Resource",
            "Purpose": "Import-Demo"
        }
    )
    
    return demo_vpc, demo_subnet, demo_sg

def compare_with_terraform():
    """Compare Pulumi import with Terraform import"""
    
    print("\n🆚 PULUMI VS TERRAFORM IMPORT COMPARISON:")
    print("="*60)
    
    comparison = {
        "Command Syntax": {
            "Pulumi": "pulumi import aws:ec2/instance:Instance my-instance i-12345",
            "Terraform": "terraform import aws_instance.my_instance i-12345",
            "Advantage": "Pulumi uses consistent URN format, Terraform varies by provider"
        },
        "Error Handling": {
            "Pulumi": "Clear error messages with suggestions and type information", 
            "Terraform": "Often cryptic errors, requires deep HCL knowledge",
            "Advantage": "Pulumi provides much better developer experience"
        },
        "IDE Integration": {
            "Pulumi": "Full IDE support, IntelliSense, debugging, refactoring",
            "Terraform": "Limited IDE support, mostly syntax highlighting",
            "Advantage": "Pulumi leverages full programming language ecosystem"
        },
        "State Management": {
            "Pulumi": "Integrated state service or self-managed backend",
            "Terraform": "State files that can be complex to manage",
            "Advantage": "Pulumi state service provides better collaboration features"
        },
        "Validation": {
            "Pulumi": "Compile-time validation, type checking, unit testing",
            "Terraform": "Runtime validation only with plan/apply", 
            "Advantage": "Pulumi catches errors much earlier in development cycle"
        },
        "Bulk Import": {
            "Pulumi": "Can script imports with programming language features",
            "Terraform": "Requires external tools or scripts for bulk operations",
            "Advantage": "Pulumi enables programmatic import workflows"
        }
    }
    
    for aspect, details in comparison.items():
        print(f"\n📊 {aspect}:")
        print(f"   Pulumi: {details['Pulumi']}")  
        print(f"   Terraform: {details['Terraform']}")
        print(f"   🏆 {details['Advantage']}")

# Main demo execution
if __name__ == "__main__":
    
    # Demonstrate the import process
    demonstrate_import_process()
    
    # Show typical workflow
    show_import_workflow()
    
    # Create demo resources
    vpc, subnet, sg = create_import_demo_resources()
    
    # Compare with Terraform
    compare_with_terraform()
    
    # Export information for presentation
    pulumi.export("import_demo_info", {
        "message": "Pulumi Import Capabilities Demonstration",
        "key_advantages": [
            "Better error messages and validation",
            "IDE integration and type safety", 
            "Programmatic import workflows",
            "Integrated state management",
            "Compile-time error detection"
        ],
        "supported_resources": [
            "EC2 Instances, VPCs, Subnets, Security Groups",
            "RDS Databases, S3 Buckets, IAM Roles",
            "Kubernetes resources, Load Balancers", 
            "And hundreds more AWS resources"
        ],
        "import_commands": {
            "vpc": "pulumi import aws:ec2/vpc:Vpc imported-vpc vpc-12345678",
            "instance": "pulumi import aws:ec2/instance:Instance imported-instance i-1234567890abcdef0",
            "security_group": "pulumi import aws:ec2/securityGroup:SecurityGroup imported-sg sg-12345678"
        }
    })
    
    # Export demo resource information
    pulumi.export("demo_resources_for_import", {
        "vpc_id": vpc.id,
        "subnet_id": subnet.id,
        "security_group_id": sg.id,
        "note": "These resources simulate existing infrastructure that could be imported",
        "next_steps": [
            "In a real scenario, these would be existing resources",
            "You would identify their IDs from AWS Console",
            "Then use pulumi import commands to bring them under management",
            "Finally update your code to match the imported state"
        ]
    })
    
    # Best practices for imports
    pulumi.export("import_best_practices", {
        "planning": [
            "Document all existing resources and their relationships",
            "Import foundational resources first (VPCs, IAM roles)", 
            "Plan import order to respect dependencies",
            "Test import process in non-production environment first"
        ],
        "execution": [
            "Start with read-only operations to verify access",
            "Import one resource at a time to isolate issues",
            "Validate each import with pulumi up --dry-run",
            "Keep detailed logs of the import process"
        ],
        "post_import": [
            "Verify no unexpected changes with pulumi preview",
            "Test that you can make safe changes to imported resources",
            "Update documentation to reflect new management approach",
            "Train team on Pulumi workflows for ongoing management"
        ]
    })
    
    print("\n✅ Import demonstration completed!")
    print("🎯 Key takeaways for your presentation:")
    print("   1. Pulumi import is as capable as Terraform import")
    print("   2. Better error messages and IDE support")
    print("   3. Can be scripted and automated")
    print("   4. Integrates with existing development workflows")
    print("   5. Supports all major AWS resources")
    
    print(f"\n📋 Export outputs: Run 'pulumi stack output' to see demo info")
    print("💡 For live demo: Show actual import commands with real resource IDs")