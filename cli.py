#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harfnegar - CLI
Command Line Interface

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""

import argparse
import sys
from text_processor import TextProcessor


def process_file(input_file, output_file=None):
    """Process a file"""
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        result = TextProcessor.encode_text(content)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✓ Output written to: {output_file}")
        else:
            print(result)
        
        return 0
    except FileNotFoundError:
        print(f"✗ Error: File '{input_file}' not found", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def process_text(text):
    """Process text directly"""
    try:
        result = TextProcessor.encode_text(text)
        print(result)
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def process_stdin():
    """Process from stdin"""
    try:
        content = sys.stdin.read()
        result = TextProcessor.encode_text(content)
        print(result)
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description='Harfnegar - Persian/Arabic Text Processor',
        epilog='Copyright (c) 2026 Sobhan Mohammadi - GPL-2.0'
    )
    
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('-f', '--file', help='Input file')
    input_group.add_argument('-t', '--text', help='Input text')
    input_group.add_argument('-s', '--stdin', action='store_true',
                           help='Read from stdin')
    
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('-v', '--version', action='version',
                       version='Harfnegar 0.0.1')
    
    args = parser.parse_args()
    
    if args.file:
        return process_file(args.file, args.output)
    elif args.text:
        return process_text(args.text)
    elif args.stdin:
        return process_stdin()
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
