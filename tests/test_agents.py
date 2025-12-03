import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent))

from src.agents.ingestor import IngestorAgent
from src.agents.parser_agent import ParserAgent
from src.agents.sast_agent import SASTAgent

class TestIngestorAgent:
    def test_process_single_file(self):
        ingestor = IngestorAgent()
        test_file = Path(__file__).parent / 'fixtures' / 'vulnerable' / 'vuln_sql_concat.py'
        files = ingestor.process_directory(str(test_file))
        
        assert len(files) == 1
        assert files[0]['extension'] == '.py'
        assert 'content' in files[0]
    
    def test_process_directory(self):
        ingestor = IngestorAgent()
        test_dir = Path(__file__).parent / 'fixtures' / 'vulnerable'
        files = ingestor.process_directory(str(test_dir))
        
        assert len(files) > 0
        assert all(f['extension'] == '.py' for f in files if f)

class TestParserAgent:
    def test_parse_python_file(self):
        parser = ParserAgent()
        ingestor = IngestorAgent()
        
        test_file = Path(__file__).parent / 'fixtures' / 'vulnerable' / 'vuln_exec.py'
        files = ingestor.process_directory(str(test_file))
        
        parsed = parser.parse_file(files[0])
        
        assert parsed is not None
        assert parsed['language'] == 'python'
        assert 'functions' in parsed
        assert len(parsed['functions']) > 0

class TestSASTAgent:
    def test_detect_hardcoded_creds(self):
        sast = SASTAgent()
        parser = ParserAgent()
        ingestor = IngestorAgent()
        
        test_file = Path(__file__).parent / 'fixtures' / 'vulnerable' / 'hardcoded_creds.py'
        files = ingestor.process_directory(str(test_file))
        parsed = parser.parse_file(files[0])
        
        findings = sast.scan(parsed)
        
        assert len(findings) > 0
        assert any(f.rule_id == 'PY001' for f in findings)
    
    def test_detect_sql_injection(self):
        sast = SASTAgent()
        parser = ParserAgent()
        ingestor = IngestorAgent()
        
        test_file = Path(__file__).parent / 'fixtures' / 'vulnerable' / 'vuln_sql_concat.py'
        files = ingestor.process_directory(str(test_file))
        parsed = parser.parse_file(files[0])
        
        findings = sast.scan(parsed)
        
        assert len(findings) > 0
        assert any(f.rule_id == 'PY002' for f in findings)
    
    def test_detect_eval_usage(self):
        sast = SASTAgent()
        parser = ParserAgent()
        ingestor = IngestorAgent()
        
        test_file = Path(__file__).parent / 'fixtures' / 'vulnerable' / 'vuln_exec.py'
        files = ingestor.process_directory(str(test_file))
        parsed = parser.parse_file(files[0])
        
        findings = sast.scan(parsed)
        
        assert len(findings) > 0
        assert any(f.rule_id == 'PY003' for f in findings)
    
    def test_no_false_positives_on_clean_code(self):
        sast = SASTAgent()
        parser = ParserAgent()
        ingestor = IngestorAgent()
        
        test_file = Path(__file__).parent / 'fixtures' / 'clean' / 'safe_sql.py'
        files = ingestor.process_directory(str(test_file))
        parsed = parser.parse_file(files[0])
        
        findings = sast.scan(parsed)
        
        # Should have no SQL injection findings
        assert not any(f.rule_id == 'PY002' for f in findings)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
