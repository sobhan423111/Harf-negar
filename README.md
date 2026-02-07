# حرف‌نگار - Harfnegar

**پردازشگر متن فارسی و عربی**  
Persian/Arabic Text Processor

---

## ویژگی‌ها / Features

✅ **پردازش با استانداردهای روز** - Using arabic-reshaper & python-bidi  
✅ **رابط گرافیکی** - Beautiful GUI with RTL support  
✅ **رابط خط فرمان** - CLI for scripting  
✅ **پنجره Regex** - Separate regex window with highlighting  
✅ **چندزبانه** - Multilingual (Persian, Arabic, English)  
✅ **کپی/پیست** - Full copy/paste support  
✅ **Decode** - Convert reshaped text back to original  

---

## نصب / Installation

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt
```

---

## استفاده / Usage

### رابط گرافیکی / GUI

```bash
python main.py
```

یا / or:

```bash
python gui.py
```

### خط فرمان / CLI

```bash
# متن مستقیم
python cli.py -t "سلام دنیا"

# فایل
python cli.py -f input.txt -o output.txt

# از stdin
echo "تست" | python cli.py -s
```

---

## راهنمای رابط گرافیکی

### استفاده از Regex
1. از منو: **ابزارها → پنجره Regex**
2. الگوی مورد نظر را وارد کنید
3. روی **تست** کلیک کنید (قسمت‌های تطابق یافته highlight می‌شوند)
4. روی **اعمال** کلیک کنید (فقط قسمت‌های highlight شده پردازش می‌شوند)

### تغییر زبان
- از منو: **ابزارها → زبان**
- زبان‌های موجود: فارسی، عربی، English
- بعد از تغییر زبان باید برنامه را restart کنید

### Decode
- اگر متن پردازش شده (reshaped) را در خروجی وارد کنید
- برنامه به صورت خودکار متن اصلی را در ورودی نمایش می‌دهد

---

## لایسنس / License

```
Harfnegar - Persian/Arabic Text Processor
Copyright (c) 2026 Sobhan Mohammadi

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation.
```

**GPL-2.0 License**

---

## تشکر / Credits

- [arabic-reshaper](https://github.com/mpcabd/python-arabic-reshaper)
- [python-bidi](https://github.com/MeirKriheli/python-bidi)
- [icon-8](https://icons8.com/)

---

**ساخته شده با ❤️ در ایران**  
**Made with ❤️ in Iran**

---

## پشتیبانی / Support

برای گزارش باگ یا پیشنهاد:  
For bug reports or suggestions:

- ایجاد Issue در GitHub
- Create an Issue on GitHub

---

## نویسنده / Author

**Sobhan Mohammadi**

Copyright (c) 2026
