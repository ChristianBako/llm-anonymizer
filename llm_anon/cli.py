"""CLI interface for the LLM anonymizer."""

import click
import sys
from pathlib import Path
from typing import Optional

from .types import AnonymizationConfig
from .anonymizer import CodeAnonymizer
from .file_processor import FileProcessor
from .validator import ContentValidator


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Output file or directory')
@click.option('--model', '-m', default='llama3.2', help='LLM model to use for anonymization')
@click.option('--temperature', '-t', default=0.1, type=float, help='Temperature for LLM generation')
@click.option('--preserve-comments', is_flag=True, help='Preserve comments in code')
@click.option('--preserve-strings', is_flag=True, help='Preserve string literals')
@click.option('--recursive', '-r', is_flag=True, help='Process directories recursively')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.option('--validation-config', type=click.Path(exists=True), help='Path to validation config file with banned strings')
@click.option('--max-retries', default=3, type=int, help='Maximum retries for validation failures')
def main(
    input_path: str,
    output: Optional[str],
    model: str,
    temperature: float,
    preserve_comments: bool,
    preserve_strings: bool,
    recursive: bool,
    verbose: bool,
    validation_config: Optional[str],
    max_retries: int
) -> None:
    """Anonymize code files using a local LLM.
    
    \b
    EXAMPLES:
      llm-anon code.py                              # Anonymize single file to stdout
      llm-anon code.py -o clean.py                  # Save anonymized output
      llm-anon src/ -r -o clean_src/                # Process entire directory
      llm-anon code.py --validation-config banned.txt  # Use validation to ensure secrets removed
      llm-anon api.py -m codellama -t 0.3           # Use different model with more creativity
    
    \b
    VALIDATION CONFIG:
    Create a text file with banned strings (one per line):
      echo "MyCompany" > banned.txt
      echo "secret_api_key" >> banned.txt
      echo "internal.company.com" >> banned.txt
    
    \b
    REQUIREMENTS:
    - Ollama must be running locally (ollama serve)
    - Model must be installed (ollama pull llama3.2)
    """
    
    # Load validation config if provided
    validation = None
    if validation_config:
        try:
            validator = ContentValidator.load_from_file(validation_config, max_retries=max_retries)
            validation = validator.config
            if verbose:
                click.echo(f"Loaded validation config: {len(validation.banned_strings)} banned strings")
        except Exception as e:
            click.echo(f"Error loading validation config: {e}", err=True)
            sys.exit(1)
    
    config = AnonymizationConfig(
        preserve_comments=preserve_comments,
        preserve_strings=preserve_strings,
        model_name=model,
        temperature=temperature,
        validation=validation
    )
    
    anonymizer = CodeAnonymizer(config)
    processor = FileProcessor()
    
    input_path_obj = Path(input_path)
    
    if input_path_obj.is_file():
        # Process single file
        code_file = processor.process_file(input_path)
        if not code_file:
            click.echo(f"Error: Could not process file {input_path}", err=True)
            sys.exit(1)
            
        if verbose:
            click.echo(f"Processing file: {code_file.path}")
            
        result = anonymizer.anonymize_code(code_file)
        
        if not result.success:
            click.echo(f"Error anonymizing file: {result.error_message}", err=True)
            if result.validation_result and not result.validation_result.passed:
                click.echo(f"Validation failed after {result.validation_result.retry_count + 1} attempts", err=True)
                click.echo(f"Found banned strings: {', '.join(result.validation_result.found_banned_strings)}", err=True)
            sys.exit(1)
            
        # Output result
        if output:
            with open(output, 'w', encoding='utf-8') as f:
                f.write(result.anonymized_content)
            if verbose:
                click.echo(f"Anonymized code written to {output}")
        else:
            click.echo(result.anonymized_content)
            
    elif input_path_obj.is_dir():
        # Process directory
        code_files = processor.process_directory(input_path, recursive=recursive)
        
        if not code_files:
            click.echo(f"No code files found in {input_path}", err=True)
            sys.exit(1)
            
        if verbose:
            click.echo(f"Found {len(code_files)} code files")
            
        if output:
            output_path = Path(output)
            output_path.mkdir(parents=True, exist_ok=True)
        
        for code_file in code_files:
            if verbose:
                click.echo(f"Processing: {code_file.path}")
                
            result = anonymizer.anonymize_code(code_file)
            
            if not result.success:
                click.echo(f"Error anonymizing {code_file.path}: {result.error_message}", err=True)
                if result.validation_result and not result.validation_result.passed:
                    click.echo(f"  Validation failed after {result.validation_result.retry_count + 1} attempts", err=True)
                    click.echo(f"  Found banned strings: {', '.join(result.validation_result.found_banned_strings)}", err=True)
                continue
                
            if output:
                # Create output file path
                relative_path = Path(code_file.path).relative_to(input_path)
                output_file = output_path / relative_path
                output_file.parent.mkdir(parents=True, exist_ok=True)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(result.anonymized_content)
                    
                if verbose:
                    click.echo(f"  -> {output_file}")
            else:
                click.echo(f"\n=== {code_file.path} ===")
                click.echo(result.anonymized_content)
                click.echo("=" * 50)


if __name__ == '__main__':
    main()