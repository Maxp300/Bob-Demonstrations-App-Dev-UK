# Design Baseline Analysis
## Energy Grid System - Technical Design Document

**Document Version:** 1.0  
**Date:** 17/04/2022  
**Status:** WIP  
**Analysis Date:** 2026-03-03

---

## Executive Summary

This document establishes the "desired state" baseline from the Technical Design Document for the Energy Grid System (Electrify). This baseline will be used to compare against the actual implementation to identify discrepancies.

---

## Key Requirements Extracted

### 1. Architecture Requirements

#### C4 Model
- **Requirement:** System must follow C4 Model architecture
- **Level 1:** System Context Diagram showing software as a whole and users
- **Documentation:** Architecture diagrams should be available via link

#### Entity Relationship Diagram
- **Requirement:** Data entities must be properly modeled
- **Purpose:** Visual representation for stakeholders
- **Reference:** Research document on energy data display requirements

---

### 2. Database Requirements

#### Database Type
- **Requirement:** Relational database (not NoSQL)
- **Justification:** Reading data is more important; need query flexibility with high read speeds
- **Server:** Specific database server chosen (link referenced in document)

#### ORM Requirements
- **Technology:** Hibernate ORM
- **Justification:** 
  - Performant and lightweight
  - Tracks schema changes
  - Auto-updates database
  - Provides CRUD operations
  - Handles database connections
  - SQL-injection proof when used properly
- **Benefits:** Reduces boilerplate code, saves development time

---

### 3. CI/CD Requirements

#### General Requirements
- **Platform:** GitLab CI
- **Security:** Use GitLab CI variables for sensitive information (usernames, passwords)

#### Backend Pipeline
- **File:** `.gitlab-ci.yml`
- **Stages:**
  1. **Build Stage** (Lines 14-24)
     - Build system
     - Store .jar files as artifacts for each microservice
  2. **Package Stage** (Lines 26-48)
     - Create Docker image for each microservice
     - Push images to Docker Hub
     - Login to Docker Hub (Line 38)
     - Process each microservice (Lines 40-46)

#### Web Application Pipeline
- **File:** `.gitlab-ci.yml`
- **Stages:**
  1. **Install Stage** (Lines 11-22)
     - Build system
     - Cache node_modules folder
  2. **Test Stage** (Lines 24-38)
     - Test for linting issues
  3. **Build Stage** (Lines 41-57)
     - Login to Docker Hub
     - Build image
     - Push to Docker Hub

---

### 4. Security Requirements

#### Authentication & Authorization
- **Technology:** Auth0 (external identity server)
- **Protocols:** OAuth2 and OpenID Connect (industry standards)
- **Architecture:**
  - **Authentication:** Implemented globally in API Gateways
  - **Authorization:** Implemented per service (best practice)

#### API Gateway Requirements
- **Purpose:** Single endpoint entry for all requests
- **Benefits:**
  - Central interface for clients
  - Reduces latency
  - Ensures consistent authentication
- **Functionality:**
  - Enrich requests with user/security context
  - Route to downstream services
  - Downstream services enforce authorization checks

#### Authorization Flow
- **Flow Type:** Authorization Code Flow with Proof Key for Code Exchange (PKCE)
- **Justification:** 
  - Recommended for single page applications
  - Most secure flow for client-side applications
  - Addresses special security challenges
- **Reference:** Auth0 documentation on PKCE flow

---

## Technology Stack Summary

| Component | Technology | Status |
|-----------|-----------|--------|
| Database Type | Relational Database | Required |
| ORM | Hibernate | Required |
| CI/CD Platform | GitLab CI | Required |
| Container Registry | Docker Hub | Required |
| Identity Provider | Auth0 | Required |
| Auth Protocol | OAuth2 + OpenID Connect | Required |
| Auth Flow | Authorization Code Flow with PKCE | Required |
| Application Type | Single Page Application | Specified |

---

## Architecture Patterns

1. **Microservices Architecture** - Multiple microservices mentioned
2. **API Gateway Pattern** - Central entry point for all requests
3. **Centralized Authentication** - Auth at gateway level
4. **Distributed Authorization** - Auth per service
5. **CI/CD Automation** - Automated build, test, and deployment

---

## Critical Integration Points

1. **Auth0 Integration** - External identity server
2. **Docker Hub Integration** - Container registry
3. **GitLab CI Integration** - CI/CD pipeline
4. **Database Integration** - Via Hibernate ORM
5. **API Gateway Integration** - Request routing and authentication

---

## Documentation References

The design document references several external resources:
- C4 Model architecture diagrams (link)
- Database server choice documentation (link)
- Backend `.gitlab-ci.yml` file (link)
- Web app `.gitlab-ci.yml` file (link)
- Research document on energy data display
- Research document on security approach
- Auth0 PKCE flow documentation (link)

---

## Notes for Gap Analysis

When comparing implementation against this baseline, check for:
1. ✓ Correct database type (relational vs NoSQL)
2. ✓ Hibernate ORM usage
3. ✓ GitLab CI pipeline structure and stages
4. ✓ Docker Hub integration
5. ✓ Auth0 integration with correct protocols
6. ✓ API Gateway implementation
7. ✓ PKCE authorization flow
8. ✓ Microservices architecture
9. ✓ Security best practices (authentication at gateway, authorization per service)
10. ✓ Proper use of CI variables for sensitive data

---

**End of Baseline Analysis**