# Simple Authentication API (Python/FastAPI)

## Project Overview
This project provides a basic Authentication API (Register, Login, Protected Route) using JSON Web Tokens (JWTs). It's designed to demonstrate understanding of product integration layers, specifically API creation and authentication mechanisms, which are crucial for integrating AI models into SaaS environments or other applications.

## Features
- User registration (with password hashing).
- User login (returning a JWT).
- JWT generation and validation for securing endpoints.
- A protected endpoint (`/users/me`) that requires authentication.
- In-memory "database" (Python dictionary) for simplicity.

## Technologies Used
- Python 3.8+
- FastAPI: Modern, fast (high-performance) web framework for building APIs.
- Pydantic: Data validation and settings management using Python type annotations.
- passlib: For secure password hashing (using bcrypt).
- python-jose: For encoding, decoding, and verifying JWTs.
- python-dotenv: For managing environment variables.
- Uvicorn: ASGI server for running FastAPI applications.

## Setup Instructions
1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd simple-auth-api-python
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    Copy the `.env.example` file to a new file named `.env`:
    ```bash
    cp .env.example .env
    ```
    Open the `.env` file and **change the `SECRET_KEY`** to a strong, unique secret.
    ```
    SECRET_KEY="your-very-strong-and-unique-secret-key"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

## How to Run
Ensure your virtual environment is activated and you are in the `simple-auth-api-python` root directory.
Run the FastAPI application using Uvicorn:
```bash
uvicorn src.main:app --reload
```

---
# Scale Authentication API (POC to Production)

## Overview

This guide details best practices and architecture considerations for evolving an Authentication API from a simple prototype to a production-grade service.

## Table of Contents

1. [Database Layer](#database-layer)
2. [Security](#security)
3. [Scalability & Performance](#scalability--performance)
4. [Monitoring & Logging](#monitoring--logging)
5. [Deployment & Operations](#deployment--operations)
6. [User Management & Administration](#user-management--administration)

---

## 1. Database Layer

### POC Scenario

* In-memory dictionary or SQLite

### Production Requirements

* **Robust Database**: PostgreSQL, MySQL, or NoSQL (MongoDB) supporting transactions, indexing, and horizontal scaling
* **High Availability & Backup**: Configure replication, automated backups, and failover mechanisms
* **Connection Pooling**: Efficiently manage DB connections (e.g., pgBouncer, HikariCP)

---

## 2. Security

### POC Scenario

* Basic password hashing, simple JWT issuance

### Production Requirements

* **Password Hashing**: Use Argon2, bcrypt, or scrypt with per-user salts
* **JWT Best Practices**:

  * Strong secret keys stored in environment variables or a secrets manager, with periodic rotation
  * Consider asymmetric algorithms (RS256/ES256) if issuer and verifier differ
  * Short-lived access tokens (5–15 minutes) and secure refresh tokens (HTTPOnly cookies)
  * Token revocation mechanism (blacklist on logout, password change)
* **Transport Security**: Enforce HTTPS on all endpoints
* **Input Validation**: Strictly validate inputs to prevent XSS, SQL injection
* **Rate Limiting & Brute-Force Protection**: Throttle login attempts, temporary account lockout
* **Multi-Factor Authentication (MFA)**: Implement 2FA with TOTP or SMS/Email codes
* **OAuth2 / OpenID Connect**: Support third‑party identity providers or allow external services to use your auth via standard protocols
* **Security Headers**: HSTS, Content-Security-Policy, X-Frame-Options, etc.
* **Regular Audits & Pen Testing**: Schedule security reviews and penetration tests

---

## 3. Scalability & Performance

### POC Scenario

* Single-instance API

### Production Requirements

* **Load Balancing**: Distribute traffic across multiple instances (e.g., AWS ELB, GCP Load Balancer)
* **Auto-Scaling**: Scale instances based on CPU, memory, or request rate
* **Caching**: Cache frequently accessed data (user permissions, session metadata) using Redis or Memcached
* **Stateless Design**: Keep the API stateless to simplify scaling

---

## 4. Monitoring & Logging

### POC Scenario

* Console logs

### Production Requirements

* **Detailed Logging**: Capture login attempts, token issuance/validation, password changes, source IP, user agent
* **Security Monitoring**: Alerts for suspicious behavior (excessive failed logins, unauthorized resource access)
* **Performance Metrics**: Track latency, error rates, throughput per endpoint
* **Centralized Log Management**: ELK Stack, Graylog, or Cloud Logging
* **Alerting & Dashboards**: Configure alerts and dashboards (Grafana, Kibana) for real-time insights

---

## 5. Deployment & Operations

### POC Scenario

* Manual execution

### Production Requirements

* **Containerization**: Dockerize services and dependencies
* **Orchestration**: Deploy on Kubernetes or serverless platforms (AWS Lambda, GCP Cloud Run)
* **CI/CD Pipeline**: Automate unit, integration, and security tests plus deployments (GitHub Actions, Jenkins, GitLab CI)
* **Configuration Management**: Securely manage credentials and secrets (Vault, AWS Secrets Manager, GCP Secret Manager)

---

## 6. User Management & Administration

### POC Scenario

* No or minimal admin interface

### Production Requirements

* **Admin Dashboard**: UI for managing user accounts, roles, permissions, password resets, and account disabling
* **Audit Logs**: Record administrative actions for compliance