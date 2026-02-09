# -*- coding: utf-8 -*-
"""Harfnegar Text Processor v1.4.2 - Simple bidi + reshaper
Copyright (c) 2026 Sobhan Mohammadi - GPL-2.0"""
from arabic_reshaper import reshape
from bidi.algorithm import get_display
import re, os

class TextProcessor:
    @staticmethod
    def is_persian_arabic(char):
        code = ord(char)
        return (0x0600 <= code <= 0x06FF) or (0xFB50 <= code <= 0xFDFF) or (0xFE70 <= code <= 0xFEFF)
    
    @staticmethod
    def encode_text(text, exceptions=None):
        """Process: reshape + bidi"""
        if not text:
            return ""
        if exceptions and TextProcessor.matches_exception(text, exceptions):
            return text
        try:
            return get_display(reshape(text))
        except:
            return text
    
    @staticmethod
    def matches_exception(text, exceptions):
        if not exceptions:
            return False
        for pattern in exceptions:
            try:
                if re.search(pattern, text, re.UNICODE | re.MULTILINE):
                    return True
            except:
                continue
        return False
    
    @staticmethod
    def decode_text(text):
        return text[::-1] if text else ""
    
    @staticmethod
    def find_regex_matches(text, patterns):
        if not text or not patterns:
            return None
        all_matches = []
        for pattern in patterns:
            if not pattern.strip():
                continue
            try:
                for m in re.finditer(pattern, text, re.UNICODE | re.MULTILINE):
                    all_matches.append((m.start(), m.end(), m.group(0), pattern))
            except:
                continue
        all_matches.sort(key=lambda x: x[0])
        return all_matches if all_matches else None
    
    @staticmethod
    def extract_and_process_matches(text, matches, exceptions=None):
        if not matches:
            return ""
        try:
            lines = [m[2] for m in matches]
            combined = '\n'.join(lines)
            return TextProcessor.encode_text(combined, exceptions)
        except:
            return ""
    
    @staticmethod
    def reverse_text(text):
        return text[::-1] if text else ""
    
    @staticmethod
    def remove_extra_spaces(text):
        return re.sub(r'\s+', ' ', text).strip() if text else ""
    
    @staticmethod
    def add_line_numbers(text):
        if not text:
            return ""
        lines = text.split('\n')
        return '\n'.join([f"{i+1}. {line}" for i, line in enumerate(lines)])
    
    @staticmethod
    def char_frequency(text):
        if not text:
            return {}
        freq = {}
        for char in text:
            if char.strip():
                freq[char] = freq.get(char, 0) + 1
        return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))
    
    @staticmethod
    def find_replace(text, find, replace):
        if not text or not find:
            return text
        return text.replace(find, replace)
    
    @staticmethod
    def read_file(filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            if ext in ['.txt', '.text', '.md', '.csv', '.po', '.json', '.yaml', '.yml', '.xml']:
                with open(filepath, 'r', encoding='utf-8') as f:
                    return f.read()
            elif ext in ['.docx', '.doc']:
                from docx import Document
                doc = Document(filepath)
                return '\n'.join([p.text for p in doc.paragraphs])
            elif ext == '.pdf':
                from PyPDF2 import PdfReader
                reader = PdfReader(filepath)
                return '\n'.join([p.extract_text() for p in reader.pages])
            else:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")
