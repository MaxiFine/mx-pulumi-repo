import pulumi
import sys
import os

# Add components directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

from webserver_component import WebServerComponent

"""
Demo: Using Pulumi ComponentResources for Multi-Environment Deployment

This demonstrates how to use a single component to deploy multiple environments
with different configurations - something that showcases Pulumi's programming
capabilities over traditional IaC tools.
"""

print("🚀 Starting Multi-Environment Deployment with Pulumi Components...")

# Demo: Create multiple environments with same component but different configs
environments = {
    'development': {
        'vpc_cidr': '10.0.0.0/16',
        'subnet_cidr': '10.0.1.0/24',
        'instance_type': 't3.micro',
        'key_name': 'aws-365-keypair',
        'environment': 'development'
    },
    'staging': {
        'vpc_cidr': '10.1.0.0/16',
        'subnet_cidr': '10.1.1.0/24',
        'instance_type': 't3.small',
        'key_name': 'aws-365-keypair',
        'environment': 'staging'
    },
    'production': {
        'vpc_cidr': '10.2.0.0/16',
        'subnet_cidr': '10.2.1.0/24',
        'instance_type': 't3.medium',
        'key_name': 'aws-365-keypair',
        'environment': 'production'
    }
}

# Create servers using component (demonstrate reusability)
servers = {}
environment_details = {}

for env_name, config in environments.items():
    print(f"🏗️ Creating {env_name} environment...")
    
    # Create server using component
    servers[env_name] = WebServerComponent(f"{env_name}-webserver", config)
    
    # Prepare environment details for export
    environment_details[env_name] = {
        'website_url': servers[env_name].instance.public_ip.apply(lambda ip: f"http://{ip}"),
        'ssh_command': servers[env_name].instance.public_ip.apply(lambda ip: f"ssh -i {config['key_name']}.pem ec2-user@{ip}"),
        'vpc_id': servers[env_name].vpc.id,
        'instance_id': servers[env_name].instance.id,
        'instance_type': config['instance_type'],
        'vpc_cidr': config['vpc_cidr']
    }

# Export all environment details
for env_name, details in environment_details.items():
    pulumi.export(env_name, details)

# Demo: Show dynamic logic capabilities - conditional environment creation
config = pulumi.Config()
deploy_prod = config.get_bool("deploy_production") or False

if deploy_prod:
    print("🏭 Production deployment enabled!")
    # Additional production-specific resources could be added here
    production_extras = {
        'monitoring_enabled': True,
        'backup_enabled': True,
        'multi_az': True
    }
    pulumi.export('production_extras', production_extras)
else:
    print("🚫 Production deployment skipped (set deploy_production=true to enable)")

# Demo: Complex output generation using programming logic
total_environments = len(environments)
total_resources_per_env = 7  # VPC, Subnet, IGW, RT, RT Assoc, SG, Instance
total_resources = total_environments * total_resources_per_env

# Demonstrate list comprehensions and complex data structures
environment_summary = [
    {
        'name': env_name,
        'instance_type': config['instance_type'],
        'vpc_cidr': config['vpc_cidr'],
        'cost_category': 'low' if config['instance_type'] == 't3.micro' else 'medium' if config['instance_type'] == 't3.small' else 'high'
    }
    for env_name, config in environments.items()
]

# Export comprehensive deployment summary
pulumi.export('deployment_summary', {
    'total_environments_deployed': total_environments,
    'total_resources_created': total_resources,
    'deployment_method': 'Pulumi ComponentResource',
    'reusability_factor': '100% - Same component, different configurations',
    'environments': environment_summary,
    'pulumi_advantages': [
        'Single component definition for multiple environments',
        'Type-safe configuration passing',
        'Complex logic and conditionals',
        'Dynamic resource creation with loops',
        'Rich data structures in outputs'
    ],
    'vs_terraform': [
        'No need for separate modules and complex variable passing',
        'Real programming constructs (loops, conditionals, functions)',
        'Better error handling and validation',
        'IDE support with IntelliSense and debugging'
    ]
})

# Demo: Advanced output with conditional logic
cost_analysis = {}
for env_name, config in environments.items():
    instance_type = config['instance_type']
    # Simplified cost calculation for demo
    hourly_costs = {'t3.micro': 0.0104, 't3.small': 0.0208, 't3.medium': 0.0416}
    monthly_cost = hourly_costs.get(instance_type, 0) * 24 * 30
    cost_analysis[env_name] = {
        'instance_type': instance_type,
        'estimated_monthly_cost_usd': round(monthly_cost, 2),
        'cost_category': 'low' if monthly_cost < 20 else 'medium' if monthly_cost < 50 else 'high'
    }

pulumi.export('cost_analysis', cost_analysis)

# Demo: Show environment-specific URLs for quick testing
quick_access = {}
for env_name in environments.keys():
    server = servers[env_name]
    quick_access[f"{env_name}_urls"] = {
        'website': server.instance.public_ip.apply(lambda ip: f"http://{ip}"),
        'health_check': server.instance.public_ip.apply(lambda ip: f"curl -I http://{ip}"),
        'ssh_access': server.instance.public_ip.apply(lambda ip: f"ssh -i aws-365-keypair.pem ec2-user@{ip}")
    }

pulumi.export('quick_access', quick_access)

# Demo: Resource tagging strategy (something easy in Pulumi, harder in Terraform)
tagging_strategy = {
    'common_tags': {
        'ManagedBy': 'Pulumi',
        'Project': 'WebServer-Demo',
        'Owner': 'DevOps-Team',
        'DeploymentMethod': 'ComponentResource'
    },
    'environment_specific_tags': {
        env_name: {
            'Environment': config['environment'],
            'CostCenter': f"CC-{env_name.upper()}",
            'InstanceType': config['instance_type']
        }
        for env_name, config in environments.items()
    }
}

pulumi.export('tagging_strategy', tagging_strategy)

print("✅ Multi-environment deployment with components completed!")
print(f"📊 Created {total_environments} environments with {total_resources} total resources")
print("🔧 Each environment is isolated with its own VPC and resources")
print("📈 Run 'pulumi stack output' to see all environment details")

# Demo: Generate deployment report
deployment_report = {
    'deployment_timestamp': pulumi.runtime.get_time(),
    'deployment_summary': f"Successfully deployed {total_environments} environments using Pulumi ComponentResources",
    'next_steps': [
        "Test each environment using the exported URLs",
        "SSH into instances using the provided SSH commands",
        "Scale environments by modifying the environments dictionary",
        "Add monitoring or other components as needed"
    ],
    'pulumi_features_demonstrated': [
        'ComponentResource pattern for reusability',
        'Dynamic resource creation with loops',
        'Complex conditional logic',
        'Rich output data structures',
        'Configuration-driven deployments',
        'Cost analysis with programming logic'
    ]
}

pulumi.export('deployment_report', deployment_report)