# """An AWS Python Pulumi program"""

# import pulumi
# from pulumi_aws import s3

# # Create an AWS resource (S3 Bucket)
# bucket = s3.Bucket('my-bucket')

# # Export the name of the bucket
# pulumi.export('bucket_name', bucket.id)

import pulumi
import pulumi_aws as aws
from pulumi import export

size = 't2.micro'
ami = aws.ec2.get_ami(most_recent="true",
                  owners=["137112412989"],
                  filters=[{"name":"name","values":["amzn2-ami-hvm-*"]}])

group = aws.ec2.SecurityGroup('sec-group',
    description='Enable HTTP access and SSH access',
    ingress=[
        { 'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0'] },
        { 'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0'] }
    ])

server = aws.ec2.Instance('ec2-webserver',
    instance_type=size,
    vpc_security_group_ids=[group.id], # reference security group from above
    ami=ami.id)

# pulumi.export('publicIp', server.public_ip)
# pulumi.export('publicIp', server.public_ip)
export('publicHostName', server.public_dns)
export('instanceId', server.id)
export('publicIp', server.public_ip)