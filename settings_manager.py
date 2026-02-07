# -*- coding: utf-8 -*-
"""
Harfnegar - Settings Manager
Manages application settings using SQLite

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""

import sqlite3
import os


class SettingsManager:
    """Manages application settings in SQLite database"""
    
    def __init__(self):
        # Use in-memory database
        self.conn = sqlite3.connect('harfnegar.dontdeleteme')
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._load_defaults()
    
    def _create_tables(self):
        """Create settings table"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        self.conn.commit()
    
    def _load_defaults(self):
        """Load default settings"""
        defaults = {
            'language': 'fa',
            'auto_copy': 'true',
            'always_on_top': 'false',
            'quick_mode': 'false',
            'font_family': 'Tahoma',
            'font_size': '11',
            'window_width': '900',
            'window_height': '700'
        }
        
        for key, value in defaults.items():
            self.set(key, value, save_if_exists=False)
    
    def get(self, key, default=''):
        """Get setting value"""
        self.cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else default
    
    def set(self, key, value, save_if_exists=True):
        """Set setting value"""
        if save_if_exists:
            self.cursor.execute('''
                INSERT OR REPLACE INTO settings (key, value)
                VALUES (?, ?)
            ''', (key, str(value)))
        else:
            # Only insert if not exists
            self.cursor.execute('''
                INSERT OR IGNORE INTO settings (key, value)
                VALUES (?, ?)
            ''', (key, str(value)))
        
        self.conn.commit()
    
    def get_bool(self, key, default=False):
        """Get boolean setting"""
        value = self.get(key, str(default).lower())
        return value.lower() == 'true'
    
    def get_int(self, key, default=0):
        """Get integer setting"""
        try:
            return int(self.get(key, str(default)))
        except:
            return default
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
