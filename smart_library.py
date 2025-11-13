"""
smart_library.py
Smart Library Management System
Single-file implementation using OOP and file handling.
Run: python smart_library.py
"""

import json
import os
from datetime import datetime
from typing import List, Optional

def safe_load_json(filepath: str):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        return []

def safe_save_json(filepath: str, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

class Book:
    def __init__(self, book_id: str, title: str, author: str, available_copies: int):
        self.book_id = book_id.strip()
        self.title = title.strip()
        self.author = author.strip()
        self.available_copies = int(available_copies)
        self.times_borrowed = 0

    def display_info(self) -> str:
        return (f"Book ID: {self.book_id} | Title: {self.title} | "
                f"Author: {self.author} | Available: {self.available_copies} | "
                f"Borrowed: {self.times_borrowed}")

    def update_copies(self, number: int):
        self.available_copies += number
        if self.available_copies < 0:
            self.available_copies = 0

    def to_dict(self) -> dict:
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "available_copies": self.available_copies,
            "times_borrowed": self.times_borrowed,
        }

    @classmethod
    def from_dict(cls, data: dict):
        b = cls(
            book_id=data.get("book_id", ""),
            title=data.get("title", ""),
            author=data.get("author", ""),
            available_copies=int(data.get("available_copies", 0)),
        )
        b.times_borrowed = int(data.get("times_borrowed", 0))
        return b

class Member:
    def __init__(self, member_id: str, name: str):
        self.member_id = member_id.strip()
        self.name = name.strip()
        self.borrowed_books: List[str] = []

    def borrow_book(self, book: Book) -> bool:
        if book.available_copies <= 0:
            return False
        book.update_copies(-1)
        book.times_borrowed += 1
        self.borrowed_books.append(book.book_id)
        return True

    def return_book(self, book: Book) -> bool:
        if book.book_id not in self.borrowed_books:
            return False
        book.update_copies(1)
        self.borrowed_books.remove(book.book_id)
        return True

    def display_member_info(self) -> str:
        borrowed = ", ".join(self.borrowed_books) if self.borrowed_books else "None"
        return f"Member ID: {self.member_id} | Name: {self.name} | Borrowed Books: {borrowed}"

    def to_dict(self) -> dict:
        return {
            "member_id": self.member_id,
            "name": self.name,
            "borrowed_books": self.borrowed_books,
        }

    @classmethod
    def from_dict(cls, data: dict):
        m = cls(member_id=data.get("member_id", ""), name=data.get("name", ""))
        m.borrowed_books = list(data.get("borrowed_books", []))
        return m

class Library:
    BOOKS_FILE = "books.txt"
    MEMBERS_FILE = "members.txt"
    TRANSACTIONS_FILE = "transactions.txt"

    def __init__(self):
        self.books: List[Book] = []
        self.members: List[Member] = []
        self.transactions: List[dict] = []
        self.load_all()

    def load_all(self):
        books_data = safe_load_json(self.BOOKS_FILE)
        self.books = [Book.from_dict(b) for b in books_data]
        members_data = safe_load_json(self.MEMBERS_FILE)
        self.members = [Member.from_dict(m) for m in members_data]
        self.transactions = safe_load_json(self.TRANSACTIONS_FILE)

    def save_all(self):
        safe_save_json(self.BOOKS_FILE, [b.to_dict() for b in self.books])
        safe_save_json(self.MEMBERS_FILE, [m.to_dict() for m in self.members])
        safe_save_json(self.TRANSACTIONS_FILE, self.transactions)

    def add_book(self, book: Book) -> bool:
        if self.find_book_by_id(book.book_id):
            return False
        self.books.append(book)
        self.save_all()
        return True

    def add_member(self, member: Member) -> bool:
        if self.find_member_by_id(member.member_id):
            return False
        self.members.append(member)
        self.save_all()
        return True

    def display_all_books(self):
        if not self.books:
            print("No books in the library.")
            return
        for book in self.books:
            print(book.display_info())

    def display_all_members(self):
        if not self.members:
            print("No members registered.")
            return
        for member in self.members:
            print(member.display_member_info())

    def find_book_by_id(self, book_id: str) -> Optional[Book]:
        for book in self.books:
            if book.book_id.lower() == book_id.strip().lower():
                return book
        return None

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.strip().lower():
                return book
        return None

    def find_member_by_id(self, member_id: str) -> Optional[Member]:
        for member in self.members:
            if member.member_id.lower() == member_id.strip().lower():
                return member
        return None

    def borrow_transaction(self, member_id: str, book_title: str) -> bool:
        member = self.find_member_by_id(member_id)
        if not member:
            print(f"No member with ID '{member_id}' found.")
            return False
        book = self.find_book_by_title(book_title)
        if not book:
            print(f"No book titled '{book_title}' found.")
            return False
        if book.available_copies <= 0:
            print(f"'{book.title}' is currently unavailable.")
            return False
        success = member.borrow_book(book)
        if success:
            self.record_transaction("BORROW", member, book)
            self.save_all()
            print(f"Book '{book.title}' borrowed successfully by {member.name}.")
            return True
        print("Borrow failed due to unknown reason.")
        return False

    def return_transaction(self, member_id: str, book_title: str) -> bool:
        member = self.find_member_by_id(member_id)
        if not member:
            print(f"No member with ID '{member_id}' found.")
            return False
        book = self.find_book_by_title(book_title)
        if not book:
            print(f"No book titled '{book_title}' found.")
            return False
        if book.book_id not in member.borrowed_books:
            print(f"Member {member.name} has not borrowed '{book.title}'.")
            return False
        success = member.return_book(book)
        if success:
            self.record_transaction("RETURN", member, book)
            self.save_all()
            print(f"Book '{book.title}' returned successfully by {member.name}.")
            return True
        print("Return failed.")
        return False

    def record_transaction(self, tx_type: str, member: Member, book: Book):
        tx = {
            "type": tx_type,
            "member_id": member.member_id,
            "member_name": member.name,
            "book_id": book.book_id,
            "book_title": book.title,
            "author": book.author,
            "timestamp": datetime.now().isoformat(sep=" ", timespec="seconds"),
        }
        self.transactions.append(tx)

    def display_transaction_history(self, limit: Optional[int] = None):
        if not self.transactions:
            print("No transactions recorded yet.")
            return
        to_show = self.transactions[-limit:] if limit else self.transactions
        print("Transaction History:")
        for tx in to_show:
            print(f"{tx['timestamp']} | {tx['type']} | Member: {tx['member_name']} "
                  f"({tx['member_id']}) | Book: {tx['book_title']} ({tx['book_id']})")

    def most_borrowed_book(self) -> Optional[Book]:
        if not self.books:
            return None
        return max(self.books, key=lambda b: b.times_borrowed)

    def search_by_author(self, author_name: str) -> List[Book]:
        query = author_name.strip().lower()
        return [b for b in self.books if query in b.author.lower()]

    def seed_sample(self):
        if self.books or self.members:
            return
        sample_books = [
            Book("B001", "Python for Beginners", "Jane Doe", 5),
            Book("B002", "Data Structures", "John Smith", 3),
            Book("B003", "Machine Learning 101", "Alice Johnson", 2),
        ]
        sample_members = [
            Member("M001", "Alice"),
            Member("M002", "Bob"),
        ]
        self.books.extend(sample_books)
        self.members.extend(sample_members)
        self.save_all()

def menu():
    lib = Library()
    lib.seed_sample()

    while True:
        print("\n===== SMART LIBRARY MANAGEMENT SYSTEM =====\n")
        print("1. Add New Book")
        print("2. Add New Member")
        print("3. Display All Books")
        print("4. Display All Members")
        print("5. Borrow Book")
        print("6. Return Book")
        print("7. Search Books by Author")
        print("8. Display Most Borrowed Book")
        print("9. Display Transaction History")
        print("10. Exit\n")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            book_id = input("Enter Book ID: ").strip()
            title = input("Enter Title: ").strip()
            author = input("Enter Author: ").strip()
            try:
                copies = int(input("Enter Available Copies: ").strip())
            except ValueError:
                print("Invalid number for copies. Operation cancelled.")
                continue
            book = Book(book_id, title, author, copies)
            if lib.add_book(book):
                print("Book added successfully!")
            else:
                print(f"Book with ID '{book_id}' already exists. Try updating instead.")
        elif choice == "2":
            member_id = input("Enter Member ID: ").strip()
            name = input("Enter Name: ").strip()
            member = Member(member_id, name)
            if lib.add_member(member):
                print("Member added successfully!")
            else:
                print(f"Member with ID '{member_id}' already exists.")
        elif choice == "3":
            print("\nAll Books:")
            lib.display_all_books()
        elif choice == "4":
            print("\nAll Members:")
            lib.display_all_members()
        elif choice == "5":
            member_id = input("Enter Member ID: ").strip()
            book_title = input("Enter Book Title: ").strip()
            lib.borrow_transaction(member_id, book_title)
        elif choice == "6":
            member_id = input("Enter Member ID: ").strip()
            book_title = input("Enter Book Title: ").strip()
            lib.return_transaction(member_id, book_title)
        elif choice == "7":
            author_q = input("Enter author name or substring to search: ").strip()
            matches = lib.search_by_author(author_q)
            if not matches:
                print("No books match that author.")
            else:
                print("Matching books:")
                for b in matches:
                    print(b.display_info())
        elif choice == "8":
            mb = lib.most_borrowed_book()
            if not mb:
                print("No books tracked yet.")
            else:
                print("Most Borrowed Book:")
                print(mb.display_info())
        elif choice == "9":
            try:
                lim_in = input("Show last N transactions? Enter N or press Enter for all: ").strip()
                limit = int(lim_in) if lim_in else None
            except ValueError:
                limit = None
            lib.display_transaction_history(limit)
        elif choice == "10":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a number from the menu.")

if __name__ == "__main__":
    menu()
