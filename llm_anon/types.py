"""Type definitions for the LLM anonymizer."""

from typing import Dict, List, Optional, Union, Set
from dataclasses import dataclass
from enum import Enum


class FileType(Enum):
    """Supported file types for anonymization."""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CPP = "cpp"
    RUST = "rust"
    GO = "go"
    OTHER = "other"


@dataclass
class ValidationConfig:
    """Configuration for validation of anonymized content."""
    banned_strings: Set[str]
    case_sensitive: bool = True
    max_retries: int = 3


@dataclass
class AnonymizationConfig:
    """Configuration for code anonymization."""
    preserve_structure: bool = True
    preserve_comments: bool = False
    preserve_strings: bool = False
    model_name: str = "llama3.2"
    temperature: float = 0.1
    validation: Optional[ValidationConfig] = None


@dataclass
class CodeFile:
    """Represents a code file to be anonymized."""
    path: str
    content: str
    file_type: FileType
    language: str


@dataclass
class ValidationResult:
    """Result of content validation."""
    passed: bool
    found_banned_strings: List[str]
    retry_count: int = 0


@dataclass
class AnonymizationResult:
    """Result of code anonymization."""
    original_file: CodeFile
    anonymized_content: str
    success: bool
    validation_result: Optional[ValidationResult] = None
    error_message: Optional[str] = None