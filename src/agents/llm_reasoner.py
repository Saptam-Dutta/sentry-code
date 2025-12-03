import ollama
from typing import Dict, List
from src.models.finding import Finding
import json
import re

class LLMReasonerAgent:
    """Uses Ollama LLM for vulnerability analysis"""
    
    def __init__(self, model_name: str = "llama3.2:latest"):
        self.model = model_name
        self.client = ollama
    
    def analyze_vulnerability(self, finding: Finding) -> Finding:
        """Analyze vulnerability and generate explanation"""
        
        prompt = self._build_analysis_prompt(finding)
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a security code reviewer. Provide clear, concise security advice in the exact format requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.3,
                    "num_predict": 400
                }
            )
            
            # Parse LLM response
            analysis = self._parse_llm_response(response["message"]["content"])
            
            # Update finding with LLM insights
            finding.explanation = analysis.get("explanation", "Unable to generate explanation")
            finding.impact = analysis.get("impact", "Unknown impact")
            finding.remediation_steps = analysis.get("remediation_steps", [])
            finding.fixed_code = analysis.get("fixed_code", None)
            finding.confidence = 0.85
            
        except Exception as e:
            print(f"LLM analysis error: {e}")
            finding.explanation = f"Error during analysis: {str(e)}"
            finding.confidence = 0.0
        
        return finding
    
    def _build_analysis_prompt(self, finding: Finding) -> str:
        """Build prompt for LLM"""
        return f"""Analyze this security vulnerability and respond in the EXACT format shown:

Vulnerability: {finding.rule_name}
Severity: {finding.severity.value}
CWE: {finding.cwe_id}
Description: {finding.description}

Code (Line {finding.line_number}):
{finding.code_snippet}

Provide your analysis in this EXACT format:

EXPLANATION: [2-3 sentences explaining why this is vulnerable]

IMPACT: [1-2 sentences on what an attacker could do]

REMEDIATION:
1. [First step to fix]
2. [Second step to fix]
3. [Third step to fix]

FIXED_CODE:
[Show corrected code here]

Remember: Follow the format exactly with those section headers."""
    
    def _parse_llm_response(self, response: str) -> Dict:
        """Parse structured LLM response with improved regex"""
        analysis = {
            "explanation": "",
            "impact": "",
            "remediation_steps": [],
            "fixed_code": None
        }
        
        try:
            # Extract explanation - more flexible matching
            expl_match = re.search(r"EXPLANATION:\s*(.+?)(?=\n\s*IMPACT:|$)", response, re.DOTALL | re.IGNORECASE)
            if expl_match:
                analysis["explanation"] = expl_match.group(1).strip()
            
            # Extract impact
            impact_match = re.search(r"IMPACT:\s*(.+?)(?=\n\s*REMEDIATION:|$)", response, re.DOTALL | re.IGNORECASE)
            if impact_match:
                analysis["impact"] = impact_match.group(1).strip()
            
            # Extract remediation steps
            rem_match = re.search(r"REMEDIATION:\s*(.+?)(?=\n\s*FIXED_CODE:|$)", response, re.DOTALL | re.IGNORECASE)
            if rem_match:
                rem_text = rem_match.group(1).strip()
                # Parse numbered or bulleted steps
                steps = []
                for line in rem_text.split("\n"):
                    line = line.strip()
                    if line and (line[0].isdigit() or line.startswith("-") or line.startswith("*")):
                        # Remove numbering/bullets
                        step = re.sub(r"^\d+\.\s*|\-\s*|\*\s*", "", line)
                        if step:
                            steps.append(step)
                analysis["remediation_steps"] = steps
            
            # Extract fixed code - look for code blocks or just the FIXED_CODE section
            code_match = re.search(r"FIXED_CODE:\s*(.+?)$", response, re.DOTALL | re.IGNORECASE)
            if code_match:
                code_text = code_match.group(1).strip()
                # Remove markdown code blocks if present
                code_text = re.sub(r"```\w*\n?", "", code_text)
                code_text = re.sub(r"```$", "", code_text)
                if code_text:
                    analysis["fixed_code"] = code_text.strip()
        
        except Exception as e:
            print(f"Response parsing error: {e}")
            # Fallback: use raw response as explanation
            if not analysis["explanation"]:
                analysis["explanation"] = response[:200] + "..." if len(response) > 200 else response
        
        return analysis
    
    def batch_analyze(self, findings: List[Finding], max_findings: int = 10) -> List[Finding]:
        """Analyze multiple findings (limit for performance)"""
        analyzed = []
        
        # Prioritize by severity
        sorted_findings = sorted(
            findings, 
            key=lambda x: ["LOW", "MEDIUM", "HIGH", "CRITICAL"].index(x.severity.value),
            reverse=True
        )
        
        for i, finding in enumerate(sorted_findings[:max_findings]):
            print(f"Analyzing finding {i+1}/{min(max_findings, len(sorted_findings))}...")
            analyzed_finding = self.analyze_vulnerability(finding)
            analyzed.append(analyzed_finding)
        
        # Add remaining findings without LLM analysis
        for finding in sorted_findings[max_findings:]:
            finding.explanation = "Analysis skipped (batch limit reached)"
            analyzed.append(finding)
        
        return analyzed
