from typing import Dict, List
from src.agents.ingestor import IngestorAgent
from src.agents.parser_agent import ParserAgent
from src.agents.sast_agent import SASTAgent
from src.agents.llm_reasoner import LLMReasonerAgent
from src.agents.patch_generator import PatchGeneratorAgent
from src.models.finding import ScanResult, Finding

class SecurityReviewOrchestrator:
    '''Main orchestrator coordinating all agents'''
    
    def __init__(self, llm_model: str = 'llama3.2:latest'):
        print('Initializing SENTRY-CODE agents...')
        self.ingestor = IngestorAgent()
        self.parser = ParserAgent()
        self.sast = SASTAgent()
        self.reasoner = LLMReasonerAgent(model_name=llm_model)
        self.patcher = PatchGeneratorAgent()
        print('All agents initialized successfully!')
    
    def analyze_repository(self, repo_path: str, use_llm: bool = True) -> ScanResult:
        '''Main workflow: orchestrate all agents'''
        
        print(f'\n[1/6] Ingesting files from: {repo_path}')
        files = self.ingestor.process_directory(repo_path)
        print(f'  Found {len(files)} files')
        
        print('\n[2/6] Parsing source code...')
        parsed_files = []
        for file in files:
            if file:
                parsed = self.parser.parse_file(file)
                if parsed:
                    parsed_files.append(parsed)
        print(f'  Parsed {len(parsed_files)} files successfully')
        
        print('\n[3/6] Running SAST analysis...')
        findings = self.sast.scan_multiple(parsed_files)
        print(f'  Detected {len(findings)} potential vulnerabilities')
        
        if use_llm and findings:
            print('\n[4/6] Analyzing with LLM (this may take a few minutes)...')
            findings = self.reasoner.batch_analyze(findings, max_findings=10)
            print('  LLM analysis complete')
        else:
            print('\n[4/6] Skipping LLM analysis')
        
        print('\n[5/6] Generating patches...')
        patches = []
        for finding in findings:
            if finding.fixed_code:
                patch = self.patcher.generate_patch(finding)
                if patch:
                    patches.append(patch)
        print(f'  Generated {len(patches)} patches')
        
        print('\n[6/6] Preparing results...')
        result = self._build_scan_result(findings, len(files))
        print(f'  Scan complete! Total findings: {result.total_findings}')
        
        return result
    
    def _build_scan_result(self, findings: List[Finding], files_count: int) -> ScanResult:
        '''Build final scan result'''
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for finding in findings:
            severity_counts[finding.severity.value] += 1
        
        return ScanResult(
            total_findings=len(findings),
            findings=findings,
            files_scanned=files_count,
            severity_counts=severity_counts
        )

