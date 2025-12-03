import ast
from typing import Dict, List, Optional

class ParserAgent:
    '''Parses source code and builds AST'''
    
    def __init__(self):
        self.parsed_files = []
    
    def parse_file(self, file_data: Dict) -> Optional[Dict]:
        '''Parse Python file and extract structure'''
        if file_data['extension'] != '.py':
            return self._parse_non_python(file_data)
        
        try:
            tree = ast.parse(file_data['content'], filename=file_data['name'])
            
            return {
                'file_path': file_data['path'],
                'language': 'python',
                'ast': tree,
                'content': file_data['content'],
                'functions': self._extract_functions(tree),
                'imports': self._extract_imports(tree),
                'variables': self._extract_variables(tree)
            }
        except SyntaxError as e:
            print(f'Syntax error in {file_data["path"]}: {e}')
            return None
    
    def _extract_functions(self, tree: ast.AST) -> List[Dict]:
        '''Extract function definitions'''
        functions = []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append({
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args]
                })
        return functions
    
    def _extract_imports(self, tree: ast.AST) -> List[str]:
        '''Extract import statements'''
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        return imports
    
    def _extract_variables(self, tree: ast.AST) -> List[Dict]:
        '''Extract variable assignments'''
        variables = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append({
                            'name': target.id,
                            'line': node.lineno
                        })
        return variables
    
    def _parse_non_python(self, file_data: Dict) -> Dict:
        '''Basic parsing for non-Python files'''
        return {
            'file_path': file_data['path'],
            'language': file_data['extension'][1:],  # Remove dot
            'content': file_data['content'],
            'ast': None
        }
