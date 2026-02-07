# -*- coding: utf-8 -*-
"""
Harfnegar - Main GUI
Main graphical user interface

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font as tkfont
import pyperclip
from text_processor import TextProcessor
from language_manager import LanguageManager
from settings_manager import SettingsManager
from regex_window import RegexWindow
import sys


class HarfnegarGUI:
    """Main application GUI"""
    
    def __init__(self, root):
        self.root = root

        #icon
        if sys.platform.startswith("win"):
            self.root.iconbitmap(self.resource_path("icon.ico"))
        else:
            icon = tk.PhotoImage(file=self.resource_path("icon.png"))
            self.root.iconphoto(True, icon)
        
        # Managers
        self.settings = SettingsManager()
        self.lang = LanguageManager(self.settings.get('language', 'fa'))
        
        # Setup window
        self.root.title(self.lang.get('title'))
        width = self.settings.get_int('window_width', 900)
        height = self.settings.get_int('window_height', 700)
        self.root.geometry(f"{width}x{height}")
        
        # Variables
        self.auto_copy = tk.BooleanVar(value=self.settings.get_bool('auto_copy'))
        self.always_on_top = tk.BooleanVar(value=self.settings.get_bool('always_on_top'))
        self.quick_mode = tk.BooleanVar(value=self.settings.get_bool('quick_mode'))
        
        # Font
        font_family = self.settings.get('font_family', 'Tahoma')
        font_size = self.settings.get_int('font_size', 11)
        self.text_font = tkfont.Font(family=font_family, size=font_size)
        
        # Create UI
        self._create_menu()
        self._create_main_area()
        self._create_control_panel()
        self._create_status_bar()

        
        # Apply settings
        self.root.attributes('-topmost', self.always_on_top.get())
        
        # Clipboard monitoring
        self.last_clipboard = ""
        self.monitor_clipboard()
        
        # Focus
        self.txt_input.focus_set()
        
        # Update status
        self.update_char_count()
    
    def resource_path(self, relative_path):
        import os, sys
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _create_menu(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('file'), menu=file_menu)
        file_menu.add_command(label=self.lang.get('new'), command=self.new_file)
        file_menu.add_command(label=self.lang.get('open'), command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang.get('save_output'), command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label=self.lang.get('exit'), command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('edit'), menu=edit_menu)
        edit_menu.add_command(label=self.lang.get('undo'), command=self.undo)
        edit_menu.add_separator()
        edit_menu.add_command(label=self.lang.get('select_all'), command=self.select_all)
        edit_menu.add_command(label=self.lang.get('copy'), command=self.copy_text)
        edit_menu.add_command(label=self.lang.get('paste'), command=self.paste_text)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('tools'), menu=tools_menu)
        tools_menu.add_command(label=self.lang.get('regex_window'), command=self.open_regex_window)
        tools_menu.add_separator()
        tools_menu.add_command(label=self.lang.get('font_settings'), command=self.font_settings)
        tools_menu.add_separator()
        tools_menu.add_checkbutton(label=self.lang.get('always_on_top'), 
                                   variable=self.always_on_top,
                                   command=self.toggle_always_on_top)
        tools_menu.add_checkbutton(label=self.lang.get('quick_mode'),
                                   variable=self.quick_mode,
                                   command=self.toggle_quick_mode)
        
        # Language submenu
        lang_menu = tk.Menu(tools_menu, tearoff=0)
        tools_menu.add_separator()
        tools_menu.add_cascade(label=self.lang.get('language'), menu=lang_menu)
        
        self.lang_var = tk.StringVar(value=self.lang.get_current_language())
        lang_menu.add_radiobutton(label="فارسی", variable=self.lang_var, 
                                 value='fa', command=lambda: self.change_language('fa'))
        lang_menu.add_radiobutton(label="العربية", variable=self.lang_var,
                                 value='ar', command=lambda: self.change_language('ar'))
        lang_menu.add_radiobutton(label="English", variable=self.lang_var,
                                 value='en', command=lambda: self.change_language('en'))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang.get('help'), menu=help_menu)
        help_menu.add_command(label=self.lang.get('user_guide'), command=self.show_help)
        help_menu.add_separator()
        help_menu.add_command(label=self.lang.get('about'), command=self.show_about)
    
    def _create_main_area(self):
        """Create main text areas"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Paned window
        paned = ttk.PanedWindow(main_frame, orient=tk.VERTICAL)
        paned.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.LabelFrame(paned, text=self.lang.get('input_label'), padding="5")
        
        txt_in_frame = ttk.Frame(input_frame)
        txt_in_frame.pack(fill=tk.BOTH, expand=True)
        
        self.txt_input = tk.Text(txt_in_frame, wrap=tk.WORD, undo=True,
                                font=self.text_font, relief=tk.SOLID, 
                                borderwidth=1, bg='#FCFDFF')
        self.txt_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll_in = ttk.Scrollbar(txt_in_frame, command=self.txt_input.yview)
        scroll_in.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_input.config(yscrollcommand=scroll_in.set)
        
        # Bind events
        self.txt_input.bind('<KeyRelease>', self.on_input_change)
        self.txt_input.bind('<ButtonRelease-1>', self.on_input_change)
        
        paned.add(input_frame, weight=1)
        
        # Output frame
        output_frame = ttk.LabelFrame(paned, text=self.lang.get('output_label'), padding="5")
        
        txt_out_frame = ttk.Frame(output_frame)
        txt_out_frame.pack(fill=tk.BOTH, expand=True)
        
        self.txt_output = tk.Text(txt_out_frame, wrap=tk.WORD, undo=True,
                                 font=self.text_font, relief=tk.SOLID,
                                 borderwidth=1, bg='#F0FFF0')
        self.txt_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scroll_out = ttk.Scrollbar(txt_out_frame, command=self.txt_output.yview)
        scroll_out.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_output.config(yscrollcommand=scroll_out.set)
        
        # Bind events for output (to decode)
        self.txt_output.bind('<KeyRelease>', self.on_output_change)
        
        paned.add(output_frame, weight=1)
    
    def _create_control_panel(self):
        """Create control panel"""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Left side
        left_frame = ttk.Frame(control_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Checkbutton(left_frame, text=self.lang.get('auto_copy'),
                       variable=self.auto_copy,
                       command=self.toggle_auto_copy).pack(side=tk.LEFT, padx=5)
        
        # Right side
        right_frame = ttk.Frame(control_frame)
        right_frame.pack(side=tk.RIGHT)
        
        ttk.Button(right_frame, text=self.lang.get('copy_output'),
                  command=self.copy_output).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(right_frame, text=self.lang.get('process'),
                  command=self.force_process).pack(side=tk.RIGHT, padx=5)
    
    def _create_status_bar(self):
        """Create status bar"""
        status_frame = ttk.Frame(self.root, relief=tk.SUNKEN)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(status_frame, text=self.lang.get('status_ready'))
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        self.char_label = ttk.Label(status_frame, text="0 " + self.lang.get('chars'))
        self.char_label.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def update_status(self, message, duration=3000):
        """Update status message"""
        self.status_label.config(text=message)
        if duration > 0:
            self.root.after(duration, lambda: self.status_label.config(
                text=self.lang.get('status_ready')))
    
    def update_char_count(self):
        """Update character count"""
        text = self.txt_input.get("1.0", "end-1c")
        count = len(text)
        self.char_label.config(text=f"{count} {self.lang.get('chars')}")
    
    def on_input_change(self, event=None):
        """Handle input changes"""
        if hasattr(self, '_update_job'):
            self.root.after_cancel(self._update_job)
        
        self._update_job = self.root.after(300, self.update_output)
        self.update_char_count()
    
    def on_output_change(self, event=None):
        """Handle output changes - decode text"""
        if hasattr(self, '_decode_job'):
            self.root.after_cancel(self._decode_job)
        
        self._decode_job = self.root.after(500, self.decode_output)
    
    def update_output(self):
        """Update output from input"""
        try:
            text = self.txt_input.get("1.0", "end-1c")
            
            if not text.strip():
                self.txt_output.delete("1.0", tk.END)
                return
            
            # Process text
            result = TextProcessor.encode_text(text)
            
            # Update output
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert("1.0", result)
            
            # Auto copy
            if self.auto_copy.get():
                self.copy_to_clipboard(result)
            
            self.update_status(self.lang.get('processed'))
            
        except Exception as e:
            print(f"Error: {e}")
    
    def decode_output(self):
        """Decode output to input"""
        try:
            text = self.txt_output.get("1.0", "end-1c")
            
            if not text.strip():
                return
            
            # Decode text
            result = TextProcessor.decode_text(text)
            
            # Update input (unbind first)
            self.txt_input.bind('<KeyRelease>', lambda e: None)
            self.txt_input.delete("1.0", tk.END)
            self.txt_input.insert("1.0", result)
            self.txt_input.bind('<KeyRelease>', self.on_input_change)
            
            self.update_char_count()
            
        except Exception as e:
            print(f"Error decoding: {e}")
    
    def force_process(self):
        """Force immediate processing"""
        self.update_output()
    
    def new_file(self):
        """Create new file"""
        if self.txt_input.get("1.0", "end-1c").strip():
            if not messagebox.askyesno(self.lang.get('warning'),
                                      self.lang.get('new_confirm')):
                return
        
        self.txt_input.delete("1.0", tk.END)
        self.txt_output.delete("1.0", tk.END)
        self.update_status(self.lang.get('status_ready'))
    
    def open_file(self):
        """Open file"""
        filename = filedialog.askopenfilename(
            title=self.lang.get('open'),
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.txt_input.delete("1.0", tk.END)
                self.txt_input.insert("1.0", content)
                self.update_output()
                self.update_status(self.lang.get('file_opened'))
                
            except Exception as e:
                messagebox.showerror(self.lang.get('error'), str(e))
    
    def save_file(self):
        """Save output file"""
        filename = filedialog.asksaveasfilename(
            title=self.lang.get('save_output'),
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                content = self.txt_output.get("1.0", "end-1c")
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.update_status(self.lang.get('file_saved'))
                messagebox.showinfo(self.lang.get('success'),
                                   self.lang.get('file_saved'))
                
            except Exception as e:
                messagebox.showerror(self.lang.get('error'), str(e))
    
    def undo(self):
        """Undo"""
        focused = self.root.focus_get()
        try:
            if focused == self.txt_output:
                self.txt_output.edit_undo()
            else:
                self.txt_input.edit_undo()
        except:
            pass
    
    def select_all(self):
        """Select all"""
        focused = self.root.focus_get()
        if focused == self.txt_output:
            self.txt_output.tag_add('sel', '1.0', 'end')
        else:
            self.txt_input.tag_add('sel', '1.0', 'end')
    
    def copy_text(self):
        """Copy selected text"""
        focused = self.root.focus_get()
        try:
            if focused in [self.txt_input, self.txt_output]:
                text = focused.selection_get()
                self.copy_to_clipboard(text)
                self.update_status(self.lang.get('copied'), 1500)
        except:
            pass
    
    def paste_text(self):
        """Paste text"""
        focused = self.root.focus_get()
        try:
            if focused in [self.txt_input, self.txt_output]:
                text = pyperclip.paste()
                focused.insert(tk.INSERT, text)
        except:
            pass
    
    def copy_output(self):
        """Copy output"""
        text = self.txt_output.get("1.0", "end-1c")
        if text.strip():
            self.copy_to_clipboard(text)
            self.update_status(self.lang.get('copied'), 1500)
    
    def copy_to_clipboard(self, text):
        """Copy to clipboard"""
        try:
            pyperclip.copy(text)
        except Exception as e:
            print(f"Clipboard error: {e}")
    
    def open_regex_window(self):
        """Open regex window"""
        def callback(result):
            self.txt_output.delete("1.0", tk.END)
            self.txt_output.insert("1.0", result)
        
        RegexWindow(self.root, self.lang, self.txt_input, 
                   self.txt_output, callback)
    
    def font_settings(self):
        """Font settings dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title(self.lang.get('font_settings'))
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        x = self.root.winfo_x() + (self.root.winfo_width() - 400) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - 200) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Font family
        ttk.Label(dialog, text="Font:").pack(pady=10)
        families = ['Tahoma', 'Arial', 'Courier New', 'B Nazanin', 'Nazanin']
        font_var = tk.StringVar(value=self.text_font.actual('family'))
        font_combo = ttk.Combobox(dialog, textvariable=font_var, values=families)
        font_combo.pack(pady=5)
        
        # Font size
        ttk.Label(dialog, text="Size:").pack(pady=10)
        size_var = tk.IntVar(value=self.text_font.actual('size'))
        size_spin = ttk.Spinbox(dialog, from_=8, to=32, textvariable=size_var)
        size_spin.pack(pady=5)
        
        def apply():
            self.text_font.config(family=font_var.get(), size=size_var.get())
            self.txt_input.config(font=self.text_font)
            self.txt_output.config(font=self.text_font)
            self.settings.set('font_family', font_var.get())
            self.settings.set('font_size', size_var.get())
            dialog.destroy()
        
        ttk.Button(dialog, text="Apply", command=apply).pack(pady=10)
    
    def toggle_always_on_top(self):
        """Toggle always on top"""
        self.root.attributes('-topmost', self.always_on_top.get())
        self.settings.set('always_on_top', self.always_on_top.get())
    
    def toggle_quick_mode(self):
        """Toggle quick mode"""
        self.settings.set('quick_mode', self.quick_mode.get())
    
    def toggle_auto_copy(self):
        """Toggle auto copy"""
        self.settings.set('auto_copy', self.auto_copy.get())
    
    def change_language(self, lang_code):
        """Change interface language"""
        self.lang.set_language(lang_code)
        self.settings.set('language', lang_code)
        
        messagebox.showinfo(
            self.lang.get('info'),
            "Please restart the application for language changes to take effect."
        )
    
    def monitor_clipboard(self):
        """Monitor clipboard in quick mode"""
        try:
            if self.quick_mode.get():
                text = pyperclip.paste()
                if text and text != self.last_clipboard:
                    self.last_clipboard = text
                    if any('\u0600' <= c <= '\u06FF' for c in text):
                        result = TextProcessor.encode_text(text)
                        self.copy_to_clipboard(result)
        except:
            pass
        
        self.root.after(1000, self.monitor_clipboard)
    
    def show_help(self):
        """Show help"""
        messagebox.showinfo(self.lang.get('help'), 
                           self.lang.get('help_text'))
    
    def show_about(self):
        """Show about"""
        messagebox.showinfo(self.lang.get('about'),
                           self.lang.get('about_text'))
    
    def run(self):
        """Run application"""
        self.root.mainloop()
        self.settings.close()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = HarfnegarGUI(root)
    app.run()


if __name__ == "__main__":
    main()
