import pulumi
import pulumi_aws as aws
# from pulumi import export

# Pulumi VPC Components
vpc = aws.ec2.Vpc('vpc',
    cidr_block='10.0.0.0/16',
    enable_dns_support=True,
    enable_dns_hostnames=True)

# Pulumi Subnet Components
public_subnet = aws.ec2.Subnet('public-subnet',
    vpc_id=vpc.id,
    cidr_block='10.0.1.0/24',
    availability_zone='us-west-1a',
    tags = {
        'Name': 'public-subnet',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
    )

# Pulumi Internet gateway
igw = aws.ec2.InternetGateway('igw',
    vpc_id=vpc.id,
    tags = {
        'Name': 'igw',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Pulumi Route Table
public_route_table = aws.ec2.RouteTable('public-route-table',
    vpc_id=vpc.id,
    routes=[
        {
            'cidr_block': '0.0.0.0/0',
            'gateway_id': igw.id
        }
    ],
    tags={
        'Name': 'public-route-table',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Route Table Association
public_route_table_association = aws.ec2.RouteTableAssociation(
    'public-route-table-association',
    subnet_id=public_subnet.id,
    route_table_id=public_route_table.id
)

# Pulumi Security Group
security_group = aws.ec2.SecurityGroup(
    'public-security-group',
    description='Enable HTTP access',
    vpc_id=vpc.id,
    ingress=[
        {
            'from_port': 80,
            'to_port': 80,
            'protocol': 'tcp',
            'cidr_blocks': ['0.0.0.0/0']
        }
    ],
    egress=[
        {
            'from_port': 0,
            'to_port': 0,
            'protocol': '-1',
            'cidr_blocks': ['0.0.0.0/0']
        }
    ],
    tags={
        'Name': 'public-security-group',
        'Environment': 'dev',
        'owner': 'mx-devops'
    }
)

# Pulumi EC2 Instance
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {
            "name": "name",
            # "values": ["amzn2-ami-hvm-*-x86_64-gp2"]
            "values": ["amzn2-ami-hvm-*"]
        }
    ]
)

user_data = """

        #!/bin/bash
echo "Hello, world!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

ec2_instance = aws.ec2.Instance(
    'webserver-instance',
    instance_type='t2.micro',
    vpc_security_group_ids=[security_group.id],
    ami=ami.id,
    user_data=user_data,
    subnet_id=public_subnet.id,
    associate_public_ip_address=True,
    # public_route_table_association=public_route_table_association.id
    
    )

pulumi.export('instance_ip', ec2_instance.public_ip)
pulumi.export('security_group_id', security_group.id)
pulumi.export('vpc_id', vpc.id)
pulumi.export('subnet_id', public_subnet.id)
pulumi.export('route_table_id', public_route_table.id)
pulumi.export('igw_id', igw.id)
pulumi.export('instance_ami', ami.id)
