# Security & Compliance Guide

Security assessment, testing, and compliance requirements for the QA Automation Backend.

---

## Security Checklist

### Authentication & Authorization

- [x] JWT token-based authentication
- [x] Password hashing (bcrypt)
- [x] Token expiration enforcement
- [x] CORS protection
- [x] User ownership verification
- [ ] 2FA/MFA implementation
- [ ] OAuth2/OIDC integration

### API Security

- [x] HTTPS/TLS enforcement
- [x] Rate limiting
- [x] Input validation (Pydantic)
- [x] SQL injection prevention (parameterized queries)
- [ ] CSRF protection tokens
- [ ] API key rotation policy
- [ ] Request signing

### Data Protection

- [x] Database encryption at rest (PostgreSQL)
- [ ] Encryption in transit (TLS)
- [ ] Data anonymization for PII
- [ ] Secure secret storage
- [ ] Audit logging for sensitive operations
- [ ] GDPR compliance
- [ ] Data retention policy

### Infrastructure

- [x] Container image scanning
- [x] Kubernetes RBAC
- [x] Network policies
- [ ] Web Application Firewall (WAF)
- [ ] DDoS protection
- [ ] Intrusion detection
- [ ] Security group restrictions

### Code & Dependencies

- [x] SAST (Static Analysis Security Testing)
- [x] Dependency vulnerability scanning
- [ ] DAST (Dynamic Analysis Security Testing)
- [ ] Penetration testing
- [ ] Code review process
- [ ] Supply chain security

---

## OWASP Top 10 Mitigations

### 1. Broken Access Control

✅ **Status:** Protected

```python
# Verify user ownership before operations
if project.owner_id != current_user.id:
    raise HTTPException(status_code=403, detail="Forbidden")
```

### 2. Cryptographic Failures

✅ **Status:** Protected

```python
# Password hashing with bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash(password)
```

### 3. Injection (SQL, NoSQL, Command)

✅ **Status:** Protected

```python
# Use parameterized queries via SQLAlchemy ORM
result = await db.execute(select(User).where(User.email == user_email))

# Never use string concatenation
# WRONG: f"SELECT * FROM users WHERE email = '{user_email}'"
```

### 4. Insecure Design

✅ **Status:** Protected

```python
# Threat modeling in design phase
# Secure defaults
# Input validation at boundaries
```

### 5. Security Misconfiguration

✅ **Status:** Protected

```python
# Use environment variables for configuration
# Disable debug mode in production
# Remove default credentials
# Minimal image sizes
```

### 6. Vulnerable & Outdated Components

✅ **Status:** Protected

```bash
# Regularly scan dependencies
pip install safety
safety check

# Use specific versions
pip-audit --fix
```

### 7. Identification & Authentication Failures

✅ **Status:** Protected

```python
# JWT token expiration
JWT_EXPIRATION_HOURS = 24

# Secure password requirements
# Rate limiting on login attempts
```

### 8. Software & Data Integrity Failures

✅ **Status:** Protected

```python
# Code review process
# Automated testing (CI/CD)
# Signed commits
# Version control
```

### 9. Logging & Monitoring Failures

✅ **Status:** Protected

```python
# Structured logging with context
logger.info(
    "security_event",
    event_type="failed_login",
    user_email=email,
    ip_address=client_ip
)
```

### 10. SSRF (Server-Side Request Forgery)

✅ **Status:** Protected

```python
# Whitelist allowed URLs
ALLOWED_WEBHOOK_DOMAINS = ["github.com", "jira.atlassian.com"]

# Validate webhook URLs before storing
if not validate_webhook_url(url, ALLOWED_WEBHOOK_DOMAINS):
    raise ValidationError("Invalid webhook URL")
```

---

## Security Testing

### Static Analysis (SAST)

```bash
# Bandit - Python security linter
pip install bandit
bandit -r backend/app -f json -o bandit-report.json

# Results analysis
# - High: SQL injection, hardcoded secrets
# - Medium: Weak cryptography
# - Low: Code quality issues
```

### Dependency Scanning

```bash
# Check for vulnerable dependencies
pip install pip-audit
pip-audit

# Safety check
pip install safety
safety check --json > safety-report.json
```

### Secret Scanning

```bash
# Scan for exposed secrets
pip install detect-secrets
detect-secrets scan > .secrets.baseline
git secrets install
git secrets scan-history
```

### Dynamic Analysis (DAST)

```bash
# OWASP ZAP Scanning
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://qa-backend:8000

# Results: XSS, SQLi, authentication bypasses
```

### Penetration Testing Checklist

1. **Authentication Testing**
   - [ ] Test password reset flow
   - [ ] Test session management
   - [ ] Test token expiration
   - [ ] Test concurrent logins
   - [ ] Test JWT key rotation

2. **Authorization Testing**
   - [ ] Test cross-user data access
   - [ ] Test privilege escalation
   - [ ] Test CORS policies
   - [ ] Test API endpoint access

3. **Input Validation**
   - [ ] Test SQLi vectors
   - [ ] Test XSS payloads
   - [ ] Test command injection
   - [ ] Test path traversal
   - [ ] Test buffer overflows

4. **API Testing**
   - [ ] Test rate limiting
   - [ ] Test request validation
   - [ ] Test response disclosure
   - [ ] Test error messages

5. **Infrastructure**
   - [ ] Test TLS configuration
   - [ ] Test certificate validity
   - [ ] Test firewall rules
   - [ ] Test network segmentation

---

## Secrets Management

### Never Commit Secrets

❌ **NEVER do this:**

```python
DATABASE_URL = "postgresql://user:password@localhost/db"
JWT_SECRET = "super-secret-key"
API_KEY = "sk-1234567890"
```

✅ **DO this:**

```python
# .env file (never commit)
DATABASE_URL=postgresql://user:password@localhost/db

# Access from environment
DATABASE_URL = os.getenv("DATABASE_URL")
```

### Secret Rotation

```bash
# Generate new JWT secret
openssl rand -hex 32

# Update in Kubernetes
kubectl create secret generic jwt-secret \
  --from-literal=JWT_SECRET="new-secret" \
  --dry-run=client -o yaml | kubectl apply -f -

# Restart pods
kubectl rollout restart deployment/qa-backend -n qa-automation
```

### Secret Scanning

```bash
# Pre-commit hook to prevent secret commits
pip install pre-commit
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
EOF

pre-commit install
pre-commit run --all-files
```

---

## Compliance

### GDPR (General Data Protection Regulation)

- [ ] Implement data export endpoint
- [ ] Implement data deletion endpoint
- [ ] Privacy policy documentation
- [ ] Consent management
- [ ] Data breach notification procedure

### HIPAA (Health Insurance Portability and Accountability Act)

- [ ] Encryption in transit (TLS)
- [ ] Encryption at rest
- [ ] Access controls
- [ ] Audit logging
- [ ] Business Associate Agreement (BAA)

### SOC 2

- [ ] Access controls documented
- [ ] Change management process
- [ ] Incident response plan
- [ ] Security monitoring
- [ ] Annual audit requirement

### PCI DSS (Payment Card Industry)

- [ ] No credit card storage
- [ ] No cardholder data processing
- [ ] Secure configuration
- [ ] Vulnerability management

---

## Incident Response

### Breach Detection

1. Monitor security logs for:
   - Multiple failed login attempts
   - Unauthorized API access
   - Data export operations
   - Admin permission changes

2. Immediate actions:
   ```bash
   # Revoke compromised tokens
   kubectl delete secret jwt-secret -n qa-automation
   kubectl create secret generic jwt-secret \
     --from-literal=JWT_SECRET="emergency-new-secret"
   
   # Force logout all users
   # (truncate session table)
   ```

### Incident Response Plan

1. **Detection** - Alert on security event
2. **Containment** - Stop attack, isolate affected systems
3. **Eradication** - Remove threat, patch vulnerability
4. **Recovery** - Restore systems, verify integrity
5. **Post-Incident** - Root cause analysis, process improvement

### Notification Process

```
1. Alert triggered → 2. Page on-call → 3. Triage → 4. Escalate
↓
5. Incident commander → 6. Notify stakeholders → 7. Communicate status
↓
8. Resolution → 9. Post-mortem → 10. Update procedures
```

---

## Security Best Practices

### Code Review

✅ **Security-focused review checklist:**

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] SQL parameterization used
- [ ] Authentication enforced
- [ ] Authorization verified
- [ ] Error handling secure (no info disclosure)
- [ ] Logging sanitized (no PII)
- [ ] Dependencies current

### Development

- Use security linters (bandit, semgrep)
- Enable pre-commit hooks
- Sign commits with GPG
- Use secure development practices
- Keep dependencies updated

### Deployment

- Scan images before deployment
- Use minimal base images
- Run containers as non-root
- Enable security context
- Implement pod security standards

### Operations

- Rotate secrets regularly
- Monitor security logs
- Perform regular audits
- Update runbooks
- Train team on security

---

## Reporting Security Issues

⚠️ **Do not open public issues for security vulnerabilities**

1. Email security team: `security@example.com`
2. Include detailed description
3. Provide reproduction steps
4. Be patient for response

**Responsible disclosure:**
- Private reporting
- No public disclosure until patch
- Credit security researcher
- Follow timeline (e.g., 90 days)

---

## Security Resources

- OWASP Top 10: https://owasp.org/Top10
- OWASP Cheat Sheets: https://cheatsheetseries.owasp.org
- CWE/SANS Top 25: https://cwe.mitre.org/top25
- Bandit: https://bandit.readthedocs.io
- Safety: https://safety.readthedocs.io
