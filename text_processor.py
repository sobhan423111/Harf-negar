# -*- coding: utf-8 -*-
"""
Harfnegar - Text Processor
Processes Persian/Arabic text using arabic-reshaper and python-bidi

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""

from arabic_reshaper import reshape
from bidi.algorithm import get_display
import re


class TextProcessor:
    """Text processing for Persian/Arabic text"""
    
    @staticmethod
    def encode_text(text):
        """
        Encode text for display (reshape and apply bidi)
        
        Args:
            text: Input Persian/Arabic text
            
        Returns:
            Processed text ready for display
        """
        if not text:
            return ""
        
        try:
            # Reshape Arabic/Persian characters
            reshaped = reshape(text)
            
            # Apply bidirectional algorithm
            display_text = get_display(reshaped)
            
            return display_text
        except Exception as e:
            print(f"Error encoding text: {e}")
            return text
    
    @staticmethod
    def decode_text(text):
        """
        Decode reshaped text back to original form
        Note: This is a best-effort approximation
        
        Args:
            text: Reshaped display text
            
        Returns:
            Decoded text (approximation)
        """
        if not text:
            return ""
        
        try:
            # Reverse the string (undo bidi)
            reversed_text = text[::-1]
            
            # Try to detect and convert reshaped forms back
            # This is approximate - perfect reversal is not always possible
            result = []
            
            for char in reversed_text:
                code = ord(char)
                
                # Map common reshaped forms back to original
                if 0xFE70 <= code <= 0xFEFF:
                    # Arabic Presentation Forms-B
                    # Try to map back (simplified mapping)
                    if 0xFE80 <= code <= 0xFEF4:
                        # Rough mapping to basic forms
                        base = 0x0621 + ((code - 0xFE80) // 4)
                        result.append(chr(base))
                    else:
                        result.append(char)
                else:
                    result.append(char)
            
            return ''.join(result)
            
        except Exception as e:
            print(f"Error decoding text: {e}")
            return text
    
    @staticmethod
    def process_with_regex(text, pattern, positions):
        """
        Process only parts of text at given positions
        
        Args:
            text: Input text
            pattern: Regex pattern (not used, positions are pre-calculated)
            positions: List of (start, end) tuples for matching positions
            
        Returns:
            Text with only matched parts processed
        """
        if not text or not positions:
            return text
        
        try:
            # Sort positions by start
            sorted_positions = sorted(positions, key=lambda x: x[0])
            
            result = []
            last_end = 0
            
            for start, end in sorted_positions:
                # Add unprocessed part
                result.append(text[last_end:start])
                
                # Process matched part
                matched_text = text[start:end]
                processed = TextProcessor.encode_text(matched_text)
                result.append(processed)
                
                last_end = end
            
            # Add remaining text
            result.append(text[last_end:])
            
            return ''.join(result)
            
        except Exception as e:
            print(f"Error in regex processing: {e}")
            return text
    
    @staticmethod
    def find_regex_matches(text, pattern):
        """
        Find all regex matches in text
        
        Args:
            text: Input text
            pattern: Regex pattern
            
        Returns:
            List of (start, end, matched_text) tuples or None if error
        """
        if not text or not pattern:
            return None
        
        try:
            matches = []
            for match in re.finditer(pattern, text, re.UNICODE):
                matches.append((match.start(), match.end(), match.group(0)))
            
            return matches if matches else None
            
        except re.error as e:
            return None
