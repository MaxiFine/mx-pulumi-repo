"""
HOW TO RUN THE CORE CONCEPTS DEMOS
==================================

Each demo demonstrates a specific Pulumi core concept. Run them individually
by copying the demo file to __main__.py or running them directly.

SETUP:
======
1. cd demo
2. Copy one of the demo files to __main__.py
3. Run the appropriate setup commands
4. Run: pulumi up

DEMO 1: STACKS - Environment-specific deployments
=================================================
File: 01_stacks_demo.py
Purpose: Show how same code manages multiple environments

Commands:
1. cp 01_stacks_demo.py __main__.py
2. pulumi stack init dev
3. pulumi config set aws:region us-east-1  
4. pulumi up
5. pulumi stack init staging
6. pulumi up
7. pulumi stack init prod  
8. pulumi up
9. pulumi stack select dev (switch between stacks)

Key Points:
- Same code, different configurations per stack
- Environment isolation through stacks
- Independent state management
- Easy environment promotion

DEMO 2: RESOURCES - Cloud infrastructure components
===================================================  
File: 02_resources_demo.py
Purpose: Show different resource types and dependencies

Commands:
1. cp 02_resources_demo.py __main__.py
2. pulumi up
3. pulumi stack output (see resource information)

Key Points:
- Physical resources (VPC, EC2, S3)
- Logical resources (Security Groups, Route Tables)
- Data sources (AMI lookup, AZ lookup)
- Automatic dependency management

DEMO 3: CONFIGURATION - Secrets, parameters, environment variables
==================================================================
File: 03_configuration_demo.py  
Purpose: Show configuration management and secrets

Commands:
1. cp 03_configuration_demo.py __main__.py
2. pulumi config set app_name "MyDemoApp"
3. pulumi config set instance_count 2
4. pulumi config set enable_https true
5. pulumi config set --secret db_password "super-secret-password"
6. pulumi config set --secret api_key "secret-api-key-12345"  
7. set ENVIRONMENT=demo (Windows) or export ENVIRONMENT="demo" (Linux/Mac)
8. pulumi up
9. pulumi config (view configuration)

Key Points:
- Required vs optional configuration
- Type conversion (string, int, bool)
- Encrypted secrets management
- Environment variable integration
- Configuration-driven infrastructure

DEMO 4: STATE - How Pulumi tracks infrastructure changes
========================================================
File: 04_state_demo.py
Purpose: Show state management and change tracking

Commands:
1. cp 04_state_demo.py __main__.py
2. pulumi up
3. pulumi stack export (see current state)
4. pulumi stack --show-urns (see resource URNs)
5. Manually change something in AWS Console
6. pulumi refresh (detect drift)
7. pulumi up (restore desired state)

Key Points:
- State tracks all resources
- Drift detection capabilities  
- Resource import functionality
- State export/import for backup
- Dependency tracking

DEMO 5: PREVIEW & UPDATE - Safe deployment workflow
===================================================
File: 05_preview_update_demo.py
Purpose: Show safe deployment practices

Commands:
1. cp 05_preview_update_demo.py __main__.py
2. pulumi config set deployment_version "1.0"
3. pulumi preview (see what will be created)
4. pulumi up (deploy safely)
5. pulumi config set deployment_version "2.0"  
6. pulumi preview (see SSH rule will be added)
7. pulumi up (apply changes)
8. pulumi config set deployment_version "3.0"
9. pulumi preview (see HTTPS rule will be added)
10. pulumi up (apply changes)
11. pulumi history (see deployment history)

Key Points:
- Preview changes before applying
- Safe update workflow
- Deployment history tracking
- Rollback capabilities
- Atomic updates (all or nothing)

CLEANUP:
========
After each demo:
1. pulumi destroy --preview (preview destruction)
2. pulumi destroy (clean up resources)
3. pulumi stack rm <stack-name> (remove stack)

TIPS:
=====
- Always run 'pulumi preview' before 'pulumi up'
- Use 'pulumi stack output' to see resource information
- Use 'pulumi config' to see current configuration
- Use 'pulumi history' to see deployment history
- Use 'pulumi refresh' to sync state with reality

NEXT STEPS:
===========
After understanding core concepts, move to best practices demos
for production-ready infrastructure patterns.
"""