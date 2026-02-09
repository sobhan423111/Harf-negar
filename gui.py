# -*- coding: utf-8 -*-
"""Harfnegar GUI v1.4.2 - Universal File Editor
Copyright (c) 2026 Sobhan Mohammadi - GPL-2.0"""
import sys, os, platform, json, yaml, polib
from xml.etree import ElementTree as ET
from xml.dom import minidom
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import pyperclip
from text_processor import TextProcessor
from database_manager import DatabaseManager
from language_manager import LanguageManager

class UniversalFileEditor(QDialog):
    """Universal editor for PO/JSON/YAML/XML files"""
    def __init__(self, parent, lang, filepath, db):
        super().__init__(parent)
        self.lang = lang
        self.filepath = filepath
        self.db = db
        self.file_type = os.path.splitext(filepath)[1].lower()
        self.data = None
        
        title_map = {'.po': 'po_editor', '.json': 'json_editor', '.yaml': 'yaml_editor', '.yml': 'yaml_editor', '.xml': 'xml_editor'}
        self.setWindowTitle(lang.get(title_map.get(self.file_type, 'file')))
        self.resize(1400, 800)
        
        layout = QVBoxLayout()
        
        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel(lang.get('search') + ':'))
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.filter_entries)
        toolbar.addWidget(self.search_input)
        
        if self.file_type == '.po':
            self.filter_combo = QComboBox()
            self.filter_combo.addItems([lang.get('show_all'), lang.get('untranslated'), lang.get('translated'), lang.get('fuzzy')])
            self.filter_combo.currentTextChanged.connect(self.filter_entries)
            toolbar.addWidget(self.filter_combo)
        
        # Buttons
        self.select_btn = QPushButton(lang.get('select_text'))
        self.select_btn.clicked.connect(self.select_current_text)
        toolbar.addWidget(self.select_btn)
        
        self.process_sel_btn = QPushButton(lang.get('process_selected'))
        self.process_sel_btn.clicked.connect(self.process_selected)
        toolbar.addWidget(self.process_sel_btn)
        
        self.process_all_btn = QPushButton(lang.get('process_all'))
        self.process_all_btn.clicked.connect(self.process_all)
        toolbar.addWidget(self.process_all_btn)
        
        save_btn = QPushButton(lang.get('save'))
        save_btn.clicked.connect(self.save_file)
        toolbar.addWidget(save_btn)
        
        layout.addLayout(toolbar)
        
        # Table
        self.table = QTableWidget()
        self.setup_table()
        layout.addWidget(self.table)
        
        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        close_btn = QPushButton(lang.get('close'))
        close_btn.clicked.connect(self.reject)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        self.load_file()
    
    def setup_table(self):
        if self.file_type == '.po':
            self.table.setColumnCount(4)
            self.table.setHorizontalHeaderLabels([self.lang.get('msgid'), self.lang.get('msgstr'), self.lang.get('comment'), self.lang.get('fuzzy')])
        else:
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels([self.lang.get('key'), self.lang.get('value'), self.lang.get('comment')])
        
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)
    
    def load_file(self):
        try:
            if self.file_type == '.po':
                self.load_po()
            elif self.file_type == '.json':
                self.load_json()
            elif self.file_type in ['.yaml', '.yml']:
                self.load_yaml()
            elif self.file_type == '.xml':
                self.load_xml()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load: {str(e)}')
    
    def load_po(self):
        self.data = polib.pofile(self.filepath)
        self.table.setRowCount(0)
        for entry in self.data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(entry.msgid))
            self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row, 1, QTableWidgetItem(entry.msgstr))
            self.table.setItem(row, 2, QTableWidgetItem(entry.comment or ''))
            
            fuzzy_cb = QCheckBox()
            fuzzy_cb.setChecked('fuzzy' in entry.flags)
            self.table.setCellWidget(row, 3, fuzzy_cb)
    
    def load_json(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.populate_dict(self.data)
    
    def load_yaml(self):
        with open(self.filepath, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)
        self.populate_dict(self.data)
    
    def load_xml(self):
        tree = ET.parse(self.filepath)
        self.data = tree.getroot()
        self.populate_xml(self.data)
    
    def populate_dict(self, data, prefix=''):
        """Populate table from dict (JSON/YAML)"""
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                if isinstance(value, (dict, list)):
                    self.populate_dict(value, full_key)
                else:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setItem(row, 0, QTableWidgetItem(full_key))
                    self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, 1, QTableWidgetItem(str(value)))
                    self.table.setItem(row, 2, QTableWidgetItem(''))
        elif isinstance(data, list):
            for i, value in enumerate(data):
                full_key = f"{prefix}[{i}]"
                if isinstance(value, (dict, list)):
                    self.populate_dict(value, full_key)
                else:
                    row = self.table.rowCount()
                    self.table.insertRow(row)
                    self.table.setItem(row, 0, QTableWidgetItem(full_key))
                    self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)
                    self.table.setItem(row, 1, QTableWidgetItem(str(value)))
                    self.table.setItem(row, 2, QTableWidgetItem(''))
    
    def populate_xml(self, root, prefix=''):
        """Populate table from XML"""
        for child in root:
            tag = f"{prefix}.{child.tag}" if prefix else child.tag
            
            # Add element with text
            if child.text and child.text.strip():
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(tag))
                self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 1, QTableWidgetItem(child.text.strip()))
                self.table.setItem(row, 2, QTableWidgetItem(''))
            
            # Add attributes
            for attr, value in child.attrib.items():
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(f"{tag}[@{attr}]"))
                self.table.item(row, 0).setFlags(self.table.item(row, 0).flags() & ~Qt.ItemIsEditable)
                self.table.setItem(row, 1, QTableWidgetItem(value))
                self.table.setItem(row, 2, QTableWidgetItem('attribute'))
            
            # Recurse
            if len(child) > 0:
                self.populate_xml(child, tag)
    
    def filter_entries(self):
        search = self.search_input.text().lower()
        
        for row in range(self.table.rowCount()):
            show = True
            
            if search:
                col0 = self.table.item(row, 0).text().lower()
                col1 = self.table.item(row, 1).text().lower()
                show = search in col0 or search in col1
            
            if show and self.file_type == '.po':
                filter_type = self.filter_combo.currentText()
                if filter_type != self.lang.get('show_all'):
                    msgstr = self.table.item(row, 1).text()
                    fuzzy = self.table.cellWidget(row, 3).isChecked()
                    
                    if filter_type == self.lang.get('untranslated'):
                        show = not msgstr
                    elif filter_type == self.lang.get('translated'):
                        show = bool(msgstr) and not fuzzy
                    elif filter_type == self.lang.get('fuzzy'):
                        show = fuzzy
            
            self.table.setRowHidden(row, not show)
    
    def select_current_text(self):
        """Select entire text in current cell"""
        current_item = self.table.currentItem()
        if current_item and current_item.column() in [0, 1]:
            # Select all text in the cell
            self.table.editItem(current_item)
            # Trigger select all in the editor
            if self.table.currentItem():
                cursor = self.table.itemWidget(self.table.currentRow(), self.table.currentColumn())
                if hasattr(cursor, 'selectAll'):
                    cursor.selectAll()
    
    def process_selected(self):
        """Process selected rows or selected text"""
        exceptions = self.db.get_exception_patterns()
        
        for item in self.table.selectedItems():
            row = item.row()
            if item.column() == 1:  # Value column
                text = item.text()
                if text:
                    # Process with bidi + reshaper
                    processed = TextProcessor.encode_text(text, exceptions)
                    item.setText(processed)
    
    def process_all(self):
        """Process all visible rows"""
        exceptions = self.db.get_exception_patterns()
        
        for row in range(self.table.rowCount()):
            if not self.table.isRowHidden(row):
                value_item = self.table.item(row, 1)
                if value_item:
                    text = value_item.text()
                    if text and (self.file_type != '.po' or not text):  # For PO, only untranslated
                        processed = TextProcessor.encode_text(text, exceptions)
                        value_item.setText(processed)
    
    def save_file(self):
        try:
            if self.file_type == '.po':
                self.save_po()
            elif self.file_type == '.json':
                self.save_json()
            elif self.file_type in ['.yaml', '.yml']:
                self.save_yaml()
            elif self.file_type == '.xml':
                self.save_xml()
            
            QMessageBox.information(self, 'Success', 'File saved')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to save: {str(e)}')
    
    def save_po(self):
        for row in range(self.table.rowCount()):
            msgid = self.table.item(row, 0).text()
            msgstr = self.table.item(row, 1).text()
            comment = self.table.item(row, 2).text()
            fuzzy = self.table.cellWidget(row, 3).isChecked()
            
            for entry in self.data:
                if entry.msgid == msgid:
                    entry.msgstr = msgstr
                    entry.comment = comment
                    if fuzzy and 'fuzzy' not in entry.flags:
                        entry.flags.append('fuzzy')
                    elif not fuzzy and 'fuzzy' in entry.flags:
                        entry.flags.remove('fuzzy')
                    break
        
        self.data.save(self.filepath)
    
    def save_json(self):
        # Rebuild dict from table
        new_data = {}
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            value = self.table.item(row, 1).text()
            self.set_nested(new_data, key, value)
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    def save_yaml(self):
        new_data = {}
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            value = self.table.item(row, 1).text()
            self.set_nested(new_data, key, value)
        
        with open(self.filepath, 'w', encoding='utf-8') as f:
            yaml.dump(new_data, f, allow_unicode=True, default_flow_style=False)
    
    def save_xml(self):
        # Update XML tree from table
        for row in range(self.table.rowCount()):
            key = self.table.item(row, 0).text()
            value = self.table.item(row, 1).text()
            
            if '@' in key:  # Attribute
                tag, attr = key.rsplit('[@', 1)
                attr = attr.rstrip(']')
                element = self.find_element(self.data, tag)
                if element is not None:
                    element.set(attr, value)
            else:  # Text
                element = self.find_element(self.data, key)
                if element is not None:
                    element.text = value
        
        tree = ET.ElementTree(self.data)
        tree.write(self.filepath, encoding='utf-8', xml_declaration=True)
    
    def set_nested(self, data, key, value):
        """Set nested dict value from dotted key"""
        parts = key.replace('[', '.').replace(']', '').split('.')
        current = data
        for part in parts[:-1]:
            if part.isdigit():
                part = int(part)
                if not isinstance(current, list):
                    current = []
                while len(current) <= part:
                    current.append({})
                current = current[part]
            else:
                if part not in current:
                    current[part] = {}
                current = current[part]
        
        last_key = parts[-1]
        if last_key.isdigit():
            last_key = int(last_key)
        current[last_key] = value
    
    def find_element(self, root, path):
        """Find XML element by dotted path"""
        parts = path.split('.')
        current = root
        for part in parts:
            found = False
            for child in current:
                if child.tag == part:
                    current = child
                    found = True
                    break
            if not found:
                return None
        return current

class HarfnegarGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.lang = LanguageManager(self.db)
        self.zoom_level = 0
        self.history = []
        
        try:
            self.history = self.db.get_history(10)
        except:
            pass
        
        self.input_timer = QTimer()
        self.input_timer.setSingleShot(True)
        self.input_timer.timeout.connect(self.process_input)
        
        self.copy_timer = QTimer()
        self.copy_timer.setSingleShot(True)
        self.copy_timer.timeout.connect(self.delayed_copy)
        
        self.clipboard_timer = QTimer()
        self.clipboard_timer.timeout.connect(self.monitor_clipboard)
        self.clipboard_timer.start(1000)
        
        self.last_clipboard = ""
        self.pending_copy = ""
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        self.setWindowTitle(f"{self.lang.get('app_name')} v1.4.2")
        self.resize(self.db.get_int('window_width', 1200), self.db.get_int('window_height', 800))
        
        icon_path = 'icon.ico' if platform.system() == 'Windows' else 'icon.png'
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        main_layout.addWidget(QLabel(self.lang.get('input')))
        self.txt_input = QTextEdit()
        self.txt_input.textChanged.connect(self.on_input_change)
        main_layout.addWidget(self.txt_input, 1)
        
        main_layout.addWidget(QLabel(self.lang.get('output')))
        self.txt_output = QTextEdit()
        self.txt_output.textChanged.connect(self.on_output_change)
        main_layout.addWidget(self.txt_output, 1)
        
        ctrl_layout = QHBoxLayout()
        self.auto_copy_cb = QCheckBox(self.lang.get('auto_copy'))
        self.auto_copy_cb.setChecked(self.db.get_bool('auto_copy', True))
        ctrl_layout.addWidget(self.auto_copy_cb)
        
        clear_btn = QPushButton(self.lang.get('clear'))
        clear_btn.clicked.connect(self.clear_all)
        ctrl_layout.addWidget(clear_btn)
        ctrl_layout.addStretch()
        
        process_btn = QPushButton(self.lang.get('process'))
        process_btn.clicked.connect(self.force_process)
        ctrl_layout.addWidget(process_btn)
        
        copy_btn = QPushButton(self.lang.get('copy'))
        copy_btn.clicked.connect(self.copy_output)
        ctrl_layout.addWidget(copy_btn)
        main_layout.addLayout(ctrl_layout)
        
        self.status = self.statusBar()
        self.char_label = QLabel(f"0 {self.lang.get('chars')}")
        self.status.addPermanentWidget(self.char_label)
        self.word_label = QLabel(f"0 {self.lang.get('words')}")
        self.status.addPermanentWidget(self.word_label)
        
        self.create_menu()
    
    def create_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu(self.lang.get('file'))
        file_menu.addAction(self.lang.get('new'), self.new_file)
        file_menu.addAction(self.lang.get('open'), self.open_file)
        file_menu.addAction(self.lang.get('save'), self.save_file)
        file_menu.addSeparator()
        
        self.recent_menu = file_menu.addMenu(self.lang.get('recent'))
        self.update_recent_menu()
        
        file_menu.addSeparator()
        file_menu.addAction(self.lang.get('exit'), self.close)
        
        edit_menu = menubar.addMenu(self.lang.get('edit'))
        edit_menu.addAction(self.lang.get('undo'), self.undo)
        edit_menu.addAction(self.lang.get('redo'), self.redo)
        edit_menu.addSeparator()
        edit_menu.addAction(self.lang.get('cut'), self.cut_text)
        edit_menu.addAction(self.lang.get('copy'), self.copy_text)
        edit_menu.addAction(self.lang.get('paste'), self.paste_text)
        edit_menu.addAction(self.lang.get('select_all'), self.select_all)
        
        view_menu = menubar.addMenu(self.lang.get('view'))
        view_menu.addAction(self.lang.get('zoom_in'), self.zoom_in)
        view_menu.addAction(self.lang.get('zoom_out'), self.zoom_out)
        view_menu.addAction(self.lang.get('reset'), self.reset_zoom)
        view_menu.addSeparator()
        view_menu.addAction(self.lang.get('stats'), self.show_statistics)
        
        tools_menu = menubar.addMenu(self.lang.get('tools'))
        tools_menu.addAction(self.lang.get('po_editor'), lambda: self.open_file_editor('.po'))
        tools_menu.addAction(self.lang.get('json_editor'), lambda: self.open_file_editor('.json'))
        tools_menu.addAction(self.lang.get('yaml_editor'), lambda: self.open_file_editor('.yaml'))
        tools_menu.addAction(self.lang.get('xml_editor'), lambda: self.open_file_editor('.xml'))
        tools_menu.addSeparator()
        tools_menu.addAction(self.lang.get('font'), self.font_settings)
        tools_menu.addSeparator()
        
        self.top_action = QAction(self.lang.get('always_on_top'), self, checkable=True)
        self.top_action.setChecked(self.db.get_bool('always_on_top'))
        self.top_action.triggered.connect(self.toggle_on_top)
        tools_menu.addAction(self.top_action)
        
        self.quick_action = QAction(self.lang.get('quick_mode'), self, checkable=True)
        self.quick_action.setChecked(self.db.get_bool('quick_mode', True))
        tools_menu.addAction(self.quick_action)
        
        theme_menu = tools_menu.addMenu(self.lang.get('theme'))
        self.theme_group = QActionGroup(self)
        current_theme = self.db.get('theme', 'light')
        
        for theme in ['light', 'dark']:
            action = QAction(self.lang.get(theme), self, checkable=True)
            action.triggered.connect(lambda checked, t=theme: self.set_theme(t))
            self.theme_group.addAction(action)
            theme_menu.addAction(action)
            if current_theme == theme:
                action.setChecked(True)
        
        help_menu = menubar.addMenu(self.lang.get('help'))
        help_menu.addAction(self.lang.get('about'), self.show_about)
    
    def apply_theme(self):
        theme = self.db.get('theme', 'light')
        app = QApplication.instance()
        
        if theme == 'dark':
            app.setStyle('Fusion')
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(35, 35, 35))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            palette.setColor(QPalette.ToolTipBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipText, Qt.white)
            app.setPalette(palette)
        else:
            app.setStyle('Fusion')
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(240, 240, 240))
            palette.setColor(QPalette.WindowText, Qt.black)
            palette.setColor(QPalette.Base, Qt.white)
            palette.setColor(QPalette.AlternateBase, QColor(245, 245, 245))
            palette.setColor(QPalette.Text, Qt.black)
            palette.setColor(QPalette.Button, QColor(240, 240, 240))
            palette.setColor(QPalette.ButtonText, Qt.black)
            palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
            palette.setColor(QPalette.HighlightedText, Qt.white)
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.black)
            app.setPalette(palette)
        
        # Apply to text edits
        if theme == 'dark':
            self.txt_input.setStyleSheet("QTextEdit { background-color: #2b2b2b; color: white; }")
            self.txt_output.setStyleSheet("QTextEdit { background-color: #2b2b2b; color: white; }")
        else:
            self.txt_input.setStyleSheet("QTextEdit { background-color: white; color: black; }")
            self.txt_output.setStyleSheet("QTextEdit { background-color: #f5fff5; color: black; }")
    
    def set_theme(self, theme):
        self.db.set('theme', theme)
        self.apply_theme()
    
    def on_input_change(self):
        if hasattr(self, '_updating') and self._updating:
            return
        text = self.txt_input.toPlainText()
        self.char_label.setText(f"{len(text)} {self.lang.get('chars')}")
        words = len(text.split()) if text.strip() else 0
        self.word_label.setText(f"{words} {self.lang.get('words')}")
        self.input_timer.stop()
        self.input_timer.start(100)
    
    def process_input(self):
        self._updating = True
        text = self.txt_input.toPlainText()
        if text:
            exceptions = self.db.get_exception_patterns()
            result = TextProcessor.encode_text(text, exceptions)
            self.txt_output.setPlainText(result)
            
            if self.auto_copy_cb.isChecked():
                self.pending_copy = result
                self.copy_timer.stop()
                self.copy_timer.start(500)
            
            if self.db.get_bool('auto_save', True):
                try:
                    self.db.add_history(text, result)
                    self.history = self.db.get_history(10)
                    self.update_recent_menu()
                except:
                    pass
        else:
            self.txt_output.clear()
        self._updating = False
    
    def delayed_copy(self):
        if self.pending_copy and self.auto_copy_cb.isChecked():
            try:
                pyperclip.copy(self.pending_copy)
            except: pass
    
    def on_output_change(self):
        if hasattr(self, '_updating') and self._updating:
            return
        self._updating = True
        text = self.txt_output.toPlainText()
        if text:
            result = TextProcessor.decode_text(text)
            self.txt_input.setPlainText(result)
        self._updating = False
    
    def force_process(self):
        self.process_input()
    
    def clear_all(self):
        self.txt_input.clear()
        self.txt_output.clear()
    
    def new_file(self):
        if QMessageBox.question(self, 'New', 'Create new?') == QMessageBox.Yes:
            self.clear_all()
    
    def open_file(self):
        fn, _ = QFileDialog.getOpenFileName(self, 'Open', '', 'All Files (*.*);;PO (*.po);;JSON (*.json);;YAML (*.yaml *.yml);;XML (*.xml)')
        if fn:
            try:
                ext = os.path.splitext(fn)[1].lower()
                if ext in ['.po', '.json', '.yaml', '.yml', '.xml']:
                    UniversalFileEditor(self, self.lang, fn, self.db).exec()
                else:
                    text = TextProcessor.read_file(fn)
                    self.txt_input.setPlainText(text)
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))
    
    def open_file_editor(self, ext):
        filters = {'.po': 'PO (*.po)', '.json': 'JSON (*.json)', '.yaml': 'YAML (*.yaml *.yml)', '.xml': 'XML (*.xml)'}
        fn, _ = QFileDialog.getOpenFileName(self, 'Open', '', filters.get(ext, 'All (*.*)'))
        if fn:
            UniversalFileEditor(self, self.lang, fn, self.db).exec()
    
    def save_file(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Save', '', 'Text (*.txt);;HTML (*.html)')
        if fn:
            try:
                with open(fn, 'w', encoding='utf-8') as f:
                    f.write(self.txt_output.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, 'Error', str(e))
    
    def undo(self):
        (self.txt_input if self.txt_input.hasFocus() else self.txt_output).undo()
    
    def redo(self):
        (self.txt_input if self.txt_input.hasFocus() else self.txt_output).redo()
    
    def cut_text(self):
        (self.txt_input if self.txt_input.hasFocus() else self.txt_output).cut()
    
    def select_all(self):
        (self.txt_input if self.txt_input.hasFocus() else self.txt_output).selectAll()
    
    def copy_text(self):
        (self.txt_input if self.txt_input.hasFocus() else self.txt_output).copy()
    
    def paste_text(self):
        (self.txt_input if self.txt_input.hasFocus() else self.txt_output).paste()
    
    def copy_output(self):
        try:
            pyperclip.copy(self.txt_output.toPlainText())
        except: pass
    
    def font_settings(self):
        font, ok = QFontDialog.getFont(self.txt_input.font(), self)
        if ok:
            self.txt_input.setFont(font)
            self.txt_output.setFont(font)
            self.db.set('font_family', font.family())
            self.db.set('font_size', font.pointSize())
    
    def toggle_on_top(self):
        flags = self.windowFlags()
        if self.top_action.isChecked():
            self.setWindowFlags(flags | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(flags & ~Qt.WindowStaysOnTopHint)
        self.show()
        self.db.set('always_on_top', self.top_action.isChecked())
    
    def zoom_in(self):
        self.zoom_level += 1
        self.apply_zoom()
    
    def zoom_out(self):
        self.zoom_level -= 1
        self.apply_zoom()
    
    def reset_zoom(self):
        self.zoom_level = 0
        self.apply_zoom()
    
    def apply_zoom(self):
        font = self.txt_input.font()
        base = self.db.get_int('font_size', 11)
        new_size = max(8, base + self.zoom_level)
        font.setPointSize(new_size)
        self.txt_input.setFont(font)
        self.txt_output.setFont(font)
    
    def update_recent_menu(self):
        self.recent_menu.clear()
        if not self.history:
            self.recent_menu.addAction('(Empty)').setEnabled(False)
            return
        for i, (inp, out, ts) in enumerate(self.history[:5], 1):
            preview = inp[:30] + '...' if len(inp) > 30 else inp
            action = self.recent_menu.addAction(f"{i}. {preview}")
            action.triggered.connect(lambda checked, t=inp: self.txt_input.setPlainText(t))
    
    def show_statistics(self):
        text = self.txt_input.toPlainText()
        lines = text.count('\n') + 1 if text else 0
        chars = len(text)
        words = len(text.split()) if text.strip() else 0
        persian = sum(1 for c in text if TextProcessor.is_persian_arabic(c))
        
        QMessageBox.information(self, self.lang.get('stats'),
            f"Lines: {lines}\nWords: {words}\nChars: {chars}\nPersian/Arabic: {persian}"
        )
    
    def monitor_clipboard(self):
        if self.quick_action.isChecked():
            try:
                text = pyperclip.paste()
                if text and text != self.last_clipboard:
                    self.last_clipboard = text
                    if any(TextProcessor.is_persian_arabic(c) for c in text):
                        exceptions = self.db.get_exception_patterns()
                        result = TextProcessor.encode_text(text, exceptions)
                        pyperclip.copy(result)
            except: pass
    
    def show_about(self):
        QMessageBox.about(self, self.lang.get('about'),
            f"{self.lang.get('app_name')} v1.4.2\n\n"
            "Universal File Editor\n"
            "PO • JSON • YAML • XML\n\n"
            "Copyright (c) 2026 Sobhan Mohammadi\n"
            "GPL-2.0 License"
        )
    
    def closeEvent(self, event):
        self.db.set('window_width', self.width())
        self.db.set('window_height', self.height())
        self.db.set('auto_copy', self.auto_copy_cb.isChecked())
        self.db.set('quick_mode', self.quick_action.isChecked())
        self.db.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = HarfnegarGUI()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
