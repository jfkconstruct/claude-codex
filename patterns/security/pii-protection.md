# PII Protection Patterns for LLM Applications

## Overview

Protecting Personally Identifiable Information (PII) is critical when using LLMs and APIs like Claude. Improper handling can lead to regulatory violations, data breaches, and loss of user trust.

**Key Principle**: The safest data is the data never transmitted. Minimize PII exposure at every stage.

## Core Protection Strategies

### 1. Automated Redaction

**Pattern**: Pre-processing PII removal

Automatically remove sensitive information before sending to LLMs.

**Implementation**:
```python
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def redact_pii(text):
    # Detect PII entities
    results = analyzer.analyze(
        text=text,
        entities=["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER",
                 "CREDIT_CARD", "SSN", "IP_ADDRESS"],
        language='en'
    )

    # Redact detected entities
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )

    return anonymized.text
```

**Benefits**:
- Minimizes exposure risk
- Works even if data is inadvertently shared
- Automated and consistent
- Can be reversed for authorized use cases

**Tools**:
- Microsoft Presidio (open source)
- OneShield
- Strac DLP
- AWS Comprehend PII detection

### 2. Pseudonymization

**Pattern**: Reversible placeholder substitution

Replace sensitive information with non-identifiable placeholders while maintaining data utility.

**Example**:
```
Original: "John Smith's SSN is 123-45-6789"
Pseudonymized: "PERSON_001's SSN is SSN_001"

Mapping (stored securely):
{
  "PERSON_001": "John Smith",
  "SSN_001": "123-45-6789"
}
```

**Implementation**:
```python
import uuid

class Pseudonymizer:
    def __init__(self):
        self.mapping = {}
        self.reverse_mapping = {}

    def pseudonymize(self, value, entity_type):
        if value in self.mapping:
            return self.mapping[value]

        # Generate unique placeholder
        placeholder = f"{entity_type}_{uuid.uuid4().hex[:8]}"
        self.mapping[value] = placeholder
        self.reverse_mapping[placeholder] = value

        return placeholder

    def de_pseudonymize(self, placeholder):
        return self.reverse_mapping.get(placeholder, placeholder)
```

**Benefits**:
- Maintains data utility for analysis
- Reversible for authorized users
- GDPR-compliant
- Reduces risk of harm to data subjects

**Use cases**:
- Analytics and reporting
- Model training data
- Testing and development
- Cross-system data sharing

### 3. Anonymization

**Pattern**: Irreversible PII removal

Completely remove or transform data so individuals cannot be re-identified.

**Techniques**:
- **Generalization**: "Age 34" → "Age 30-40"
- **Suppression**: Remove specific identifiers entirely
- **Noise addition**: Add random variations
- **K-anonymity**: Ensure each record is indistinguishable from k-1 others

**When to use**:
- Training datasets
- Public data releases
- Long-term storage
- Situations where re-identification is never needed

**Caution**: True anonymization is difficult. Combining datasets can enable re-identification.

### 4. Data Minimization

**Pattern**: Only send what's necessary

Avoid sending any more data to LLM APIs than required for the task.

**Checklist**:
- [ ] Remove unnecessary fields from requests
- [ ] Truncate verbose data
- [ ] Use aggregated summaries instead of raw data
- [ ] Filter out PII-heavy sections
- [ ] Apply principle of least privilege

**Example**:
```python
# ❌ Bad: Sending full user profile
user_data = {
    "name": "John Smith",
    "email": "john@example.com",
    "ssn": "123-45-6789",
    "address": "123 Main St",
    "phone": "555-1234",
    "purchase_history": [...]
}
llm.analyze(user_data)

# ✅ Good: Sending only necessary data
purchase_summary = {
    "user_id": "hashed_id_xyz",
    "total_purchases": 15,
    "avg_purchase_value": 45.67,
    "last_purchase_date": "2025-01"
}
llm.analyze(purchase_summary)
```

### 5. Masking Techniques

**Pattern**: Replace sensitive tokens with placeholders

Strip or mask sensitive identifiers before sending to the model.

**Common masking patterns**:
```
Email: user@domain.com → [EMAIL]
Phone: 555-123-4567 → [PHONE]
SSN: 123-45-6789 → [SSN]
Credit Card: 4111-1111-1111-1111 → [CREDIT_CARD]
Name: John Smith → [NAME]
Address: 123 Main St → [ADDRESS]
```

**Context-aware preprocessing**:
```python
import re

def mask_sensitive_data(text):
    patterns = {
        'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'PHONE': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'SSN': r'\b\d{3}-\d{2}-\d{4}\b',
        'CREDIT_CARD': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
    }

    masked_text = text
    for entity_type, pattern in patterns.items():
        masked_text = re.sub(pattern, f'[{entity_type}]', masked_text)

    return masked_text
```

### 6. DLP (Data Loss Prevention) Integration

**Pattern**: Automated enforcement at API boundary

Implement guardrails to ensure no confidential tokens reach the model unchecked.

**Architecture**:
```
User Input → DLP Scanner → Policy Check → LLM API
                ↓
        [Block / Sanitize / Allow]
```

**DLP capabilities**:
- Real-time scanning of requests
- Pattern-based detection
- ML-based classification
- Policy enforcement
- Audit logging
- Automatic blocking/sanitization

**Example tools**:
- Strac Cloud DLP
- Microsoft Purview
- Google Cloud DLP API
- AWS Macie

## Claude API Data Privacy Policies

### Free vs. Paid Services

**Free/Consumer Claude**:
- May use conversations for model training
- Limited privacy protections
- ⚠️ **Never use for sensitive data**

**Claude Enterprise/API**:
- Anthropic does NOT train models on customer content from paid services
- Commercial terms with stricter confidentiality
- Enterprise-grade privacy protections
- Business Associate Agreements (BAA) available for HIPAA

### Best Practices for Claude API

1. **Use Enterprise plan** for sensitive data
2. **Review contracts**: Ensure Commercial Terms prohibit training on your data
3. **Request BAA** if handling healthcare data
4. **Verify DPA** (Data Processing Agreement) for GDPR compliance
5. **Enable audit logging** to track data access

## Implementation Patterns

### Pattern: Preprocessing Pipeline

```python
class PIIProtectionPipeline:
    def __init__(self):
        self.redactor = PIIRedactor()
        self.pseudonymizer = Pseudonymizer()
        self.dlp_scanner = DLPScanner()

    def process_for_llm(self, text, protection_level='high'):
        # Stage 1: DLP scan
        scan_result = self.dlp_scanner.scan(text)
        if scan_result.has_violations():
            log_security_event(scan_result)
            if scan_result.severity == 'critical':
                raise SecurityException("Critical PII detected")

        # Stage 2: Redaction or pseudonymization
        if protection_level == 'maximum':
            processed = self.redactor.redact(text)
        elif protection_level == 'high':
            processed = self.pseudonymizer.pseudonymize(text)
        else:
            processed = self.mask_pii(text)

        # Stage 3: Final validation
        if self.contains_pii(processed):
            raise SecurityException("PII still present after processing")

        return processed

    def restore_response(self, llm_response, original_context):
        # De-pseudonymize if needed
        return self.pseudonymizer.de_pseudonymize(llm_response)
```

### Pattern: Secure Envelope

```python
class SecureEnvelope:
    """Separate PII from content sent to LLM"""

    def prepare_request(self, content_with_pii):
        # Extract PII references
        pii_refs = self.extract_pii_references(content_with_pii)

        # Replace with tokens
        sanitized_content = self.replace_with_tokens(
            content_with_pii,
            pii_refs
        )

        # Store mapping securely
        session_id = self.store_mapping(pii_refs)

        return {
            'content': sanitized_content,
            'session_id': session_id
        }

    def reconstruct_response(self, llm_response, session_id):
        # Retrieve mapping
        pii_refs = self.get_mapping(session_id)

        # Restore PII where appropriate
        return self.restore_tokens(llm_response, pii_refs)
```

## Compliance Considerations

### GDPR
- Pseudonymization is encouraged by GDPR
- Reduces risk of harm to data subjects
- Must document processing activities
- Right to erasure applies to mappings

### HIPAA
- PHI must be encrypted in transit and at rest
- Business Associate Agreement required
- Minimum necessary standard applies (data minimization)
- Audit logs required

### SOC 2
- Document PII handling procedures
- Implement access controls
- Regular security assessments
- Incident response procedures

## Security Checklist

- [ ] Never include PII in prompts unnecessarily
- [ ] Use automated PII detection (Presidio, etc.)
- [ ] Implement DLP at API boundaries
- [ ] Choose appropriate protection: redaction vs. pseudonymization vs. anonymization
- [ ] Use Claude Enterprise for sensitive data
- [ ] Verify contracts prohibit training on your data
- [ ] Request BAA for HIPAA compliance
- [ ] Implement secure mapping storage for pseudonymization
- [ ] Encrypt PII mappings at rest
- [ ] Apply principle of least privilege
- [ ] Log all PII access
- [ ] Regular security audits
- [ ] Employee training on PII handling
- [ ] Incident response plan for data exposure

## Common Pitfalls

1. **Assuming API providers don't store data**: Always verify contracts
2. **Incomplete redaction**: Use comprehensive PII detection
3. **Storing plaintext mappings**: Encrypt pseudonymization mappings
4. **Over-redaction**: Balance security with utility
5. **Forgetting about metadata**: Timestamps, IPs can be identifying
6. **Cross-dataset correlation**: Multiple "anonymized" datasets can enable re-identification
7. **Not testing**: Regular pen testing for PII leaks

## References

- Strac: Secure Sensitive Data in LLM Prompts
- Microsoft Presidio Documentation
- GDPR Article 25: Data Protection by Design
- NIST Privacy Framework
- Anthropic Commercial Terms
- HIPAA Security Rule

## Related Patterns

- [Compliance Requirements](./compliance-requirements.md)
- [Security Audit Patterns](./security-audit-patterns.md)
- [Prompt Injection Defense](./prompt-injection-defense.md)
