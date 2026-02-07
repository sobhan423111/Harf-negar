#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harfnegar - Main Entry Point
Persian/Arabic Text Processor

Copyright (c) 2026 Sobhan Mohammadi
Licensed under GPL-2.0
"""

import sys


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # CLI mode
        from cli import main as cli_main
        return cli_main()
    else:
        # GUI mode
        from gui import main as gui_main
        return gui_main()


if __name__ == "__main__":
    sys.exit(main() or 0)
