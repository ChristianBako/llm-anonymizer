# Examples

This directory contains example files to test the LLM anonymizer.

## Files

### `lamasoft_example.py`
A comprehensive Python example for a fictional company "LamaSoft" containing:
- Company-specific class names and identifiers
- API keys and credentials
- Contact information (emails, phone numbers)
- Internal URLs and domains
- Various sensitive strings to test anonymization

### `test_example.py`
A simpler Python example with common patterns:
- Database connection strings
- Class and method names
- SQL queries and parameters

### `banned_strings.txt`
Example validation configuration file containing banned strings for the LamaSoft example:
- Company names and branding
- Contact information
- API keys and credentials
- URLs and domains
- Product-specific terms

## Usage

Try anonymizing the examples:

```bash
# Test basic anonymization
llm-anon examples/test_example.py

# Test with validation to ensure sensitive strings are removed
llm-anon examples/lamasoft_example.py --validation-config examples/banned_strings.txt -v

# Save anonymized output
llm-anon examples/lamasoft_example.py -o anonymized_output.py

# Process with verbose output to see the validation process
llm-anon examples/lamasoft_example.py --validation-config examples/banned_strings.txt -v -o clean_output.py
```

The LamaSoft example is particularly useful for testing the validation system's ability to catch and remove company-specific information through multiple retry attempts.