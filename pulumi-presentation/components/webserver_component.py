import pulumi
import pulumi_aws as aws

class WebServerComponent(pulumi.ComponentResource):
    """
    A reusable web server component that creates:
    - VPC with public subnet
    - Internet Gateway and routing
    - Security group with HTTP, HTTPS, and SSH access
    - EC2 instance with a web server
    
    This demonstrates Pulumi's component resource pattern for reusable infrastructure.
    """
    
    def __init__(self, name, args=None, opts=None):
        super().__init__('custom:WebServer', name, None, opts)
        
        if args is None:
            args = {}
        
        print(f"🏗️ Creating WebServer component: {name}")
        
        # Get dynamic AZs
        availability_zones = aws.get_availability_zones(state='available')
        selected_az = availability_zones.names[0]
        
        # Create VPC
        self.vpc = aws.ec2.Vpc(f'{name}-vpc',
            cidr_block=args.get('vpc_cidr', '10.0.0.0/16'),
            enable_dns_support=True,
            enable_dns_hostnames=True,
            tags={
                'Name': f'{name}-vpc',
                'Component': 'WebServer',
                'ManagedBy': 'Pulumi',
                'Environment': args.get('environment', 'demo')
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Create public subnet
        self.public_subnet = aws.ec2.Subnet(f'{name}-public-subnet',
            vpc_id=self.vpc.id,
            cidr_block=args.get('subnet_cidr', '10.0.1.0/24'),
            availability_zone=selected_az,
            map_public_ip_on_launch=True,
            tags={
                'Name': f'{name}-public-subnet',
                'Component': 'WebServer',
                'Environment': args.get('environment', 'demo')
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Create internet gateway
        self.igw = aws.ec2.InternetGateway(f'{name}-igw',
            vpc_id=self.vpc.id,
            tags={
                'Name': f'{name}-igw',
                'Component': 'WebServer',
                'Environment': args.get('environment', 'demo')
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Create route table
        self.route_table = aws.ec2.RouteTable(f'{name}-rt',
            vpc_id=self.vpc.id,
            routes=[{
                'cidr_block': '0.0.0.0/0',
                'gateway_id': self.igw.id
            }],
            tags={
                'Name': f'{name}-route-table',
                'Component': 'WebServer',
                'Environment': args.get('environment', 'demo')
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Associate route table with subnet
        self.rt_association = aws.ec2.RouteTableAssociation(f'{name}-rt-assoc',
            subnet_id=self.public_subnet.id,
            route_table_id=self.route_table.id,
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Create security group
        self.security_group = aws.ec2.SecurityGroup(f'{name}-sg',
            description=f'Security group for {name} web server',
            vpc_id=self.vpc.id,
            ingress=[
                {
                    'from_port': 80,
                    'to_port': 80,
                    'protocol': 'tcp',
                    'cidr_blocks': ['0.0.0.0/0'],
                    'description': 'HTTP access'
                },
                {
                    'from_port': 443,
                    'to_port': 443,
                    'protocol': 'tcp',
                    'cidr_blocks': ['0.0.0.0/0'],
                    'description': 'HTTPS access'
                },
                {
                    'from_port': 22,
                    'to_port': 22,
                    'protocol': 'tcp',
                    'cidr_blocks': ['0.0.0.0/0'],
                    'description': 'SSH access'
                }
            ],
            egress=[{
                'from_port': 0,
                'to_port': 0,
                'protocol': '-1',
                'cidr_blocks': ['0.0.0.0/0']
            }],
            tags={
                'Name': f'{name}-security-group',
                'Component': 'WebServer',
                'Environment': args.get('environment', 'demo')
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Get latest AMI
        ami = aws.ec2.get_ami(
            most_recent=True,
            owners=["amazon"],
            filters=[{
                "name": "name",
                "values": ["amzn2-ami-hvm-*"]
            }]
        )
        
        # Create EC2 instance
        self.instance = aws.ec2.Instance(f'{name}-instance',
            instance_type=args.get('instance_type', 't3.micro'),
            ami=ami.id,
            key_name=args.get('key_name', 'aws-365-keypair'),
            security_groups=[self.security_group.id],
            subnet_id=self.public_subnet.id,
            associate_public_ip_address=True,
            user_data=self._get_user_data(name, args.get('environment', 'demo')),
            tags={
                'Name': f'{name}-instance',
                'Component': 'WebServer',
                'Environment': args.get('environment', 'demo'),
                'CreatedBy': 'Pulumi-Component'
            },
            opts=pulumi.ResourceOptions(parent=self)
        )
        
        # Register outputs that can be accessed from the component
        self.register_outputs({
            'vpc_id': self.vpc.id,
            'subnet_id': self.public_subnet.id,
            'instance_id': self.instance.id,
            'public_ip': self.instance.public_ip,
            'website_url': pulumi.Output.concat("http://", self.instance.public_ip),
            'ssh_command': pulumi.Output.concat("ssh -i ", args.get('key_name', 'aws-365-keypair'), ".pem ec2-user@", self.instance.public_ip),
            'security_group_id': self.security_group.id
        })
        
        print(f"✅ WebServer component {name} created successfully!")
    
    def _get_user_data(self, name, environment):
        """Generate user data script for the instance"""
        return f"""#!/bin/bash
yum update -y
yum install -y httpd
systemctl start httpd
systemctl enable httpd

cat <<EOF > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
    <title>Pulumi Component Demo - {name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .container {{ 
            max-width: 800px;
            width: 100%;
            background: rgba(255,255,255,0.1); 
            padding: 40px; 
            border-radius: 20px; 
            backdrop-filter: blur(15px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.2);
        }}
        h1 {{ 
            color: #fdcb6e; 
            text-align: center; 
            font-size: 2.5rem;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 2rem 0;
        }}
        .info {{ 
            background: rgba(255,255,255,0.15); 
            padding: 25px; 
            border-radius: 15px; 
            border-left: 4px solid #fdcb6e;
            border: 1px solid rgba(255,255,255,0.2);
            transition: transform 0.3s ease;
        }}
        .info:hover {{
            transform: translateY(-5px);
        }}
        .info h3 {{
            color: #fdcb6e;
            margin-bottom: 15px;
            font-size: 1.2rem;
        }}
        .highlight {{ 
            color: #fdcb6e; 
            font-weight: bold; 
        }}
        .feature-list {{
            list-style: none;
            padding: 0;
        }}
        .feature-list li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        .feature-list li:last-child {{
            border-bottom: none;
        }}
        .status-banner {{
            text-align: center;
            font-size: 1.2rem;
            margin-top: 2rem;
            padding: 20px;
            background: linear-gradient(45deg, rgba(0,255,0,0.2), rgba(0,200,0,0.3));
            border-radius: 15px;
            border: 2px solid rgba(0,255,0,0.4);
        }}
        .component-badge {{
            display: inline-block;
            background: rgba(253,203,110,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.9rem;
            border: 1px solid rgba(253,203,110,0.3);
            margin: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 Pulumi Component Demo</h1>
        <div style="text-align: center; margin-bottom: 2rem;">
            <span class="component-badge">Component: {name}</span>
            <span class="component-badge">Environment: {environment}</span>
        </div>
        
        <div class="info-grid">
            <div class="info">
                <h3>🏗️ Component Details</h3>
                <p><span class="highlight">Component Name:</span> {name}</p>
                <p><span class="highlight">Type:</span> WebServerComponent</p>
                <p><span class="highlight">Environment:</span> {environment}</p>
                <p><span class="highlight">Managed By:</span> Pulumi ComponentResource</p>
                <p><span class="highlight">Instance Type:</span> $(curl -s http://169.254.169.254/latest/meta-data/instance-type)</p>
                <p><span class="highlight">Deployment Time:</span> $(date)</p>
            </div>
            
            <div class="info">
                <h3>🌐 Network Information</h3>
                <p><span class="highlight">Public IP:</span> $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)</p>
                <p><span class="highlight">Private IP:</span> $(curl -s http://169.254.169.254/latest/meta-data/local-ipv4)</p>
                <p><span class="highlight">AZ:</span> $(curl -s http://169.254.169.254/latest/meta-data/placement/availability-zone)</p>
                <p><span class="highlight">Instance ID:</span> $(curl -s http://169.254.169.254/latest/meta-data/instance-id)</p>
            </div>
        </div>
        
        <div class="info">
            <h3>✅ Infrastructure Resources Created</h3>
            <ul class="feature-list">
                <li>🌐 Custom VPC with DNS support</li>
                <li>🏠 Public subnet with auto-assign public IP</li>
                <li>🚪 Internet Gateway for external access</li>
                <li>🛣️ Route table with default route</li>
                <li>🔒 Security group (HTTP, HTTPS, SSH)</li>
                <li>🖥️ EC2 instance with Apache HTTP server</li>
                <li>🎯 All resources properly tagged and organized</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🚀 Component Benefits</h3>
            <ul class="feature-list">
                <li>🔄 <strong>Reusable:</strong> Deploy multiple environments easily</li>
                <li>🏗️ <strong>Encapsulated:</strong> Best practices built-in</li>
                <li>📦 <strong>Shareable:</strong> Can be packaged and distributed</li>
                <li>🛡️ <strong>Consistent:</strong> Same pattern every time</li>
                <li>⚡ <strong>Configurable:</strong> Customize via parameters</li>
                <li>🧪 <strong>Testable:</strong> Unit test the component logic</li>
            </ul>
        </div>
        
        <div class="status-banner">
            <strong>🎉 Component Deployed Successfully!</strong><br>
            <em>This infrastructure was created using a Pulumi ComponentResource 🚀</em>
        </div>
    </div>
</body>
</html>
EOF

chown apache:apache /var/www/html/index.html
"""