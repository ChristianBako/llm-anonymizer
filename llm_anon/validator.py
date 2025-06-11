"""Content validation for anonymized code."""

import re
from typing import List, Set
from .types import ValidationConfig, ValidationResult


class ContentValidator:
    """Validates anonymized content against banned strings."""
    
    def __init__(self, config: ValidationConfig) -> None:
        self.config = config
        
    def validate_content(self, content: str) -> ValidationResult:
        """Validate content against banned strings."""
        found_banned = []
        
        for banned_string in self.config.banned_strings:
            if self._contains_banned_string(content, banned_string):
                found_banned.append(banned_string)
        
        return ValidationResult(
            passed=len(found_banned) == 0,
            found_banned_strings=found_banned
        )
    
    def _contains_banned_string(self, content: str, banned_string: str) -> bool:
        """Check if content contains a banned string."""
        search_content = content if self.config.case_sensitive else content.lower()
        search_string = banned_string if self.config.case_sensitive else banned_string.lower()
        
        # Use word boundaries for more accurate matching
        pattern = r'\b' + re.escape(search_string) + r'\b'
        
        return bool(re.search(pattern, search_content))
    
    @classmethod
    def load_from_file(cls, file_path: str, case_sensitive: bool = True, max_retries: int = 3) -> 'ContentValidator':
        """Load validation config from a file."""
        banned_strings = set()
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):  # Skip empty lines and comments
                        banned_strings.add(line)
        except FileNotFoundError:
            raise FileNotFoundError(f"Validation config file not found: {file_path}")
        
        config = ValidationConfig(
            banned_strings=banned_strings,
            case_sensitive=case_sensitive,
            max_retries=max_retries
        )
        
        return cls(config)