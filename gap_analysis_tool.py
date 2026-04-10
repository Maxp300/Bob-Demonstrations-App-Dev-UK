#!/usr/bin/env python3
"""
Gap Analysis Tool for Business Analyst Workflow
Detects discrepancies between design artifacts and implementation
"""

import os
import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


class SeverityLevel(Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class DiscrepancyType(Enum):
    MISSING_FEATURE = "Missing Feature"
    INCORRECT_IMPLEMENTATION = "Incorrect Implementation"
    MISSING_DEPENDENCY = "Missing Dependency"
    CONFIGURATION_MISMATCH = "Configuration Mismatch"
    ARCHITECTURE_DEVIATION = "Architecture Deviation"
    SECURITY_ISSUE = "Security Issue"
    DOCUMENTATION_GAP = "Documentation Gap"


@dataclass
class Discrepancy:
    id: str
    type: DiscrepancyType
    severity: SeverityLevel
    title: str
    description: str
    design_requirement: str
    actual_implementation: str
    impact: str
    recommendation: str
    file_path: str = None
    line_number: int = None


class GapAnalyzer:
    def __init__(self, design_baseline_path: str, implementation_path: str):
        self.design_baseline_path = design_baseline_path
        self.implementation_path = implementation_path
        self.discrepancies: List[Discrepancy] = []
        
    def analyze(self) -> List[Discrepancy]:
        """Run complete gap analysis"""
        print("Starting Gap Analysis...")
        print("=" * 80)
        
        # Analyze different aspects
        self.analyze_database_requirements()
        self.analyze_security_requirements()
        self.analyze_cicd_pipeline()
        self.analyze_dependencies()
        self.analyze_architecture_patterns()
        
        print(f"\nAnalysis complete. Found {len(self.discrepancies)} discrepancies.")
        return self.discrepancies
    
    def analyze_database_requirements(self):
        """Check database implementation against design"""
        print("\n[1/5] Analyzing database requirements...")
        
        # Check pom.xml for database dependencies
        pom_path = os.path.join(self.implementation_path, "backend/pom.xml")
        if os.path.exists(pom_path):
            with open(pom_path, 'r') as f:
                pom_content = f.read()
            
            # Check for MongoDB (should be relational DB)
            if 'spring-boot-starter-data-mongodb' in pom_content:
                self.discrepancies.append(Discrepancy(
                    id="DISC-001",
                    type=DiscrepancyType.INCORRECT_IMPLEMENTATION,
                    severity=SeverityLevel.CRITICAL,
                    title="Wrong Database Type: MongoDB instead of Relational Database",
                    description="Implementation uses MongoDB (NoSQL) but design specifies relational database",
                    design_requirement="Relational database for better query flexibility and high read speeds",
                    actual_implementation="MongoDB (NoSQL database) configured in pom.xml",
                    impact="Data model may not support complex queries; migration will be required",
                    recommendation="Replace MongoDB with PostgreSQL or MySQL and update all data access layers",
                    file_path="implementation/backend/pom.xml",
                    line_number=42
                ))
            
            # Check for Hibernate
            if 'hibernate' not in pom_content.lower():
                self.discrepancies.append(Discrepancy(
                    id="DISC-002",
                    type=DiscrepancyType.MISSING_DEPENDENCY,
                    severity=SeverityLevel.HIGH,
                    title="Missing Hibernate ORM Dependency",
                    description="Design specifies Hibernate ORM but it's not explicitly configured",
                    design_requirement="Hibernate ORM for performant, lightweight data access with schema tracking",
                    actual_implementation="Generic Spring Data JPA without explicit Hibernate configuration",
                    impact="May not get Hibernate-specific features like automatic schema updates",
                    recommendation="Add explicit Hibernate dependency and configuration",
                    file_path="implementation/backend/pom.xml",
                    line_number=35
                ))
    
    def analyze_security_requirements(self):
        """Check security implementation against design"""
        print("[2/5] Analyzing security requirements...")
        
        # Check pom.xml for Auth0
        pom_path = os.path.join(self.implementation_path, "backend/pom.xml")
        if os.path.exists(pom_path):
            with open(pom_path, 'r') as f:
                pom_content = f.read()
            
            if 'auth0' not in pom_content.lower():
                self.discrepancies.append(Discrepancy(
                    id="DISC-003",
                    type=DiscrepancyType.MISSING_DEPENDENCY,
                    severity=SeverityLevel.CRITICAL,
                    title="Missing Auth0 Integration",
                    description="Design specifies Auth0 for authentication but no Auth0 dependency found",
                    design_requirement="Auth0 as external identity server with OAuth2 and OpenID Connect",
                    actual_implementation="Basic Spring Security without Auth0",
                    impact="Security implementation doesn't meet design specifications; no OAuth2/OIDC support",
                    recommendation="Add Auth0 Spring Security dependency and configure OAuth2 resource server",
                    file_path="implementation/backend/pom.xml"
                ))
        
        # Check SecurityConfig
        security_config_path = os.path.join(
            self.implementation_path, 
            "backend/src/main/java/com/electrify/config/SecurityConfig.java"
        )
        if os.path.exists(security_config_path):
            with open(security_config_path, 'r') as f:
                security_content = f.read()
            
            if 'httpBasic()' in security_content:
                self.discrepancies.append(Discrepancy(
                    id="DISC-004",
                    type=DiscrepancyType.SECURITY_ISSUE,
                    severity=SeverityLevel.CRITICAL,
                    title="Using HTTP Basic Auth instead of OAuth2/OIDC",
                    description="Implementation uses HTTP Basic authentication instead of OAuth2 with PKCE",
                    design_requirement="Authorization Code Flow with PKCE for single page applications",
                    actual_implementation="HTTP Basic authentication",
                    impact="Security model doesn't support modern authentication flows; vulnerable to attacks",
                    recommendation="Implement OAuth2 resource server with Auth0 and PKCE flow",
                    file_path="implementation/backend/src/main/java/com/electrify/config/SecurityConfig.java",
                    line_number=38
                ))
        
        # Check frontend package.json for Auth0 React SDK
        package_json_path = os.path.join(self.implementation_path, "frontend/package.json")
        if os.path.exists(package_json_path):
            with open(package_json_path, 'r') as f:
                package_content = f.read()
            
            if '@auth0/auth0-react' not in package_content:
                self.discrepancies.append(Discrepancy(
                    id="DISC-005",
                    type=DiscrepancyType.MISSING_DEPENDENCY,
                    severity=SeverityLevel.HIGH,
                    title="Missing Auth0 React SDK",
                    description="Frontend missing Auth0 React SDK for PKCE authentication flow",
                    design_requirement="Single page application with Auth0 PKCE flow",
                    actual_implementation="No Auth0 integration in frontend",
                    impact="Cannot implement PKCE flow; authentication not aligned with design",
                    recommendation="Add @auth0/auth0-react package and implement Auth0Provider",
                    file_path="implementation/frontend/package.json"
                ))
    
    def analyze_cicd_pipeline(self):
        """Check CI/CD pipeline against design"""
        print("[3/5] Analyzing CI/CD pipeline...")
        
        gitlab_ci_path = os.path.join(self.implementation_path, "infrastructure/.gitlab-ci.yml")
        if os.path.exists(gitlab_ci_path):
            with open(gitlab_ci_path, 'r') as f:
                ci_content = f.read()
            
            # Check for variables section
            if not re.search(r'^variables:', ci_content, re.MULTILINE):
                self.discrepancies.append(Discrepancy(
                    id="DISC-006",
                    type=DiscrepancyType.CONFIGURATION_MISMATCH,
                    severity=SeverityLevel.MEDIUM,
                    title="Missing CI/CD Variables Section",
                    description="GitLab CI pipeline missing variables section for sensitive data",
                    design_requirement="Variables section (lines 3-8) for usernames, passwords, etc.",
                    actual_implementation="No variables section defined",
                    impact="Sensitive information may be hardcoded; security risk",
                    recommendation="Add variables section with GitLab CI variables for sensitive data",
                    file_path="implementation/infrastructure/.gitlab-ci.yml"
                ))
            
            # Check for package stage
            if 'package' not in ci_content:
                self.discrepancies.append(Discrepancy(
                    id="DISC-007",
                    type=DiscrepancyType.MISSING_FEATURE,
                    severity=SeverityLevel.HIGH,
                    title="Missing Package Stage in CI/CD Pipeline",
                    description="CI/CD pipeline missing package stage for Docker image creation",
                    design_requirement="Package stage (lines 26-48) to create and push Docker images",
                    actual_implementation="Only build stage implemented",
                    impact="Cannot deploy containerized applications; incomplete CI/CD workflow",
                    recommendation="Add package stage with Docker build and push to Docker Hub",
                    file_path="implementation/infrastructure/.gitlab-ci.yml"
                ))
            
            # Check for Docker Hub integration
            if 'docker login' not in ci_content.lower():
                self.discrepancies.append(Discrepancy(
                    id="DISC-008",
                    type=DiscrepancyType.MISSING_FEATURE,
                    severity=SeverityLevel.HIGH,
                    title="Missing Docker Hub Integration",
                    description="No Docker Hub login or image push configured in pipeline",
                    design_requirement="Docker Hub integration for image storage and distribution",
                    actual_implementation="No Docker Hub integration",
                    impact="Cannot store or distribute container images",
                    recommendation="Add Docker Hub login and image push commands in package stage",
                    file_path="implementation/infrastructure/.gitlab-ci.yml"
                ))
    
    def analyze_dependencies(self):
        """Check for missing or incorrect dependencies"""
        print("[4/5] Analyzing dependencies...")
        
        # Already covered in other methods, but can add more checks here
        pass
    
    def analyze_architecture_patterns(self):
        """Check architecture patterns against design"""
        print("[5/5] Analyzing architecture patterns...")
        
        # Check for API Gateway
        docker_compose_path = os.path.join(self.implementation_path, "infrastructure/docker-compose.yml")
        if os.path.exists(docker_compose_path):
            with open(docker_compose_path, 'r') as f:
                compose_content = f.read()
            
            if 'gateway' not in compose_content.lower() and 'api-gateway' not in compose_content.lower():
                self.discrepancies.append(Discrepancy(
                    id="DISC-009",
                    type=DiscrepancyType.ARCHITECTURE_DEVIATION,
                    severity=SeverityLevel.CRITICAL,
                    title="Missing API Gateway",
                    description="No API Gateway service found in infrastructure",
                    design_requirement="API Gateway as single entry point for authentication and routing",
                    actual_implementation="Direct service access without API Gateway",
                    impact="Cannot implement centralized authentication; architecture doesn't match design",
                    recommendation="Implement API Gateway service (e.g., Spring Cloud Gateway or Kong)",
                    file_path="implementation/infrastructure/docker-compose.yml"
                ))
    
    def generate_report(self, output_format: str = "markdown") -> str:
        """Generate gap analysis report"""
        if output_format == "markdown":
            return self._generate_markdown_report()
        elif output_format == "json":
            return self._generate_json_report()
        else:
            raise ValueError(f"Unsupported format: {output_format}")
    
    def _generate_markdown_report(self) -> str:
        """Generate markdown format report"""
        report = []
        report.append("# Gap Analysis Report")
        report.append("## Energy Grid System - Design vs Implementation")
        report.append("")
        report.append(f"**Total Discrepancies Found:** {len(self.discrepancies)}")
        report.append("")
        
        # Summary by severity
        severity_counts = {}
        for disc in self.discrepancies:
            severity_counts[disc.severity] = severity_counts.get(disc.severity, 0) + 1
        
        report.append("### Summary by Severity")
        report.append("")
        report.append("| Severity | Count |")
        report.append("|----------|-------|")
        for severity in SeverityLevel:
            count = severity_counts.get(severity, 0)
            report.append(f"| {severity.value} | {count} |")
        report.append("")
        
        # Summary by type
        type_counts = {}
        for disc in self.discrepancies:
            type_counts[disc.type] = type_counts.get(disc.type, 0) + 1
        
        report.append("### Summary by Type")
        report.append("")
        report.append("| Type | Count |")
        report.append("|------|-------|")
        for disc_type in DiscrepancyType:
            count = type_counts.get(disc_type, 0)
            report.append(f"| {disc_type.value} | {count} |")
        report.append("")
        
        # Detailed findings
        report.append("---")
        report.append("")
        report.append("## Detailed Findings")
        report.append("")
        
        # Sort by severity
        severity_order = {
            SeverityLevel.CRITICAL: 0,
            SeverityLevel.HIGH: 1,
            SeverityLevel.MEDIUM: 2,
            SeverityLevel.LOW: 3,
            SeverityLevel.INFO: 4
        }
        sorted_discrepancies = sorted(
            self.discrepancies, 
            key=lambda x: severity_order[x.severity]
        )
        
        for disc in sorted_discrepancies:
            report.append(f"### {disc.id}: {disc.title}")
            report.append("")
            report.append(f"**Severity:** {disc.severity.value}  ")
            report.append(f"**Type:** {disc.type.value}  ")
            if disc.file_path:
                location = f"{disc.file_path}"
                if disc.line_number:
                    location += f" (Line {disc.line_number})"
                report.append(f"**Location:** `{location}`  ")
            report.append("")
            report.append(f"**Description:** {disc.description}")
            report.append("")
            report.append("**Design Requirement:**")
            report.append(f"> {disc.design_requirement}")
            report.append("")
            report.append("**Actual Implementation:**")
            report.append(f"> {disc.actual_implementation}")
            report.append("")
            report.append(f"**Impact:** {disc.impact}")
            report.append("")
            report.append(f"**Recommendation:** {disc.recommendation}")
            report.append("")
            report.append("---")
            report.append("")
        
        return "\n".join(report)
    
    def _generate_json_report(self) -> str:
        """Generate JSON format report"""
        report_data = {
            "title": "Gap Analysis Report - Energy Grid System",
            "total_discrepancies": len(self.discrepancies),
            "discrepancies": [
                {
                    **asdict(disc),
                    "type": disc.type.value,
                    "severity": disc.severity.value
                }
                for disc in self.discrepancies
            ]
        }
        return json.dumps(report_data, indent=2)


def main():
    """Main execution function"""
    # Paths
    design_baseline = "design_baseline_analysis.md"
    implementation_dir = "implementation"
    
    # Create analyzer
    analyzer = GapAnalyzer(design_baseline, implementation_dir)
    
    # Run analysis
    discrepancies = analyzer.analyze()
    
    # Generate reports
    print("\n" + "=" * 80)
    print("Generating reports...")
    
    # Markdown report
    markdown_report = analyzer.generate_report("markdown")
    with open("gap_analysis_report.md", "w") as f:
        f.write(markdown_report)
    print("✓ Markdown report saved to: gap_analysis_report.md")
    
    # JSON report
    json_report = analyzer.generate_report("json")
    with open("gap_analysis_report.json", "w") as f:
        f.write(json_report)
    print("✓ JSON report saved to: gap_analysis_report.json")
    
    print("\n" + "=" * 80)
    print(f"Gap analysis complete! Found {len(discrepancies)} discrepancies.")
    print("=" * 80)


if __name__ == "__main__":
    main()

# Made with Bob
