"""
Simple Networking Module
========================

Basic VPC, subnets, and internet gateway functions.
Perfect for new engineers learning Pulumi modules!
"""

import pulumi
import pulumi_aws as aws


def create_vpc(name: str, cidr: str = "10.0.0.0/16"):
    """
    Create a simple VPC with DNS support.
    
    Args:
        name: Name for the VPC
        cidr: CIDR block (default: 10.0.0.0/16)
    
    Returns:
        VPC resource
    """
    vpc = aws.ec2.Vpc(
        f"{name}-vpc",
        cidr_block=cidr,
        enable_dns_hostnames=True,
        enable_dns_support=True,
        tags={"Name": f"{name}-vpc"}
    )
    
    print(f"✅ VPC created: {name}-vpc ({cidr})")
    return vpc


def create_internet_gateway(name: str, vpc_id):
    """
    Create Internet Gateway and attach to VPC.
    
    Args:
        name: Name prefix
        vpc_id: VPC ID to attach to
    
    Returns:
        Internet Gateway resource
    """
    igw = aws.ec2.InternetGateway(
        f"{name}-igw",
        vpc_id=vpc_id,
        tags={"Name": f"{name}-igw"}
    )
    
    print(f"✅ Internet Gateway created: {name}-igw")
    return igw


def create_public_subnet(name: str, vpc_id, cidr: str, az: str):
    """
    Create a public subnet (with auto-assign public IP).
    
    Args:
        name: Subnet name
        vpc_id: VPC ID
        cidr: Subnet CIDR block
        az: Availability zone
    
    Returns:
        Subnet resource
    """
    subnet = aws.ec2.Subnet(
        f"{name}-public",
        vpc_id=vpc_id,
        cidr_block=cidr,
        availability_zone=az,
        map_public_ip_on_launch=True,  # Makes it public
        tags={
            "Name": f"{name}-public",
            "Type": "Public"
        }
    )
    
    print(f"✅ Public subnet created: {name}-public ({cidr})")
    return subnet


def create_private_subnet(name: str, vpc_id, cidr: str, az: str):
    """
    Create a private subnet (no public IP).
    
    Args:
        name: Subnet name
        vpc_id: VPC ID
        cidr: Subnet CIDR block  
        az: Availability zone
    
    Returns:
        Subnet resource
    """
    subnet = aws.ec2.Subnet(
        f"{name}-private",
        vpc_id=vpc_id,
        cidr_block=cidr,
        availability_zone=az,
        map_public_ip_on_launch=False,  # Keeps it private
        tags={
            "Name": f"{name}-private",
            "Type": "Private"
        }
    )
    
    print(f"✅ Private subnet created: {name}-private ({cidr})")
    return subnet


def setup_public_routing(name: str, vpc_id, igw_id, subnet_id):
    """
    Setup routing for public subnet to internet.
    
    Args:
        name: Name prefix
        vpc_id: VPC ID
        igw_id: Internet Gateway ID
        subnet_id: Public subnet ID
    """
    # Create route table
    route_table = aws.ec2.RouteTable(
        f"{name}-public-rt",
        vpc_id=vpc_id,
        tags={"Name": f"{name}-public-rt"}
    )
    
    # Add route to internet
    aws.ec2.Route(
        f"{name}-internet-route",
        route_table_id=route_table.id,
        destination_cidr_block="0.0.0.0/0",
        gateway_id=igw_id
    )
    
    # Associate with subnet
    aws.ec2.RouteTableAssociation(
        f"{name}-public-rta",
        subnet_id=subnet_id,
        route_table_id=route_table.id
    )
    
    print(f"✅ Public routing setup: {name}-public-rt")
    return route_table