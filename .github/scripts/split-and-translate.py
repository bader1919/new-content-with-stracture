#!/usr/bin/env python3
"""
Script to split large markdown files into smaller chunks for DeepL translation
and then recombine them.
"""

import os
import sys
import re
from pathlib import Path

def split_markdown_file(file_path, max_chars=15000):
    """
    Split a markdown file into smaller chunks at natural breakpoints.
    
    Args:
        file_path (str): Path to the input markdown file
        max_chars (int): Maximum characters per chunk (default 15KB)
    
    Returns:
        list: List of chunk file paths created
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if len(content) <= max_chars:
        print(f"File {file_path} is small enough ({len(content)} chars), no splitting needed")
        return []
    
    chunks = []
    current_chunk = ""
    lines = content.split('\n')
    
    for line in lines:
        # If adding this line would exceed the limit, save current chunk
        if len(current_chunk) + len(line) + 1 > max_chars and current_chunk:
            chunks.append(current_chunk.strip())
            current_chunk = line + '\n'
        else:
            current_chunk += line + '\n'
    
    # Add the last chunk if it has content
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    # Write chunks to separate files
    chunk_files = []
    base_name = Path(file_path).stem
    base_dir = Path(file_path).parent
    
    for i, chunk in enumerate(chunks, 1):
        chunk_file = base_dir / f"{base_name}_chunk_{i}.md"
        with open(chunk_file, 'w', encoding='utf-8') as f:
            f.write(chunk)
        chunk_files.append(str(chunk_file))
        print(f"Created chunk {i}: {chunk_file} ({len(chunk)} chars)")
    
    return chunk_files

def main():
    if len(sys.argv) != 2:
        print("Usage: python split-and-translate.py <markdown_file>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        sys.exit(1)
    
    print(f"Processing file: {file_path}")
    chunk_files = split_markdown_file(file_path)
    
    if chunk_files:
        print(f"File split into {len(chunk_files)} chunks:")
        for chunk_file in chunk_files:
            print(f"  - {chunk_file}")
    else:
        print("No splitting required")

if __name__ == "__main__":
    main()