# -*- coding: utf-8 -*-
"""Harfnegar Language Manager v1.4.2"""
import polib

class LanguageManager:
    LANGS = {
        'en': {
            'app_name': 'Harfnegar', 'file': 'File', 'new': 'New', 'open': 'Open', 'save': 'Save', 'save_as': 'Save As', 'exit': 'Exit',
            'edit': 'Edit', 'undo': 'Undo', 'redo': 'Redo', 'select_all': 'Select All', 'copy': 'Copy', 'paste': 'Paste', 'cut': 'Cut',
            'tools': 'Tools', 'regex': 'Regex', 'font': 'Font', 'always_on_top': 'Always on Top', 'quick_mode': 'Quick Mode',
            'language': 'Language', 'help': 'Help', 'about': 'About',
            'input': 'Input', 'output': 'Output', 'auto_copy': 'Auto Copy', 'process': 'Process', 'ready': 'Ready',
            'chars': 'chars', 'words': 'words', 'lines': 'lines', 'clear': 'Clear',
            'zoom_in': 'Zoom In', 'zoom_out': 'Zoom Out', 'reset': 'Reset Zoom', 'stats': 'Statistics',
            'view': 'View', 'theme': 'Theme', 'light': 'Light', 'dark': 'Dark',
            'pattern': 'Pattern:', 'test': 'Test', 'apply': 'Apply', 'close': 'Close', 'matches': 'matches',
            'recent': 'Recent', 'history': 'History', 'export_pot': 'Export POT', 'import_po': 'Import PO',
            'utilities': 'Utilities', 'reverse': 'Reverse Text', 'remove_spaces': 'Remove Extra Spaces',
            'line_numbers': 'Add Line Numbers', 'frequency': 'Character Frequency', 'find_replace': 'Find & Replace',
            'favorites': 'Favorites', 'add_favorite': 'Add to Favorites', 'manage_favorites': 'Manage Favorites',
            'po_editor': 'PO Editor', 'json_editor': 'JSON Editor', 'yaml_editor': 'YAML Editor', 'xml_editor': 'XML Editor',
            'msgid': 'Source', 'msgstr': 'Translation', 'comment': 'Comment', 'key': 'Key', 'value': 'Value',
            'process_all': 'Process All', 'process_selected': 'Process Selected', 'select_text': 'Select',
            'search': 'Search', 'filter': 'Filter', 'exceptions': 'Exceptions', 'add_exception': 'Add Exception',
            'description': 'Description', 'enabled': 'Enabled', 'disabled': 'Disabled', 'delete': 'Delete',
            'fuzzy': 'Fuzzy', 'untranslated': 'Untranslated', 'translated': 'Translated', 'show_all': 'Show All',
            'row': 'Row', 'expand': 'Expand', 'collapse': 'Collapse', 'expand_all': 'Expand All', 'collapse_all': 'Collapse All',
            'insert': 'Insert', 'remove': 'Remove', 'move_up': 'Move Up', 'move_down': 'Move Down',
            'duplicate': 'Duplicate', 'validate': 'Validate', 'format': 'Format', 'minify': 'Minify',
            'prettify': 'Prettify', 'sort_keys': 'Sort Keys', 'node': 'Node', 'attribute': 'Attribute',
            'text_content': 'Text', 'add_node': 'Add Node', 'add_attribute': 'Add Attribute',
        },
        'fa': {
            'app_name': 'حرف‌نگار', 'file': 'پرونده', 'new': 'جدید', 'open': 'باز کردن', 'save': 'ذخیره', 'save_as': 'ذخیره در', 'exit': 'خروج',
            'edit': 'ویرایش', 'undo': 'واگرد', 'redo': 'از نو', 'select_all': 'انتخاب همه', 'copy': 'کپی', 'paste': 'چسباندن', 'cut': 'برش',
            'tools': 'ابزارها', 'regex': 'Regex', 'font': 'فونت', 'always_on_top': 'همیشه بالا', 'quick_mode': 'حالت سریع',
            'language': 'زبان', 'help': 'راهنما', 'about': 'درباره',
            'input': 'ورودی', 'output': 'خروجی', 'auto_copy': 'کپی خودکار', 'process': 'پردازش', 'ready': 'آماده',
            'chars': 'حرف', 'words': 'کلمه', 'lines': 'خط', 'clear': 'پاک کردن',
            'zoom_in': 'بزرگنمایی', 'zoom_out': 'کوچکنمایی', 'reset': 'بازنشانی', 'stats': 'آمار',
            'view': 'نمایش', 'theme': 'تم', 'light': 'روشن', 'dark': 'تاریک',
            'history': 'تاریخچه', 'recent': 'اخیر', 'utilities': 'ابزارها',
            'reverse': 'معکوس کردن', 'remove_spaces': 'حذف فضای اضافی', 'line_numbers': 'شماره خط',
            'frequency': 'فراوانی حروف', 'find_replace': 'جست‌وجو و جایگزین', 'favorites': 'علاقه‌مندی‌ها',
            'po_editor': 'ویرایشگر PO', 'json_editor': 'ویرایشگر JSON', 'yaml_editor': 'ویرایشگر YAML', 'xml_editor': 'ویرایشگر XML',
            'msgid': 'منبع', 'msgstr': 'ترجمه', 'comment': 'توضیح', 'key': 'کلید', 'value': 'مقدار',
            'process_all': 'پردازش همه', 'process_selected': 'پردازش انتخاب‌شده', 'select_text': 'انتخاب',
            'search': 'جستجو', 'filter': 'فیلتر', 'exceptions': 'استثنائات', 'add_exception': 'افزودن استثنا',
            'description': 'توضیحات', 'enabled': 'فعال', 'disabled': 'غیرفعال', 'delete': 'حذف',
            'fuzzy': 'مبهم', 'untranslated': 'ترجمه نشده', 'translated': 'ترجمه شده', 'show_all': 'نمایش همه',
            'row': 'ردیف', 'expand': 'باز کردن', 'collapse': 'بستن', 'expand_all': 'باز کردن همه', 'collapse_all': 'بستن همه',
            'insert': 'درج', 'remove': 'حذف', 'move_up': 'بالا', 'move_down': 'پایین',
            'duplicate': 'تکثیر', 'validate': 'اعتبارسنجی', 'format': 'قالب‌بندی', 'minify': 'فشرده', 'prettify': 'زیباسازی',
        },
        'ar': {'app_name': 'Harfnegar', 'theme': 'المظهر', 'light': 'فاتح', 'dark': 'داكن'},
    }
    
    # Add other 48 languages with minimal translations
    for lang_code in ['es', 'fr', 'de', 'ru', 'zh', 'ja', 'tr', 'pt', 'it', 'nl', 'pl', 'ko', 'vi', 'th', 'id', 'ms', 'hi', 'bn', 'ur', 'sw', 'ro', 'uk', 'cs', 'sv', 'da', 'no', 'fi', 'el', 'he', 'hu', 'sk', 'bg', 'hr', 'sr', 'ca', 'af', 'az', 'ka', 'lt', 'lv', 'et', 'sl', 'sq', 'mk', 'is', 'mt', 'cy', 'ga']:
        if lang_code not in LANGS:
            LANGS[lang_code] = {'app_name': 'Harfnegar'}
    
    def __init__(self, db):
        self.db = db
        self.lang = db.get('language', 'en')
        self.custom = {}
        for cl in db.get_custom_languages():
            self.custom[cl['code']] = cl['translations']
    
    def get(self, key, default=''):
        if self.lang in self.custom and key in self.custom[self.lang]:
            return self.custom[self.lang][key]
        return self.LANGS.get(self.lang, {}).get(key, self.LANGS['en'].get(key, default))
    
    def set_language(self, lang):
        self.lang = lang
        self.db.set('language', lang)
    
    def get_languages(self):
        return {'builtin': list(self.LANGS.keys()), 'custom': list(self.custom.keys())}
    
    def export_pot(self, filename):
        try:
            po = polib.POFile()
            po.metadata = {'Project-Id-Version': '1.4.2', 'Content-Type': 'text/plain; charset=utf-8'}
            for k, v in self.LANGS['en'].items():
                po.append(polib.POEntry(msgid=k, msgstr='', comment=v))
            po.save(filename)
            return True
        except: return False
    
    def import_po(self, filename, code, name):
        try:
            po = polib.pofile(filename)
            trans = {e.msgid: e.msgstr for e in po if e.msgstr}
            self.db.add_custom_language(code, name, trans)
            self.custom[code] = trans
            return True
        except: return False
