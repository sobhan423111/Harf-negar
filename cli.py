#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harfnegar CLI v1.4.2"""
import sys, argparse
from text_processor import TextProcessor
from database_manager import DatabaseManager

def main():
    parser = argparse.ArgumentParser(description='Harfnegar - Text Processor')
    parser.add_argument('input', nargs='?', help='Input text or file')
    parser.add_argument('-f', '--file', action='store_true', help='Read from file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--no-exceptions', action='store_true', help='Disable exceptions')
    parser.add_argument('--add-exception', help='Add exception pattern')
    parser.add_argument('--list-exceptions', action='store_true', help='List exceptions')
    parser.add_argument('--version', action='version', version='1.4.2')
    
    args = parser.parse_args()
    db = DatabaseManager()
    
    if args.list_exceptions:
        exceptions = db.get_exceptions(enabled_only=False)
        if exceptions:
            for exc_id, pattern, desc, enabled in exceptions:
                status = "✓" if enabled else "✗"
                print(f"{status} [{exc_id}] {pattern}")
                if desc:
                    print(f"   {desc}")
        else:
            print("No exceptions")
        return
    
    if args.add_exception:
        if db.add_exception(args.add_exception):
            print(f"Added: {args.add_exception}")
        return
    
    if not args.input:
        if not sys.stdin.isatty():
            text = sys.stdin.read()
        else:
            parser.print_help()
            return
    elif args.file:
        text = TextProcessor.read_file(args.input)
    else:
        text = args.input
    
    exceptions = [] if args.no_exceptions else db.get_exception_patterns()
    result = TextProcessor.encode_text(text, exceptions)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Saved to {args.output}")
    else:
        print(result)
    
    db.close()

if __name__ == '__main__':
    main()
