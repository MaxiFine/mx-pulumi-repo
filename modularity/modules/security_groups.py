"""
Simple Security Groups Module
=============================

Basic security group functions for common use cases.
Easy to understand and reuse!
"""

import pulumi_aws as aws


def create_web_security_group(name: str, vpc_id):
    """
    Create security group for web servers.
    Allows HTTP, HTTPS, and SSH access.
    
    Args:
        name: Name for security group
        vpc_id: VPC ID
    
    Returns:
        Security group resource
    """
    sg = aws.ec2.SecurityGroup(
        f"{name}-web-sg",
        name=f"{name}-web-sg",
        description="Security group for web servers",
        vpc_id=vpc_id,
        
        # Inbound rules
        ingress=[
            # HTTP
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=80,
                to_port=80,
                cidr_blocks=["0.0.0.0/0"]
            ),
            # HTTPS  
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=443,
                to_port=443,
                cidr_blocks=["0.0.0.0/0"]
            ),
            # SSH
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=22,
                to_port=22,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        
        # Outbound rules (allow all)
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol="-1",  # All protocols
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        
        tags={"Name": f"{name}-web-sg", "Type": "Web"}
    )
    
    print(f"Web security group created: {name}-web-sg")
    print("   Allows: HTTP (80), HTTPS (443), SSH (22)")
    return sg


def create_database_security_group(name: str, vpc_id, web_sg_id):
    """
    Create security group for database servers.
    Only allows access from web servers + SSH.
    
    Args:
        name: Name for security group
        vpc_id: VPC ID
        web_sg_id: Web security group ID (for database access)
    
    Returns:
        Security group resource
    """
    sg = aws.ec2.SecurityGroup(
        f"{name}-db-sg",
        name=f"{name}-db-sg",
        description="Security group for database servers",
        vpc_id=vpc_id,
        
        # Inbound rules
        ingress=[
            # MySQL/Aurora from web servers only
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=3306,
                to_port=3306,
                security_groups=[web_sg_id]  # Only from web security group
            ),
            # SSH from anywhere (for admin access)
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=22,
                to_port=22,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        
        # Outbound rules
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol="-1",
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        
        tags={"Name": f"{name}-db-sg", "Type": "Database"}
    )
    
    print(f"Database security group created: {name}-db-sg")
    print("   Allows: MySQL (3306) from web servers, SSH (22)")
    return sg


def create_custom_security_group(name: str, vpc_id, allowed_ports: list, description: str = None):
    """
    Create custom security group with specific ports.
    
    Args:
        name: Name for security group
        vpc_id: VPC ID
        allowed_ports: List of ports to allow (e.g., [80, 443, 22])
        description: Custom description
    
    Returns:
        Security group resource
    """
    # Create ingress rules for each port
    ingress_rules = []
    for port in allowed_ports:
        ingress_rules.append(
            aws.ec2.SecurityGroupIngressArgs(
                protocol="tcp",
                from_port=port,
                to_port=port,
                cidr_blocks=["0.0.0.0/0"]
            )
        )
    
    sg = aws.ec2.SecurityGroup(
        f"{name}-custom-sg",
        name=f"{name}-custom-sg", 
        description=description or f"Custom security group for {name}",
        vpc_id=vpc_id,
        ingress=ingress_rules,
        egress=[
            aws.ec2.SecurityGroupEgressArgs(
                protocol="-1",
                from_port=0,
                to_port=0,
                cidr_blocks=["0.0.0.0/0"]
            )
        ],
        tags={"Name": f"{name}-custom-sg", "Type": "Custom"}
    )
    
    ports_str = ", ".join(str(port) for port in allowed_ports)
    print(f"Custom security group created: {name}-custom-sg")
    print(f"   Allows ports: {ports_str}")
    return sg