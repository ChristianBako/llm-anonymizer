"""Core anonymization logic using local LLM."""

import ollama
from typing import Optional
from .types import CodeFile, AnonymizationResult, AnonymizationConfig, ValidationResult
from .validator import ContentValidator


class CodeAnonymizer:
    """Handles code anonymization using local LLM."""
    
    def __init__(self, config: AnonymizationConfig) -> None:
        self.config = config
        self.validator = ContentValidator(config.validation) if config.validation else None
        
    def anonymize_code(self, code_file: CodeFile) -> AnonymizationResult:
        """Anonymize a code file using the local LLM with validation."""
        try:
            retry_count = 0
            max_retries = self.config.validation.max_retries if self.config.validation else 1
            
            while retry_count < max_retries:
                # Generate anonymized content
                prompt = self._build_prompt(code_file, retry_count)
                
                response = ollama.chat(
                    model=self.config.model_name,
                    messages=[
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    options={
                        'temperature': self.config.temperature
                    }
                )
                
                anonymized_content = response['message']['content']
                
                # Validate if validator is configured
                if self.validator:
                    validation_result = self.validator.validate_content(anonymized_content)
                    validation_result.retry_count = retry_count
                    
                    if validation_result.passed:
                        return AnonymizationResult(
                            original_file=code_file,
                            anonymized_content=anonymized_content,
                            success=True,
                            validation_result=validation_result
                        )
                    
                    retry_count += 1
                    
                    if retry_count >= max_retries:
                        return AnonymizationResult(
                            original_file=code_file,
                            anonymized_content=anonymized_content,
                            success=False,
                            validation_result=validation_result,
                            error_message=f"Validation failed after {max_retries} attempts. Found banned strings: {', '.join(validation_result.found_banned_strings)}"
                        )
                else:
                    # No validation, return immediately
                    return AnonymizationResult(
                        original_file=code_file,
                        anonymized_content=anonymized_content,
                        success=True
                    )
            
        except Exception as e:
            return AnonymizationResult(
                original_file=code_file,
                anonymized_content="",
                success=False,
                error_message=str(e)
            )
    
    def _build_prompt(self, code_file: CodeFile, retry_count: int = 0) -> str:
        """Build the anonymization prompt for the LLM."""
        base_prompt = """Please anonymize the following code by replacing:
- Variable names with generic names (var1, var2, etc.)
- Function names with generic names (func1, func2, etc.)
- Class names with generic names (Class1, Class2, etc.)
- String literals with placeholder text (unless they're important for understanding)
- Comments with generic comments (unless they explain important logic)

Preserve:
- Code structure and logic
- Control flow
- Data types
- Import statements and library calls
- Syntax and formatting

Code to anonymize:

```{language}
{code}
```

Return only the anonymized code without explanations:"""

        # Add specific banned string removal instructions for retries
        if retry_count > 0 and self.validator:
            banned_strings_list = ", ".join(f'"{s}"' for s in self.validator.config.banned_strings)
            retry_prompt = f"""

CRITICAL: This is attempt #{retry_count + 1}. The previous attempt contained banned strings that MUST be completely removed.

BANNED STRINGS THAT MUST NOT APPEAR IN YOUR OUTPUT:
{banned_strings_list}

Double-check your output and ensure NONE of these strings appear anywhere in the anonymized code, including in:
- Variable names
- Function names  
- Class names
- String literals
- Comments
- Any other text

Replace any occurrence of these banned strings with completely generic alternatives."""
            
            base_prompt += retry_prompt
        
        return base_prompt.format(
            language=code_file.language,
            code=code_file.content
        )