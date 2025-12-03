import os
from pathlib import Path
from typing import List, Dict

class IngestorAgent:
    '''Handles file ingestion and validation'''
    
    SUPPORTED_EXTENSIONS = {'.py', '.js', '.cs'}
    
    def __init__(self):
        self.files_processed = []
    
    def process_directory(self, path: str) -> List[Dict]:
        '''Process all supported files in directory'''
        path_obj = Path(path)
        files = []
        
        if path_obj.is_file():
            if path_obj.suffix in self.SUPPORTED_EXTENSIONS:
                files.append(self._process_file(path_obj))
        else:
            for file_path in path_obj.rglob('*'):
                if file_path.is_file() and file_path.suffix in self.SUPPORTED_EXTENSIONS:
                    files.append(self._process_file(file_path))
        
        self.files_processed = files
        return files
    
    def _process_file(self, file_path: Path) -> Dict:
        '''Extract file metadata and content'''
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return {
                'path': str(file_path),
                'name': file_path.name,
                'extension': file_path.suffix,
                'content': content,
                'lines': content.count('\n') + 1,
                'size': len(content)
            }
        except Exception as e:
            print(f'Error processing {file_path}: {e}')
            return None
    
    def get_statistics(self) -> Dict:
        '''Return ingestion statistics'''
        return {
            'total_files': len(self.files_processed),
            'total_lines': sum(f['lines'] for f in self.files_processed if f),
            'by_extension': self._count_by_extension()
        }
    
    def _count_by_extension(self) -> Dict:
        counts = {}
        for file in self.files_processed:
            if file:
                ext = file['extension']
                counts[ext] = counts.get(ext, 0) + 1
        return counts
