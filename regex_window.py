# -*- coding: utf-8 -*-
"""
Harfnegar - Regex Window
Separate window for regex pattern input and testing

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from text_processor import TextProcessor
import gui
import sys


class RegexWindow(tk.Toplevel):
    """Regex pattern window with live preview"""
    
    def __init__(self, parent, lang_manager, input_widget, output_widget, callback):
        super().__init__(parent)

        # icon
        if sys.platform.startswith("win"):
            self.iconbitmap(self.resource_path("icon.ico"))
        else:
            icon = tk.PhotoImage(file=self.resource_path("icon.png"))
            self.iconphoto(True, icon)
            self._icon = icon
        
        self.lang = lang_manager
        self.input_widget = input_widget
        self.output_widget = output_widget
        self.callback = callback
        self.current_matches = []
        
        # Window setup
        self.title(self.lang.get('regex_title'))
        self.geometry("600x400")
        self.transient(parent)
        
        self._create_ui()
        
        # Center window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
     
    def resource_path(self, relative_path):
        import os, sys
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def _create_ui(self):
        """Create UI elements"""
        # Main frame
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Pattern input
        pattern_frame = ttk.Frame(main_frame)
        pattern_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(pattern_frame, text=self.lang.get('regex_pattern')).pack(side=tk.LEFT, padx=(0, 5))
        
        self.pattern_entry = ttk.Entry(pattern_frame)
        self.pattern_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.pattern_entry.focus_set()
        
        ttk.Button(pattern_frame, text=self.lang.get('regex_test'), 
                  command=self.test_pattern).pack(side=tk.LEFT)
        
        # Results area
        result_frame = ttk.LabelFrame(main_frame, text=self.lang.get('info'), padding="5")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrolled text for results
        text_frame = ttk.Frame(result_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(text_frame, height=10, wrap=tk.WORD, 
                                   relief=tk.SOLID, borderwidth=1)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)
        self.result_text.config(state='disabled')
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text=self.lang.get('regex_close'), 
                  command=self.close_window).pack(side=tk.RIGHT, padx=(5, 0))
        
        ttk.Button(button_frame, text=self.lang.get('regex_apply'), 
                  command=self.apply_pattern).pack(side=tk.RIGHT)
    
    def test_pattern(self):
        """Test regex pattern and highlight matches"""
        pattern = self.pattern_entry.get().strip()
        
        if not pattern:
            messagebox.showwarning(
                self.lang.get('warning'),
                self.lang.get('regex_invalid')
            )
            return
        
        # Get input text
        text = self.input_widget.get("1.0", "end-1c")
        
        if not text:
            messagebox.showwarning(
                self.lang.get('warning'),
                "Input text is empty"
            )
            return
        
        # Find matches
        matches = TextProcessor.find_regex_matches(text, pattern)
        
        if matches is None:
            messagebox.showerror(
                self.lang.get('error'),
                self.lang.get('regex_invalid')
            )
            return
        
        if not matches:
            messagebox.showinfo(
                self.lang.get('info'),
                self.lang.get('regex_no_match')
            )
            self.clear_highlights()
            return
        
        # Store matches
        self.current_matches = [(m[0], m[1]) for m in matches]
        
        # Highlight in input
        self.highlight_matches(matches)
        
        # Show results
        self.show_results(matches)
    
    def highlight_matches(self, matches):
        """Highlight matched text in input widget"""
        # Remove previous highlights
        self.clear_highlights()
        
        # Configure highlight tag
        self.input_widget.tag_configure('regex_match', 
                                       background='yellow',
                                       foreground='black')
        
        # Add highlights
        for start, end, text in matches:
            # Convert position to line.column format
            start_pos = f"1.0 + {start} chars"
            end_pos = f"1.0 + {end} chars"
            
            self.input_widget.tag_add('regex_match', start_pos, end_pos)
    
    def clear_highlights(self):
        """Clear all highlights from input widget"""
        try:
            self.input_widget.tag_remove('regex_match', '1.0', 'end')
        except:
            pass
    
    def show_results(self, matches):
        """Show match results in result text"""
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', 'end')
        
        result = f"✓ {len(matches)} {self.lang.get('regex_matches')}:\n\n"
        
        for i, (start, end, text) in enumerate(matches[:20], 1):
            result += f"{i}. '{text}' ({start}-{end})\n"
        
        if len(matches) > 20:
            result += f"\n... and {len(matches) - 20} more"
        
        self.result_text.insert('1.0', result)
        self.result_text.config(state='disabled')
    
    def apply_pattern(self):
        """Apply pattern: put matched parts line by line in input and update output"""
        if not self.current_matches:
            messagebox.showwarning(
                self.lang.get('warning'),
                "Please test the pattern first"
            )
            return

        text = self.input_widget.get("1.0", "end-1c")
        pattern = self.pattern_entry.get().strip()

        matched_texts = [text[start:end] for start, end in self.current_matches]

        if not matched_texts:
            messagebox.showinfo(
                self.lang.get('info'),
                "No matches to apply"
            )
            return

        new_input = "\n".join(matched_texts)
        self.input_widget.delete("1.0", "end")
        self.input_widget.insert("1.0", new_input)
        try:
            result = TextProcessor.encode_text(new_input)
            self.output_widget.delete("1.0", "end")
            self.output_widget.insert("1.0", result)
        except Exception as e:
            print(f"Error processing output: {e}")

        if hasattr(self, 'callback') and self.callback:
            result = TextProcessor.process_with_regex(text, pattern, self.current_matches)
            self.callback(result)

        messagebox.showinfo(
            self.lang.get('success'),
            self.lang.get('processed')
        )
    
    def close_window(self):
        """Close window and clear highlights"""
        self.clear_highlights()
        self.destroy()
