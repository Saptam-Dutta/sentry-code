import re
from dataclasses import dataclass
from typing import Pattern

@dataclass
class VulnerabilityRule:
    rule_id: str
    name: str
    severity: str
    cwe_id: str
    pattern: Pattern
    description: str
    remediation: str

PYTHON_RULES = [
    VulnerabilityRule(
        rule_id="PY001",
        name="Hardcoded Credentials",
        severity="CRITICAL",
        cwe_id="CWE-798",
        pattern=re.compile(
            r"(password|passwd|pwd|secret|api_key|token|access_key)\s*=\s*[\"'][^\"']{8,}[\"']",
            re.IGNORECASE
        ),
        description="Hardcoded credentials found in source code",
        remediation="Use environment variables or secure vaults (e.g., .env files, AWS Secrets Manager)"
    ),
    
    VulnerabilityRule(
        rule_id="PY002",
        name="SQL Injection Risk",
        severity="CRITICAL",
        cwe_id="CWE-89",
        pattern=re.compile(
            r"(query\s*=\s*.*\s*\+\s*.*|cursor\.execute\s*\(\s*[\"'].*\+|execute\s*\(\s*[\"'].*\+|query\s*=\s*f[\"'].*SELECT)",
            re.MULTILINE | re.IGNORECASE
        ),
        description="SQL query uses string concatenation or formatting",
        remediation="Use parameterized queries with placeholders (?)"
    ),
    
    VulnerabilityRule(
        rule_id="PY003",
        name="Code Injection via eval()",
        severity="CRITICAL",
        cwe_id="CWE-95",
        pattern=re.compile(r"\beval\s*\("),
        description="Dangerous use of eval() function",
        remediation="Use ast.literal_eval() for safe evaluation or validate input strictly"
    ),
    
    VulnerabilityRule(
        rule_id="PY004",
        name="Disabled SSL Verification",
        severity="HIGH",
        cwe_id="CWE-295",
        pattern=re.compile(r"verify\s*=\s*False"),
        description="SSL/TLS certificate verification disabled",
        remediation="Remove verify=False or use proper certificate validation"
    ),
    
    VulnerabilityRule(
        rule_id="PY005",
        name="Command Injection",
        severity="CRITICAL",
        cwe_id="CWE-78",
        pattern=re.compile(r"os\.system\s*\(.*[+]|subprocess\.call\s*\(.*[+]"),
        description="Command injection via unsanitized input",
        remediation="Use subprocess with list arguments and avoid shell=True"
    ),
    
    VulnerabilityRule(
        rule_id="PY006",
        name="Unsafe Deserialization",
        severity="CRITICAL",
        cwe_id="CWE-502",
        pattern=re.compile(r"pickle\.loads?\s*\("),
        description="Unsafe deserialization of untrusted data",
        remediation="Use JSON or validate pickle sources, never unpickle untrusted data"
    ),
    
    VulnerabilityRule(
        rule_id="PY007",
        name="Weak Cryptographic Hash",
        severity="MEDIUM",
        cwe_id="CWE-327",
        pattern=re.compile(r"hashlib\.(md5|sha1)\s*\("),
        description="Use of weak cryptographic hash function",
        remediation="Use SHA-256 or stronger: hashlib.sha256()"
    ),
    
    VulnerabilityRule(
        rule_id="PY008",
        name="Debug Mode Enabled",
        severity="MEDIUM",
        cwe_id="CWE-489",
        pattern=re.compile(r"debug\s*=\s*True"),
        description="Debug mode enabled in production",
        remediation="Set debug=False in production environments"
    ),
]
