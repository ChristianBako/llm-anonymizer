"""File processing utilities for different code types."""

import os
from pathlib import Path
from typing import List, Optional
from .types import CodeFile, FileType


class FileProcessor:
    """Handles file reading and type detection."""
    
    LANGUAGE_EXTENSIONS = {
        '.py': ('python', FileType.PYTHON),
        '.js': ('javascript', FileType.JAVASCRIPT),
        '.ts': ('typescript', FileType.TYPESCRIPT),
        '.jsx': ('javascript', FileType.JAVASCRIPT),
        '.tsx': ('typescript', FileType.TYPESCRIPT),
        '.java': ('java', FileType.JAVA),
        '.cpp': ('cpp', FileType.CPP),
        '.cc': ('cpp', FileType.CPP),
        '.cxx': ('cpp', FileType.CPP),
        '.c': ('c', FileType.CPP),
        '.h': ('cpp', FileType.CPP),
        '.hpp': ('cpp', FileType.CPP),
        '.rs': ('rust', FileType.RUST),
        '.go': ('go', FileType.GO),
    }
    
    def process_file(self, file_path: str) -> Optional[CodeFile]:
        """Process a single file and return a CodeFile object."""
        try:
            path = Path(file_path)
            
            if not path.exists():
                return None
                
            if not path.is_file():
                return None
                
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            language, file_type = self._detect_language(path)
            
            return CodeFile(
                path=str(path),
                content=content,
                file_type=file_type,
                language=language
            )
            
        except Exception:
            return None
    
    def process_directory(self, directory_path: str, recursive: bool = True) -> List[CodeFile]:
        """Process all code files in a directory."""
        code_files = []
        path = Path(directory_path)
        
        if not path.exists() or not path.is_dir():
            return code_files
            
        pattern = '**/*' if recursive else '*'
        
        for file_path in path.glob(pattern):
            if file_path.is_file() and self._is_code_file(file_path):
                code_file = self.process_file(str(file_path))
                if code_file:
                    code_files.append(code_file)
                    
        return code_files
    
    def _detect_language(self, path: Path) -> tuple[str, FileType]:
        """Detect the programming language from file extension."""
        extension = path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(extension, ('text', FileType.OTHER))
    
    def _is_code_file(self, path: Path) -> bool:
        """Check if a file is a supported code file."""
        extension = path.suffix.lower()
        return extension in self.LANGUAGE_EXTENSIONS