# """
# Pulumi Import Demo - Managing Existing AWS Resources
# ==================================================

# This demo shows how to bring existing AWS resources under Pulumi management.
# Perfect for teams wanting to adopt Pulumi with existing infrastructure!

# 🎯 KEY LESSON: You don't have to start from scratch with Pulumi!
# """

# import pulumi
# import pulumi_aws as aws

# # Get current stack name
# stack_name = pulumi.get_stack()
# print(f"\nPULUMI IMPORT DEMO - Stack: {stack_name}")
# print("=" * 50)

# print("1. Importing existing S3 bucket...")
# print("   This bucket was created outside of Pulumi")
# print("   Now we'll bring it under Pulumi management")

# # Define the S3 bucket resource that matches your existing bucket
# # This tells Pulumi what the resource should look like
# imported_bucket = aws.s3.Bucket(
#     "my-imported-bucket123",  # Must match the import command resource name
#     bucket="pulumi-import-bucket-123",  # Actual AWS bucket name (this exists!)
#     tags={
#         "Name": "ImportedBucket",
#         "ManagedBy": "Pulumi", 
#         "Purpose": "ImportDemo",
#         "Environment": stack_name
#     }
# )

# print("2. Adding bucket versioning configuration...")
# # Add versioning to the imported bucket
# bucket_versioning = aws.s3.BucketVersioning(
#     "imported-bucket-versioning",
#     bucket=imported_bucket.id,
#     versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
#         status="Enabled"
#     )
# )

# print("3. Adding server-side encryption...")
# # Add encryption to the imported bucket
# bucket_encryption = aws.s3.BucketServerSideEncryptionConfiguration(
#     "imported-bucket-encryption",
#     bucket=imported_bucket.id,
#     rules=[
#         aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
#             apply_server_side_encryption_by_default=aws.s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
#                 sse_algorithm="AES256"
#             )
#         )
#     ]
# )

# print("4. Creating new resources alongside imported ones...")
# # Create a new S3 bucket to show we can mix imported and new resources
# # new_bucket = aws.s3.Bucket(
# #     "new-demo-bucket",
# #     bucket=f"pulumi-new-demo-{stack_name}-{pulumi.get_stack()}",
# #     tags={
# #         "Name": "NewBucket",
# #         "ManagedBy": "Pulumi",
# #         "Purpose": "ImportDemo", 
# #         "Environment": stack_name,
# #         "CreatedBy": "PulumiCode"
# #     }
# # )

# # Add versioning to the new bucket too
# # new_bucket_versioning = aws.s3.BucketVersioning(
# #     "new-bucket-versioning", 
# #     bucket=new_bucket.id,
# #     versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
# #         status="Enabled"
# #     )
# # )

# # Export information about both buckets
# pulumi.export("imported_bucket_name", imported_bucket.bucket)
# pulumi.export("imported_bucket_arn", imported_bucket.arn)
# # pulumi.export("new_bucket_name", new_bucket.bucket)
# # pulumi.export("new_bucket_arn", new_bucket.arn)

# pulumi.export("demo_info", {
#     "purpose": "Show how to import existing AWS resources",
#     "imported_resources": ["S3 Bucket"],
#     "new_resources": ["S3 Bucket with versioning"],
#     "benefits": [
#         "Gradual adoption of Pulumi",
#         "Manage existing + new resources together", 
#         "Apply consistent policies to all resources"
#     ]
# })

# print("=" * 50)
# print("IMPORT DEMO READY!")
# print("Next steps:")
# print("1. Run: pulumi import aws:s3/bucket:Bucket my-imported-bucket123 pulumi-import-bucket-123")
# print("2. Then: pulumi up")
# print("=" * 50)


"""
Simple Pulumi Import Demo
========================
Shows how to import existing AWS resources into Pulumi.

What we'll demonstrate:
1. We have an existing S3 bucket called "pulumi-import-demo"
2. We'll import it into Pulumi management
3. We'll add better security to it
4. We'll show how Pulumi now manages it
"""

import pulumi
import pulumi_aws as aws

# Step 1: Define the existing bucket that we want to import
# This bucket already exists in AWS: "pulumi-import-demo"
imported_bucket = aws.s3.Bucket(
    "my-imported-bucket",           # This is the name in Pulumi code
    bucket="pulumi-import-demo",    # This is the actual AWS bucket name
    tags={
        "ManagedBy": "Pulumi",
        "Status": "Imported",
        "Team": "DevOps"
    }
)

# Step 2: Add security features to our imported bucket
# Add versioning (keeps old versions of files)
bucket_versioning = aws.s3.BucketVersioning(
    "imported-bucket-versioning",
    bucket=imported_bucket.id,
    versioning_configuration=aws.s3.BucketVersioningVersioningConfigurationArgs(
        status="Enabled"
    )
)

# Add encryption (protects our files)
bucket_encryption = aws.s3.BucketServerSideEncryptionConfiguration(
    "imported-bucket-encryption",
    bucket=imported_bucket.id,
    rules=[aws.s3.BucketServerSideEncryptionConfigurationRuleArgs(
        apply_server_side_encryption_by_default=aws.
        s3.BucketServerSideEncryptionConfigurationRuleApplyServerSideEncryptionByDefaultArgs(
            sse_algorithm="AES256"
        )
    )]
)

# Step 3: Show what we accomplished
pulumi.export("bucket_name", imported_bucket.bucket)
pulumi.export("bucket_arn", imported_bucket.arn)
pulumi.export("what_we_did", [
    "Imported existing S3 bucket into Pulumi",
    "Added versioning for better file management",
    "Added encryption for security",
    "Now we can manage it with code!"
])

print("\n" + "="*50)
print("SIMPLE PULUMI IMPORT DEMO")
print("="*50)
print("Bucket to import: pulumi-import-demo")
print("What happens:")
print("1. Import existing bucket into Pulumi")
print("2. Add versioning and encryption")
print("3. Pulumi now manages the bucket")
print("="*50)