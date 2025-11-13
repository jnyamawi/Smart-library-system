Smart Library Management System
================================

Files:
- smart_library.py        : Main Python program (single-file)
- books.txt               : JSON file storing books (created/updated by program)
- members.txt             : JSON file storing members (created/updated by program)
- transactions.txt        : JSON file storing transaction history (created/updated by program)
- README.txt              : This file

Requirements:
- Python 3.7+ (tested on 3.8+)
- No external libraries required

How to run:
1. Unzip the project folder.
2. Open a terminal/command prompt and navigate to the unzipped folder.
3. Run: python smart_library.py
4. Follow the menu prompts.

Persistent storage:
- The program reads/writes JSON text into books.txt, members.txt and transactions.txt in the same folder.
- Data persists across runs. Do NOT delete those files if you want to keep data.

Assumptions:
- Book identifiers (book_id) and member identifiers (member_id) are unique (case-insensitive).
- Titles and author searches are case-insensitive.
- Borrowed books stored as book_id references in members.
- For simplicity, no user authentication implemented (members identified by ID in CLI).
- The program uses simple JSON text files per assignment requirement (open, read, write, with statements).

Extra features implemented:
- Tracks times each book is borrowed and displays the "most borrowed book".
- Stores transaction history with timestamps and can display history (all or last N).
- Search books by author (case-insensitive substring match).

Author:
- (Your Name / Student ID) -- replace before submission if desired
