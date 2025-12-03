import re
from typing import List, Dict
from src.rules.python_rules import PYTHON_RULES
from src.models.finding import Finding, Severity

class SASTAgent:
    '''Static Application Security Testing Agent'''
    
    def __init__(self):
        self.rules = PYTHON_RULES
    
    def scan(self, parsed_data: Dict) -> List[Finding]:
        '''Scan parsed code for vulnerabilities'''
        if not parsed_data or parsed_data['language'] != 'python':
            return []
        
        findings = []
        content = parsed_data['content']
        lines = content.split('\n')
        
        for rule in self.rules:
            matches = rule.pattern.finditer(content)
            
            for match in matches:
                # Calculate line number
                line_num = content[:match.start()].count('\n') + 1
                
                # Extract code snippet (3 lines context)
                start_line = max(0, line_num - 2)
                end_line = min(len(lines), line_num + 1)
                snippet = '\n'.join(lines[start_line:end_line])
                
                finding = Finding(
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    severity=Severity[rule.severity],
                    cwe_id=rule.cwe_id,
                    file_path=parsed_data['file_path'],
                    line_number=line_num,
                    code_snippet=snippet,
                    description=rule.description
                )
                
                findings.append(finding)
        
        return findings
    
    def scan_multiple(self, parsed_files: List[Dict]) -> List[Finding]:
        '''Scan multiple files'''
        all_findings = []
        for parsed in parsed_files:
            if parsed:
                findings = self.scan(parsed)
                all_findings.extend(findings)
        return all_findings
