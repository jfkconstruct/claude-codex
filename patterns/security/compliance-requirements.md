# Compliance Requirements for LLM Applications

## Overview

LLM applications handling sensitive data must comply with various regulatory frameworks. This guide covers GDPR, HIPAA, and SOC 2 requirements, which are the most common compliance standards for AI/LLM deployments.

**Key Insight**: Production AI agents handling sensitive data require GDPR/HIPAA/SOC 2 compliance, adding $8k-25k to development costs, and must include encryption, audit logging, PII protection, and data retention policies.

## Compliance Framework Comparison

| Framework | Scope | Primary Focus | Verification | Penalties |
|-----------|-------|---------------|--------------|-----------|
| **GDPR** | EU residents' data (global) | Data privacy, user rights | Self-managed | Up to €20M or 4% global revenue |
| **HIPAA** | US healthcare data (PHI) | Healthcare data protection | Self-managed | $141 - $2.1M per violation |
| **SOC 2** | Service providers | Security controls | External audit | Contract/business impact |

## SOC 2 Compliance

### Overview

**Importance**: 83-85% of enterprise buyers now require SOC 2 compliance as a vendor prerequisite. SOC 2 Type II is a minimum in many enterprise procurement checklists.

**Business Impact**: Regulatory penalties can reach millions of dollars, but compliance isn't just about avoiding fines—it's about enabling business growth and maintaining customer trust.

### Trust Service Criteria

SOC 2 is based on five Trust Service Criteria:

1. **Security**: Protection against unauthorized access
2. **Availability**: System operational and available for use
3. **Processing Integrity**: System processing is complete, valid, accurate, timely
4. **Confidentiality**: Confidential information is protected
5. **Privacy**: Personal information is collected, used, retained, disclosed, and disposed properly

### SOC 2 Type I vs Type II

- **Type I**: Controls are properly designed at a point in time
- **Type II**: Controls operate effectively over a period (typically 6-12 months)

**Recommendation**: Pursue Type II for credibility with enterprise customers.

### Key Requirements for LLM Applications

#### 1. Access Controls
```yaml
Requirements:
  - Multi-factor authentication (MFA)
  - Role-based access control (RBAC)
  - Principle of least privilege
  - Regular access reviews
  - Termination procedures

Implementation:
  - Use identity providers (Okta, Auth0, Azure AD)
  - Implement API key rotation
  - Log all access attempts
  - Separate production and development access
```

#### 2. Encryption
```yaml
Requirements:
  - Data at rest: AES-256 or equivalent
  - Data in transit: TLS 1.2+ (prefer TLS 1.3)
  - Key management: Hardware Security Modules (HSM) or cloud KMS

For LLM Applications:
  - Encrypt API requests/responses
  - Encrypt stored prompts and completions
  - Encrypt model artifacts
  - Secure key storage (AWS KMS, Azure Key Vault, GCP KMS)
```

#### 3. Monitoring and Logging
```yaml
Requirements:
  - Centralized logging
  - Log retention (typically 90 days minimum)
  - Real-time alerting
  - Audit trails
  - Log immutability

LLM-Specific Logs:
  - API calls with timestamps
  - User identifiers (hashed)
  - Input/output content (if policy permits)
  - Model versions used
  - Policy violations
  - Access to sensitive data
```

#### 4. Incident Response
```yaml
Requirements:
  - Documented incident response plan
  - Regular testing/drills
  - Defined escalation procedures
  - Post-incident reviews

LLM-Specific Incidents:
  - Prompt injection attacks
  - Data leakage
  - Model poisoning
  - Unauthorized access to training data
  - PII exposure
```

#### 5. Vendor Management
```yaml
Requirements:
  - Vendor risk assessments
  - Third-party security reviews
  - SOC 2 reports from vendors
  - Data processing agreements

For LLM Vendors (Claude, OpenAI, etc.):
  - Review vendor SOC 2 reports
  - Ensure BAA/DPA in place
  - Verify data handling policies
  - Understand model training policies
  - Check subprocessor list
```

### SOC 2 Audit Process

1. **Preparation** (2-4 months)
   - Gap assessment
   - Implement required controls
   - Document policies and procedures

2. **Readiness Assessment** (1 month)
   - Pre-audit by auditor
   - Identify gaps
   - Remediate issues

3. **Audit** (2-4 weeks)
   - Evidence collection
   - Control testing
   - Interviews

4. **Report Issuance** (2-4 weeks)
   - Draft report review
   - Final report delivery

**Total timeline**: 6-12 months for Type II

**Costs**: $15k-$50k for initial audit, $10k-$30k for annual renewals

## HIPAA Compliance

### Overview

**Scope**: Protected Health Information (PHI) in the United States

**Penalties**: $141 to $2,134,831 per violation, depending on negligence level

**Key Requirement**: Business Associate Agreement (BAA) required with any vendor processing PHI

### What is PHI?

Protected Health Information includes:
- Names
- Dates (birth, admission, discharge, death)
- Phone/fax numbers
- Email addresses
- Social Security numbers
- Medical record numbers
- Health plan beneficiary numbers
- Account numbers
- Certificate/license numbers
- Vehicle identifiers and serial numbers
- Device identifiers and serial numbers
- URLs and IP addresses
- Biometric identifiers (fingerprints, voice prints)
- Full-face photos
- Any other unique identifying number or code

### HIPAA Rules for LLM Applications

#### 1. Privacy Rule

**Requirements**:
- Minimum necessary standard (only access PHI needed for task)
- Patient consent for uses beyond treatment/payment/operations
- Right to access own records
- Right to request amendments
- Notice of privacy practices

**For LLMs**:
```python
# ❌ Bad: Sending entire medical record
send_to_llm(patient_complete_record)

# ✅ Good: Send only necessary fields
send_to_llm({
    "symptoms": patient.symptoms,
    "relevant_history": filter_relevant(patient.history),
    "age_range": generalize_age(patient.age)
})
```

#### 2. Security Rule

**Administrative Safeguards**:
- Risk analysis and management
- Workforce training
- Access management
- Security incident procedures

**Physical Safeguards**:
- Facility access controls
- Workstation security
- Device and media controls

**Technical Safeguards**:
- Access controls (unique user IDs, emergency access, automatic log-off)
- Audit controls
- Integrity controls
- Transmission security (encryption)

#### 3. Breach Notification Rule

**Requirements if PHI breach occurs**:
- Notify affected individuals within 60 days
- Notify HHS (immediately if >500 individuals)
- Notify media if >500 individuals in same state
- Document breach and response

**Prevention for LLMs**:
```python
class HIPAACompliantLLMGateway:
    def __init__(self):
        self.phi_detector = PHIDetector()
        self.encryptor = Encryptor()
        self.audit_logger = AuditLogger()

    def process_request(self, request, user):
        # Detect PHI
        phi_detected = self.phi_detector.scan(request)
        if phi_detected:
            self.audit_logger.log_phi_access(user, phi_detected)

        # Encrypt before sending
        encrypted = self.encryptor.encrypt(request)

        # Send via secure channel (VPN/private link + TLS)
        response = self.llm_api.call(encrypted)

        # Log transaction
        self.audit_logger.log_transaction(user, request.id, response.id)

        return response
```

### Deployment Options for HIPAA Compliance

Three compliant options:

1. **Self-hosted open-source LLM**
   - Pros: Full control, maximum privacy
   - Cons: Deep technical expertise required, infrastructure costs
   - Examples: Llama 2, Mistral on your own servers

2. **HIPAA-eligible cloud platforms**
   - Pros: Scalability, easier setup
   - Cons: Careful configuration required, shared responsibility
   - Examples: AWS (with BAA), Azure (with BAA), GCP (with BAA)

3. **Healthcare-focused AI vendors**
   - Pros: Turnkey, HIPAA-ready solutions
   - Cons: Higher costs, vendor lock-in
   - Examples: Specialized healthcare AI providers with BAA

### Anthropic Claude & HIPAA

**Enterprise Plans**:
- Anthropic offers BAA for enterprise customers
- Does not train on customer data from paid services
- Encryption in transit (TLS)
- Encryption at rest

**Additional measures needed**:
```yaml
Your Responsibilities:
  - Implement PHI detection and redaction
  - Use VPN or AWS PrivateLink for additional security
  - Enable comprehensive audit logging
  - Implement access controls
  - Train workforce on HIPAA
  - Document all processing activities
  - Incident response plan
  - Regular risk assessments
```

## GDPR Compliance

### Overview

**Scope**: Any organization processing data of EU residents, regardless of where the company is located

**Penalties**: Up to €20 million or 4% of global annual turnover (whichever is higher)

**Key Principles**:
1. Lawfulness, fairness, and transparency
2. Purpose limitation
3. Data minimization
4. Accuracy
5. Storage limitation
6. Integrity and confidentiality
7. Accountability

### Individual Rights Under GDPR

1. **Right to be informed**: Clear privacy notices
2. **Right of access**: Individuals can request their data
3. **Right to rectification**: Correct inaccurate data
4. **Right to erasure** ("right to be forgotten")
5. **Right to restrict processing**
6. **Right to data portability**: Receive data in machine-readable format
7. **Right to object**: Object to processing
8. **Rights related to automated decision-making**: Not be subject to purely automated decisions

### GDPR Requirements for LLM Applications

#### 1. Legal Basis for Processing

You must have a legal basis to process personal data:
- **Consent**: Freely given, specific, informed
- **Contract**: Necessary for contract performance
- **Legal obligation**: Required by law
- **Vital interests**: Protect someone's life
- **Public task**: Perform official functions
- **Legitimate interests**: Necessary for legitimate interests (balance test required)

**For LLMs**:
```
Example consent notice:
"We use AI to analyze your feedback and improve our service. Your data will be
processed by [LLM Provider]. You can withdraw consent at any time by [method]."
```

#### 2. Data Processing Agreements (DPA)

**Required when using LLM APIs**:

A DPA must specify:
- Subject matter and duration of processing
- Nature and purpose of processing
- Types of personal data
- Categories of data subjects
- Obligations and rights of controller
- Security measures
- Subprocessor provisions

**Example DPA requirements for Claude API**:
```yaml
Controller: Your Company
Processor: Anthropic
Purpose: Natural language processing for [specific use case]
Data Categories: [User queries, feedback, etc.]
Security: Encryption in transit and at rest
Subprocessors: [List of Anthropic subprocessors]
Data Location: [US, EU, etc.]
Deletion: Upon contract termination or request
```

#### 3. Privacy by Design and Default

Build privacy into your LLM application from the start:

```python
class GDPRCompliantLLMApp:
    """Privacy by design example"""

    def __init__(self):
        # Default to minimal data collection
        self.data_minimization = True

        # Pseudonymization by default
        self.pseudonymizer = Pseudonymizer()

        # Retention limits
        self.retention_days = 30  # Delete after 30 days unless required

        # Consent management
        self.consent_manager = ConsentManager()

    def process_user_request(self, user_id, request):
        # Check consent
        if not self.consent_manager.has_consent(user_id, 'ai_processing'):
            return self.request_consent(user_id)

        # Minimize data
        minimized = self.minimize_data(request)

        # Pseudonymize
        pseudonymized = self.pseudonymizer.pseudonymize(minimized)

        # Process
        response = self.llm.process(pseudonymized)

        # Log for accountability
        self.log_processing(user_id, minimized, purpose='service_improvement')

        # Schedule deletion
        self.schedule_deletion(user_id, days=self.retention_days)

        return response
```

#### 4. Data Protection Impact Assessment (DPIA)

**Required when**:
- Large-scale processing of sensitive data
- Automated decision-making with legal effects
- Systematic monitoring of public areas
- High risk to rights and freedoms

**LLM applications likely requiring DPIA**:
- Processing health data with LLMs
- Automated hiring decisions based on LLM analysis
- Large-scale sentiment analysis of user content
- Behavioral profiling using LLMs

**DPIA components**:
1. Description of processing
2. Necessity and proportionality assessment
3. Risk assessment
4. Mitigation measures
5. Consultation records (if applicable)

#### 5. Right to Erasure Implementation

```python
class DataErasureService:
    """Implement GDPR right to erasure"""

    def process_erasure_request(self, user_id):
        # 1. Delete user data from database
        self.db.delete_user_data(user_id)

        # 2. Remove from LLM context stores
        self.vector_db.delete_user_embeddings(user_id)

        # 3. Invalidate cached responses
        self.cache.invalidate_user_cache(user_id)

        # 4. Remove from logs (where legally possible)
        self.anonymize_logs(user_id)

        # 5. Notify third-party processors
        self.notify_processors_of_deletion(user_id)

        # 6. Document erasure
        self.log_erasure_completion(user_id, datetime.now())

        return {"status": "erased", "user_id": user_id}
```

**Challenge**: Some LLM providers retain data for model improvement. Ensure your contract prohibits training on user data or get explicit consent.

### Recent GDPR Enforcement Actions (LLMs)

**OpenAI Fine (December 2024)**:
- Italy fined OpenAI €15 million
- Violations:
  - Processing personal data without sufficient legal basis
  - Violating transparency obligations
  - Not providing clear information to users

**Key takeaways**:
- Clear privacy notices essential
- Valid legal basis required
- Transparency about AI use mandatory

## Convergence of Compliance Requirements

The good news: SOC 2, HIPAA, and GDPR have overlapping requirements around core security controls, making a unified approach possible and efficient.

### Common Requirements Matrix

| Requirement | SOC 2 | HIPAA | GDPR |
|-------------|-------|-------|------|
| Encryption at rest | ✓ | ✓ | ✓ (recommended) |
| Encryption in transit | ✓ | ✓ | ✓ |
| Access controls | ✓ | ✓ | ✓ |
| Audit logging | ✓ | ✓ | ✓ |
| Incident response | ✓ | ✓ | ✓ |
| Vendor management | ✓ | ✓ (BAA) | ✓ (DPA) |
| Data minimization | - | ✓ | ✓ |
| Right to access | - | ✓ | ✓ |
| Right to delete | - | - | ✓ |
| Risk assessments | ✓ | ✓ | ✓ (DPIA) |

### Unified Compliance Architecture

```
┌─────────────────────────────────────────────┐
│         Application Layer                   │
│  - GDPR consent management                  │
│  - HIPAA minimum necessary filtering        │
│  - Data minimization                        │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         Security Layer                      │
│  - Encryption (SOC 2, HIPAA, GDPR)         │
│  - Access controls (all)                    │
│  - MFA (all)                                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         LLM Gateway                         │
│  - PHI detection (HIPAA)                    │
│  - PII detection (GDPR)                     │
│  - Audit logging (all)                      │
│  - Rate limiting (SOC 2)                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│         LLM Provider (Claude, etc.)         │
│  - DPA in place (GDPR)                      │
│  - BAA in place (HIPAA)                     │
│  - SOC 2 Type II report                     │
└─────────────────────────────────────────────┘
```

## Implementation Checklist

### SOC 2
- [ ] Define scope of audit
- [ ] Document security policies
- [ ] Implement access controls (MFA, RBAC)
- [ ] Enable encryption (at rest and in transit)
- [ ] Set up centralized logging
- [ ] Implement monitoring and alerting
- [ ] Create incident response plan
- [ ] Conduct vendor risk assessments
- [ ] Perform readiness assessment
- [ ] Engage SOC 2 auditor

### HIPAA
- [ ] Sign BAA with LLM provider
- [ ] Implement PHI detection and redaction
- [ ] Encrypt all PHI (at rest and in transit)
- [ ] Use VPN/PrivateLink for API calls
- [ ] Implement minimum necessary access
- [ ] Train workforce on HIPAA
- [ ] Create breach notification procedures
- [ ] Conduct annual risk assessment
- [ ] Implement physical safeguards
- [ ] Document all policies

### GDPR
- [ ] Determine legal basis for processing
- [ ] Create privacy notice
- [ ] Sign DPA with LLM provider
- [ ] Implement consent management
- [ ] Enable data minimization
- [ ] Implement pseudonymization
- [ ] Support right to access
- [ ] Support right to erasure
- [ ] Conduct DPIA (if high risk)
- [ ] Appoint DPO (if required)
- [ ] Document processing activities
- [ ] Implement data retention limits

## Costs and Timeline

| Compliance | Initial Cost | Annual Cost | Timeline |
|------------|-------------|-------------|----------|
| SOC 2 Type I | $15k-$30k | - | 3-6 months |
| SOC 2 Type II | $25k-$50k | $10k-$30k | 6-12 months |
| HIPAA | $10k-$25k | $5k-$15k | 3-6 months |
| GDPR | $8k-$20k | $5k-$10k | 2-4 months |

**Note**: Costs vary based on organization size, complexity, and existing controls.

## References

- Requesty.ai: Security & Compliance Checklist for LLM Gateways
- TechMagic: HIPAA Compliance AI Guide
- P0STMAN: AI Agent Security Guide 2025
- GDPR Official Text
- HIPAA Security Rule
- AICPA SOC 2 Guidelines

## Related Patterns

- [PII Protection](./pii-protection.md)
- [Security Audit Patterns](./security-audit-patterns.md)
- [Incident Reports](./incident-reports.md)
