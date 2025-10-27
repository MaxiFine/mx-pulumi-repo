# ADR FOR PULUMI: PULUMI FOR IaC OVER TERRAFORM

**Status**: Proposed

**Date**: 2025-10-01

* Deciders: 
   - Ebenezer Butias
   - Maxwell Adomako

**Technical Lead**: Ebenezer Butias

### Problem Statement
The team needs to adopt an alternative Infrastructure as Code (IaC) solution that can leverage existing programming skills while providing strong type safety, reusability, and multi-cloud capabilities. 
Currently part of the team members rely on the console as manual infrastructure management is error-prone, while others use Terraform as the IaC but this doesn't scale with team growth.

### Why Pulumi
Pulumi provides a modern approach to IaC that leverages familiar programming languages while maintaining declarative infrastructure definitions.

## Decision
We will adopt Pulumi with Python as our Infrastructure as Code platform.



