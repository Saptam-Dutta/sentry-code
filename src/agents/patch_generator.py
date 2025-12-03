from typing import Optional, Dict
from src.models.finding import Finding
import difflib

class PatchGeneratorAgent:
    '''Generates code patches and diffs'''
    
    def generate_patch(self, finding: Finding) -> Optional[Dict]:
        '''Generate patch from LLM-suggested fix'''
        if not finding.fixed_code:
            return None
        
        try:
            # Read original file
            with open(finding.file_path, 'r', encoding='utf-8') as f:
                original_lines = f.readlines()
            
            # Create patched version
            patched_lines = original_lines.copy()
            
            # Simple line replacement (for demonstration)
            # In production, use more sophisticated AST-based patching
            target_line = finding.line_number - 1
            if 0 <= target_line < len(patched_lines):
                patched_lines[target_line] = finding.fixed_code + '\n'
            
            # Generate unified diff
            diff = list(difflib.unified_diff(
                original_lines,
                patched_lines,
                fromfile=f'{finding.file_path} (original)',
                tofile=f'{finding.file_path} (patched)',
                lineterm=''
            ))
            
            return {
                'finding_id': finding.rule_id,
                'file_path': finding.file_path,
                'original_code': finding.code_snippet,
                'patched_code': finding.fixed_code,
                'diff': '\n'.join(diff),
                'validated': self._validate_patch(finding.fixed_code)
            }
        
        except Exception as e:
            print(f'Patch generation error: {e}')
            return None
    
    def _validate_patch(self, code: str) -> bool:
        '''Basic syntax validation'''
        try:
            compile(code, '<string>', 'exec')
            return True
        except SyntaxError:
            return False
    
    def apply_patch(self, patch: Dict) -> bool:
        '''Apply patch to file (use with caution!)'''
        try:
            with open(patch['file_path'], 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Apply the patch (simplified)
            # In production, use proper patch application logic
            
            with open(patch['file_path'] + '.patched', 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            return True
        except Exception as e:
            print(f'Patch application error: {e}')
            return False
