# Security Best Practices for Claude and LLM Applications

## Overview

This directory contains comprehensive security patterns, best practices, and real-world incident analysis for building secure LLM applications, with specific focus on Claude and similar large language models.

**Last Updated**: November 2025

## Contents

### 📋 [Prompt Injection Defense](./prompt-injection-defense.md)
Comprehensive guide to defending against prompt injection attacks, the #1 vulnerability in OWASP's 2025 LLM Top 10.

**Key Topics**:
- Multi-layered defense strategies
- Claude-specific recommendations
- AWS best practices tested on Claude
- Salted tags and attack pattern recognition
- Input validation and sanitization
- Context adherence and role definition
- Known limitations and future research

**Critical Stats**:
- 78% success rate on Claude 3.5 Sonnet with sufficient attempts
- Claude is far more resistant than other LLMs due to Constitutional AI
- No fool-proof solution exists yet

---

### 🔒 [PII Protection](./pii-protection.md)
Strategies for protecting Personally Identifiable Information when using LLMs and APIs.

**Key Topics**:
- Automated redaction techniques
- Pseudonymization vs. anonymization
- Data minimization patterns
- Masking techniques
- DLP (Data Loss Prevention) integration
- Claude API data privacy policies
- Implementation patterns

**Core Principle**: The safest data is the data never transmitted.

**Tools Covered**:
- Microsoft Presidio
- OneShield
- Strac DLP
- AWS Comprehend

---

### 🛡️ [Content Filtering and Moderation](./content-filtering.md)
Modern approaches to content moderation using LLMs for context-aware filtering.

**Key Topics**:
- Evolution from keyword filtering to LLM-based moderation
- Dual-model moderation pattern
- Prompt-based moderation
- LlamaGuard implementation
- Human-AI hybrid moderation
- Context-aware filtering
- Known challenges (bias, multilingual, prompt injection)

**Best Practice**: Multi-layered approach combining automated filtering, human oversight, and continuous monitoring.

---

### 📜 [Compliance Requirements](./compliance-requirements.md)
Detailed guide to GDPR, HIPAA, and SOC 2 compliance for LLM applications.

**Frameworks Covered**:

| Framework | Scope | Primary Focus | Penalties |
|-----------|-------|---------------|-----------|
| **GDPR** | EU residents (global) | Data privacy | Up to €20M or 4% revenue |
| **HIPAA** | US healthcare (PHI) | Health data protection | $141 - $2.1M per violation |
| **SOC 2** | Service providers | Security controls | Business impact |

**Key Insight**: 83-85% of enterprise buyers require SOC 2 compliance. Compliance costs: $8k-25k implementation.

**Includes**:
- Technical requirements
- Deployment options
- Implementation checklists
- Costs and timelines
- Unified compliance architecture

---

### 🔍 [Security Audit Patterns](./security-audit-patterns.md)
Frameworks and tools for auditing LLM application security.

**Key Topics**:
- OWASP Top 10 for LLM Applications (2025)
- LLM AI Security and Governance Checklist
- Comprehensive penetration testing
- Automated vulnerability scanning
- Periodic vulnerability assessments
- Security testing tools (LLMFuzzer, Garak)
- Best practices and audit reporting

**OWASP LLM Top 10**:
1. Prompt Injection
2. Insecure Output Handling
3. Training Data Poisoning
4. Model Denial of Service
5. Supply Chain Vulnerabilities
6. Sensitive Information Disclosure
7. Insecure Plugin Design
8. Excessive Agency
9. Overreliance
10. Model Theft

---

### 📰 [Incident Reports](./incident-reports.md)
Real-world security incidents and case studies from 2024-2025.

**Major Incidents Covered**:
- **Cursor IDE Vulnerabilities** (2025): Remote code execution via prompt injection
- **OmniGPT Data Breach** (Feb 2025): 30,000+ users, 34M+ chat conversations leaked
- **DeepSeek Database Exposure** (Dec 2024): 1M+ API tokens compromised, 2B+ tokens illegally used
- **Microsoft 365 Copilot** (2025): Zero-click data exfiltration
- **ChatGPT "ShadowLeak"** (2025): Server-side vulnerability in Deep Research
- **Claude Desktop Extensions** (Nov 2025): Unsandboxed execution risk
- **OpenAI GDPR Fine** (Dec 2024): €15M fine for privacy violations
- **Copy-Paste Injection** (2024): Hidden prompts in text
- **Cisco DeepSeek R1 Jailbreak** (Q1 2025): 100% success rate
- **Microsoft Copilot Phishing Bot** (2025): Email-based prompt injection

**Key Statistics**:
- 5 major LLM data breaches in Jan-Feb 2025 alone
- Estimated $100M+ industry impact in direct costs 2024-2025
- 100% jailbreak success rate demonstrated on some models

---

## Quick Start Guide

### For Developers

1. **Start with defense basics**:
   - Read [Prompt Injection Defense](./prompt-injection-defense.md)
   - Implement multi-layered input validation
   - Set up output monitoring

2. **Protect sensitive data**:
   - Review [PII Protection](./pii-protection.md)
   - Implement automated redaction
   - Use data minimization

3. **Add content filtering**:
   - Read [Content Filtering](./content-filtering.md)
   - Implement dual-model moderation
   - Set up human review queues

4. **Test security**:
   - Follow [Security Audit Patterns](./security-audit-patterns.md)
   - Use LLMFuzzer and Garak
   - Run penetration tests

### For Compliance Teams

1. **Determine applicable frameworks**:
   - Review [Compliance Requirements](./compliance-requirements.md)
   - Identify GDPR, HIPAA, or SOC 2 requirements
   - Create implementation checklist

2. **Implement controls**:
   - Encryption (at rest and in transit)
   - Access controls and MFA
   - Audit logging
   - Incident response plan

3. **Vendor management**:
   - Review Claude Enterprise terms
   - Request BAA (HIPAA) or DPA (GDPR)
   - Verify SOC 2 reports

### For Security Teams

1. **Understand the threat landscape**:
   - Read [Incident Reports](./incident-reports.md)
   - Study attack patterns
   - Learn from real breaches

2. **Implement monitoring**:
   - Real-time anomaly detection
   - Prompt injection detection
   - Data exfiltration monitoring

3. **Regular audits**:
   - Quarterly security reviews
   - Penetration testing
   - Red team exercises

## Common Patterns at a Glance

### Multi-Layered Defense
```
User Input → Validation → Sanitization → LLM Gateway → Claude API
                ↓              ↓              ↓
           Block bad     Remove PII    Monitor/Log
```

### PII Protection Pipeline
```
Input → PII Detection → Redaction/Pseudonymization → LLM → De-pseudonymization → Output
```

### Content Moderation Flow
```
Content → Moderation Model → [PASS/BLOCK/REVIEW]
                ↓                    ↓
           Main LLM            Human Review
                ↓
         Output Check → User
```

### Compliance Architecture
```
Application Layer (GDPR consent, HIPAA minimization)
      ↓
Security Layer (Encryption, MFA, Access Control)
      ↓
LLM Gateway (PII/PHI detection, Audit logging)
      ↓
LLM Provider (DPA, BAA, SOC 2)
```

## Implementation Priorities

### Phase 1: Critical Security (Week 1-2)
- [ ] Input validation and sanitization
- [ ] Basic prompt injection defense
- [ ] PII detection and redaction
- [ ] Encryption (TLS 1.3)
- [ ] Basic audit logging

### Phase 2: Enhanced Protection (Week 3-4)
- [ ] Multi-layered defense implementation
- [ ] Content moderation
- [ ] Rate limiting
- [ ] Anomaly detection
- [ ] Incident response plan

### Phase 3: Compliance (Month 2-3)
- [ ] GDPR/HIPAA/SOC 2 requirements
- [ ] DPA/BAA with providers
- [ ] Data retention policies
- [ ] Privacy notices
- [ ] Consent management

### Phase 4: Advanced Security (Month 3-6)
- [ ] Red team testing
- [ ] Automated vulnerability scanning
- [ ] SOC 2 audit preparation
- [ ] Security training program
- [ ] Continuous monitoring

## Tools and Resources

### Security Testing Tools
- **LLMFuzzer**: Open-source fuzzing framework
- **Garak**: Red-teaming and assessment kit
- **Microsoft Presidio**: PII detection and anonymization
- **OWASP ZAP**: Web application security scanner

### Monitoring and DLP
- **Strac**: Cloud DLP for Claude
- **AWS Macie**: PII detection
- **Microsoft Purview**: Data governance
- **Splunk/ELK**: Log aggregation and analysis

### Compliance Tools
- **Vanta**: SOC 2 compliance automation
- **Drata**: Continuous compliance monitoring
- **OneTrust**: GDPR compliance management

## Key Metrics to Track

### Security Metrics
- **Prompt injection attempts detected**: Target: >95% detection
- **False positive rate**: Target: <5%
- **Mean time to detect (MTTD)**: Target: <5 minutes
- **Mean time to respond (MTTR)**: Target: <1 hour
- **PII exposure incidents**: Target: 0

### Compliance Metrics
- **Audit findings closed**: Target: 100% within 30 days
- **Training completion rate**: Target: 100% annually
- **Policy review frequency**: Target: Quarterly
- **Vendor assessment completion**: Target: 100% annually

### Operational Metrics
- **API availability**: Target: 99.9%
- **Response time**: Target: <500ms p95
- **Rate limit violations**: Monitor trends
- **Failed authentication attempts**: Monitor for patterns

## Cost Considerations

### Implementation Costs
- **PII detection tools**: $5k-$20k/year
- **DLP solutions**: $10k-$50k/year
- **Security testing**: $15k-$50k initial, $10k-$30k annual
- **Compliance (SOC 2)**: $25k-$50k initial, $10k-$30k annual
- **Monitoring tools**: $5k-$25k/year

### Incident Costs (if prevention fails)
- **Data breach remediation**: $100k-$5M
- **GDPR fines**: Up to €20M or 4% revenue
- **HIPAA fines**: $141-$2.1M per violation
- **Reputation damage**: Ongoing
- **Legal fees**: $50k-$2M

**ROI**: Prevention is 10-100x cheaper than incident response.

## Recent Updates and Trends

### November 2025
- Claude Desktop extensions security concerns identified
- Cursor IDE vulnerabilities patched
- Increased regulatory scrutiny on LLM providers

### Q1 2025
- Multiple major data breaches (OmniGPT, DeepSeek)
- ChatGPT ShadowLeak discovered and patched
- 100% jailbreak success demonstrated on some models
- Microsoft Copilot phishing attack demonstrated

### 2024
- OpenAI €15M GDPR fine
- Copy-paste injection exploits discovered
- OWASP LLM Top 10 updated

## Contributing

This documentation is maintained as part of the claude-codex project. To contribute:
1. Report security findings via private channels
2. Suggest improvements via pull requests
3. Share relevant incident reports
4. Update compliance requirements as regulations change

## Disclaimer

This documentation provides general guidance and should not be considered legal advice. Consult with security professionals and legal counsel for your specific use case. Security is a rapidly evolving field—stay updated with the latest threats and mitigations.

## Support and Questions

For questions or clarifications:
- Review the individual pattern documents
- Check real incident reports for context
- Consult OWASP LLM Top 10 for latest vulnerabilities
- Engage security professionals for implementation

---

**Remember**: Security is not a one-time implementation but an ongoing process. Regular audits, continuous monitoring, and staying informed about emerging threats are essential for maintaining secure LLM applications.
