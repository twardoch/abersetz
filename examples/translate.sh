#!/bin/bash
# this_file: examples/translate.sh

# Basic shell script examples for abersetz CLI

# Example 1: Simple translation
echo "=== Example 1: Simple translation ==="
abersetz tr es poem_en.txt --engine translators/google

# Example 2: Using shorthand command
echo -e "\n=== Example 2: Shorthand command ==="
abtr fr poem_en.txt

# Example 3: Translate directory recursively
echo -e "\n=== Example 3: Directory translation ==="
abersetz tr de ./docs --recurse --output ./docs_de

# Example 4: Translate with specific patterns
echo -e "\n=== Example 4: Pattern matching ==="
abtr ja . --include "*.md,*.txt" --exclude "*test*,.*" --output ./translations/ja

# Example 5: Overwrite original files (be careful!)
echo -e "\n=== Example 5: In-place translation ==="
# abersetz tr es backup_first.txt --overwrite

# Example 6: Dry run to test without translating
echo -e "\n=== Example 6: Dry run mode ==="
abersetz tr zh-CN ./project --dry-run

# Example 7: Using different engines
echo -e "\n=== Example 7: Different engines ==="
# Google Translate
abtr pt file.txt --engine translators/google

# Bing Translate
abtr pt file.txt --engine translators/bing

# DeepL via deep-translator
abtr pt file.txt --engine deep-translator/deepl

# Example 8: Save vocabulary for LLM engines
echo -e "\n=== Example 8: LLM with vocabulary ==="
# Requires SILICONFLOW_API_KEY environment variable
# abersetz tr es technical.md --engine hysf --save-voc

# Example 9: Verbose mode for debugging
echo -e "\n=== Example 9: Verbose output ==="
abersetz tr fr test.txt --verbose --dry-run

# Example 10: Check version
echo -e "\n=== Example 10: Version check ==="
abersetz version