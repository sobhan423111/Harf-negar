# -*- coding: utf-8 -*-
"""
Harfnegar - Language Manager
Manages translations for multiple languages

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""


class LanguageManager:
    """Manages application translations"""
    
    TRANSLATIONS = {
        'fa': {
            # Menu
            'file': 'پرونده',
            'new': 'جدید',
            'open': 'باز کردن...',
            'save_output': 'ذخیره خروجی...',
            'exit': 'خروج',
            
            'edit': 'ویرایش',
            'undo': 'واگرد',
            'select_all': 'انتخاب همه',
            'copy': 'کپی',
            'paste': 'چسباندن',
            
            'tools': 'ابزارها',
            'regex_window': 'پنجره Regex...',
            'font_settings': 'تنظیم فونت...',
            'always_on_top': 'همیشه در بالا',
            'quick_mode': 'حالت سریع',
            'language': 'زبان',
            
            'help': 'راهنما',
            'user_guide': 'راهنمای استفاده',
            'about': 'درباره',
            
            # Main window
            'title': 'حرف‌نگار - Harfnegar',
            'input_label': 'متن ورودی (فارسی/عربی)',
            'output_label': 'متن خروجی (پردازش شده)',
            'auto_copy': 'کپی خودکار',
            'process': 'پردازش',
            'copy_output': 'کپی خروجی',
            'status_ready': 'آماده',
            'chars': 'کاراکتر',
            
            # Regex window
            'regex_title': 'پنجره Regex',
            'regex_pattern': 'الگوی Regex:',
            'regex_test': 'تست',
            'regex_apply': 'اعمال',
            'regex_close': 'بستن',
            'regex_matches': 'تطابق',
            'regex_invalid': 'الگوی Regex نامعتبر است',
            'regex_no_match': 'تطابقی یافت نشد',
            
            # Messages
            'new_confirm': 'آیا می‌خواهید فایل جدید ایجاد کنید؟\nتغییرات ذخیره نشده از بین می‌رود.',
            'file_opened': 'فایل باز شد',
            'file_saved': 'فایل ذخیره شد',
            'copied': 'کپی شد',
            'processed': 'پردازش انجام شد',
            'error': 'خطا',
            'warning': 'هشدار',
            'success': 'موفقیت',
            'info': 'اطلاعات',
            
            # About
            'about_text': '''حرف‌نگار - Harfnegar
نسخه 0.0.1

پردازشگر متن فارسی و عربی

استفاده از:
• arabic-reshaper
• python-bidi
• tkinter

Copyright (c) 2026 Sobhan Mohammadi
GPL-2.0 License''',
            
            # Help
            'help_text': '''راهنمای حرف‌نگار

نحوه استفاده:
1. متن فارسی/عربی را در بخش ورودی وارد کنید
2. متن پردازش شده در بخش خروجی نمایش داده می‌شود
3. می‌توانید از Regex برای پردازش انتخابی استفاده کنید

استفاده از Regex:
1. از منوی ابزارها → پنجره Regex را باز کنید
2. الگوی مورد نظر را وارد کنید
3. روی "تست" کلیک کنید - قسمت‌های تطابق یافته highlight می‌شوند
4. روی "اعمال" کلیک کنید - فقط قسمت‌های highlight شده پردازش می‌شوند'''
        },
        
        'ar': {
            # Menu
            'file': 'ملف',
            'new': 'جديد',
            'open': 'فتح...',
            'save_output': 'حفظ المخرجات...',
            'exit': 'خروج',
            
            'edit': 'تحرير',
            'undo': 'تراجع',
            'select_all': 'تحديد الكل',
            'copy': 'نسخ',
            'paste': 'لصق',
            
            'tools': 'أدوات',
            'regex_window': 'نافذة Regex...',
            'font_settings': 'إعدادات الخط...',
            'always_on_top': 'دائماً في المقدمة',
            'quick_mode': 'الوضع السريع',
            'language': 'اللغة',
            
            'help': 'مساعدة',
            'user_guide': 'دليل المستخدم',
            'about': 'حول',
            
            # Main window
            'title': 'حرف‌نگار - Harfnegar',
            'input_label': 'النص المدخل (فارسي/عربي)',
            'output_label': 'النص المخرج (معالج)',
            'auto_copy': 'نسخ تلقائي',
            'process': 'معالجة',
            'copy_output': 'نسخ المخرجات',
            'status_ready': 'جاهز',
            'chars': 'حرف',
            
            # Regex window
            'regex_title': 'نافذة Regex',
            'regex_pattern': 'نمط Regex:',
            'regex_test': 'اختبار',
            'regex_apply': 'تطبيق',
            'regex_close': 'إغلاق',
            'regex_matches': 'تطابق',
            'regex_invalid': 'نمط Regex غير صالح',
            'regex_no_match': 'لم يتم العثور على تطابق',
            
            # Messages
            'new_confirm': 'هل تريد إنشاء ملف جديد؟\nسيتم فقدان التغييرات غير المحفوظة.',
            'file_opened': 'تم فتح الملف',
            'file_saved': 'تم حفظ الملف',
            'copied': 'تم النسخ',
            'processed': 'تمت المعالجة',
            'error': 'خطأ',
            'warning': 'تحذير',
            'success': 'نجاح',
            'info': 'معلومات',
            
            # About
            'about_text': '''حرف‌نگار - Harfnegar
الإصدار 0.0.1

معالج النصوص الفارسية والعربية

استخدام:
• arabic-reshaper
• python-bidi
• tkinter

Copyright (c) 2026 Sobhan Mohammadi
GPL-2.0 License''',
            
            # Help
            'help_text': '''دليل حرف‌نگار

كيفية الاستخدام:
1. أدخل النص الفارسي/العربي في قسم الإدخال
2. سيتم عرض النص المعالج في قسم الإخراج
3. يمكنك استخدام Regex للمعالجة الانتقائية

استخدام Regex:
1. افتح من قائمة الأدوات → نافذة Regex
2. أدخل النمط المطلوب
3. انقر على "اختبار" - سيتم تمييز الأجزاء المطابقة
4. انقر على "تطبيق" - سيتم معالجة الأجزاء المميزة فقط'''
        },
        
        'en': {
            # Menu
            'file': 'File',
            'new': 'New',
            'open': 'Open...',
            'save_output': 'Save Output...',
            'exit': 'Exit',
            
            'edit': 'Edit',
            'undo': 'Undo',
            'select_all': 'Select All',
            'copy': 'Copy',
            'paste': 'Paste',
            
            'tools': 'Tools',
            'regex_window': 'Regex Window...',
            'font_settings': 'Font Settings...',
            'always_on_top': 'Always on Top',
            'quick_mode': 'Quick Mode',
            'language': 'Language',
            
            'help': 'Help',
            'user_guide': 'User Guide',
            'about': 'About',
            
            # Main window
            'title': 'Harfnegar',
            'input_label': 'Input Text (Persian/Arabic)',
            'output_label': 'Output Text (Processed)',
            'auto_copy': 'Auto Copy',
            'process': 'Process',
            'copy_output': 'Copy Output',
            'status_ready': 'Ready',
            'chars': 'chars',
            
            # Regex window
            'regex_title': 'Regex Window',
            'regex_pattern': 'Regex Pattern:',
            'regex_test': 'Test',
            'regex_apply': 'Apply',
            'regex_close': 'Close',
            'regex_matches': 'matches',
            'regex_invalid': 'Invalid Regex pattern',
            'regex_no_match': 'No matches found',
            
            # Messages
            'new_confirm': 'Do you want to create a new file?\nUnsaved changes will be lost.',
            'file_opened': 'File opened',
            'file_saved': 'File saved',
            'copied': 'Copied',
            'processed': 'Processed',
            'error': 'Error',
            'warning': 'Warning',
            'success': 'Success',
            'info': 'Information',
            
            # About
            'about_text': '''Harfnegar
Version 0.0.1

Persian/Arabic Text Processor

Using:
• arabic-reshaper
• python-bidi
• tkinter

Copyright (c) 2026 Sobhan Mohammadi
GPL-2.0 License''',
            
            # Help
            'help_text': '''Harfnegar User Guide

How to use:
1. Enter Persian/Arabic text in the input section
2. Processed text will be displayed in the output section
3. You can use Regex for selective processing

Using Regex:
1. Open from Tools menu → Regex Window
2. Enter the desired pattern
3. Click "Test" - matching parts will be highlighted
4. Click "Apply" - only highlighted parts will be processed'''
        }
    }
    
    def __init__(self, language='fa'):
        self.current_language = language
    
    def set_language(self, language):
        """Set current language"""
        if language in self.TRANSLATIONS:
            self.current_language = language
            return True
        return False
    
    def get(self, key, default=''):
        """Get translation for key"""
        return self.TRANSLATIONS.get(self.current_language, {}).get(key, default)
    
    def get_current_language(self):
        """Get current language code"""
        return self.current_language
