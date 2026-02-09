# -*- coding: utf-8 -*-
"""Harfnegar Database v1.4.2"""
import sqlite3, json

class DatabaseManager:
    DB_FILE = "harfnegar.dontdeleteme"
    
    def __init__(self):
        self.conn = sqlite3.connect(self.DB_FILE)
        self.cursor = self.conn.cursor()
        self._create_tables()
        self._load_defaults()
    
    def _create_tables(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS custom_languages (code TEXT PRIMARY KEY, name TEXT, translations TEXT)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, input TEXT, output TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)')
        self.cursor.execute('CREATE TABLE IF NOT EXISTS exceptions (id INTEGER PRIMARY KEY AUTOINCREMENT, pattern TEXT UNIQUE, description TEXT, enabled INTEGER DEFAULT 1)')
        self.conn.commit()
    
    def _load_defaults(self):
        defaults = {
            'language': 'en', 'auto_copy': 'true', 'always_on_top': 'false',
            'quick_mode': 'true', 'font_family': 'Segoe UI', 'font_size': '11',
            'window_width': '1200', 'window_height': '800', 'theme': 'light',
            'auto_save': 'true'
        }
        for k, v in defaults.items():
            self.cursor.execute('INSERT OR IGNORE INTO settings (key, value) VALUES (?, ?)', (k, v))
        self.conn.commit()
    
    def get(self, key, default=''):
        self.cursor.execute('SELECT value FROM settings WHERE key = ?', (key,))
        r = self.cursor.fetchone()
        return r[0] if r else default
    
    def set(self, key, value):
        self.cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', (key, str(value)))
        self.conn.commit()
    
    def get_bool(self, key, default=False):
        return self.get(key, str(default).lower()).lower() == 'true'
    
    def get_int(self, key, default=0):
        try: return int(self.get(key, str(default)))
        except: return default
    
    def add_custom_language(self, code, name, translations):
        try:
            self.cursor.execute('INSERT OR REPLACE INTO custom_languages (code, name, translations) VALUES (?, ?, ?)',
                              (code, name, json.dumps(translations, ensure_ascii=False)))
            self.conn.commit()
            return True
        except: return False
    
    def get_custom_languages(self):
        self.cursor.execute('SELECT code, name, translations FROM custom_languages')
        results = []
        for row in self.cursor.fetchall():
            try:
                results.append({'code': row[0], 'name': row[1], 'translations': json.loads(row[2])})
            except: continue
        return results
    
    def add_history(self, input_text, output_text):
        try:
            self.cursor.execute('INSERT INTO history (input, output) VALUES (?, ?)', (input_text, output_text))
            self.conn.commit()
            self.cursor.execute('DELETE FROM history WHERE id NOT IN (SELECT id FROM history ORDER BY id DESC LIMIT 100)')
            self.conn.commit()
        except: pass
    
    def get_history(self, limit=10):
        try:
            self.cursor.execute('SELECT input, output, timestamp FROM history ORDER BY id DESC LIMIT ?', (limit,))
            return self.cursor.fetchall()
        except:
            return []
    
    def add_favorite(self, text):
        try:
            self.cursor.execute('INSERT INTO favorites (text) VALUES (?)', (text,))
            self.conn.commit()
            return True
        except:
            return False
    
    def get_favorites(self):
        try:
            self.cursor.execute('SELECT id, text, timestamp FROM favorites ORDER BY id DESC')
            return self.cursor.fetchall()
        except:
            return []
    
    def delete_favorite(self, fav_id):
        try:
            self.cursor.execute('DELETE FROM favorites WHERE id = ?', (fav_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    def add_exception(self, pattern, description=''):
        try:
            self.cursor.execute('INSERT INTO exceptions (pattern, description) VALUES (?, ?)', (pattern, description))
            self.conn.commit()
            return True
        except:
            return False
    
    def get_exceptions(self, enabled_only=True):
        try:
            if enabled_only:
                self.cursor.execute('SELECT id, pattern, description, enabled FROM exceptions WHERE enabled = 1')
            else:
                self.cursor.execute('SELECT id, pattern, description, enabled FROM exceptions')
            return self.cursor.fetchall()
        except:
            return []
    
    def get_exception_patterns(self):
        try:
            self.cursor.execute('SELECT pattern FROM exceptions WHERE enabled = 1')
            return [row[0] for row in self.cursor.fetchall()]
        except:
            return []
    
    def update_exception(self, exc_id, pattern, description, enabled):
        try:
            self.cursor.execute('UPDATE exceptions SET pattern = ?, description = ?, enabled = ? WHERE id = ?',
                              (pattern, description, enabled, exc_id))
            self.conn.commit()
            return True
        except:
            return False
    
    def delete_exception(self, exc_id):
        try:
            self.cursor.execute('DELETE FROM exceptions WHERE id = ?', (exc_id,))
            self.conn.commit()
            return True
        except:
            return False
    
    def close(self):
        if self.conn: self.conn.close()
