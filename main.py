from library_manager.book import Book
from library_manager.inventory import LibraryInventory
import logging
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from library_manager.book import Book

LOG_FILE = "library.log"

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

def print_menu() -> None:
    print("\n===== Library Inventory Manager =====")
    print("1. Add Book")
    print("2. Issue Book")
    print("3. Return Book")
    print("4. View All Books")
    print("5. Search Books")
    print("6. Exit")

def get_non_empty_input(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")

def handle_add_book(inventory: LibraryInventory) -> None:
    print("\n--- Add Book ---")
    title = get_non_empty_input("Enter title: ")
    author = get_non_empty_input("Enter author: ")
    isbn = get_non_empty_input("Enter ISBN: ")
    book = Book(title=title, author=author, isbn=isbn)
    try:
        inventory.add_book(book)
        print("Book added successfully.")
    except Exception as e:
        logging.error(f"Error adding book: {e}")
        print("Failed to add book. Please check logs.")

def handle_issue_book(inventory: LibraryInventory) -> None:
    print("\n--- Issue Book ---")
    isbn = get_non_empty_input("Enter ISBN: ")
    book = inventory.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    if book.issue():
        try:
            inventory.save_to_file()
            print("Book issued successfully.")
        except Exception as e:
            logging.error(f"Error issuing book: {e}")
            print("Failed to update file. Please check logs.")
    else:
        print("Book is already issued.")

def handle_return_book(inventory: LibraryInventory) -> None:
    print("\n--- Return Book ---")
    isbn = get_non_empty_input("Enter ISBN: ")
    book = inventory.search_by_isbn(isbn)
    if not book:
        print("Book not found.")
        return
    if book.return_book():
        try:
            inventory.save_to_file()
            print("Book returned successfully.")
        except Exception as e:
            logging.error(f"Error returning book: {e}")
            print("Failed to update file. Please check logs.")
    else:
        print("Book was not issued.")

def handle_view_all(inventory: LibraryInventory) -> None:
    print("\n--- All Books ---")
    books = inventory.display_all()
    if not books:
        print("No books in inventory.")
        return
    for book in books:
        print(book)

def handle_search(inventory: LibraryInventory) -> None:
    print("\n--- Search Books ---")
    print("1. Search by Title")
    print("2. Search by ISBN")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        title = get_non_empty_input("Enter title to search: ")
        results = inventory.search_by_title(title)
        if results:
            print(f"\nFound {len(results)} book(s):")
            for book in results:
                print(book)
        else:
            print("No books found with that title.")
    elif choice == "2":
        isbn = get_non_empty_input("Enter ISBN to search: ")
        book = inventory.search_by_isbn(isbn)
        if book:
            print("\nBook found:")
            print(book)
        else:
            print("No book found with that ISBN.")
    else:
        print("Invalid choice.")

def main() -> None:
    configure_logging()
    logging.info("Starting Library Inventory Manager CLI")
    inventory = LibraryInventory()

    while True:
        print_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                handle_add_book(inventory)
            elif choice == "2":
                handle_issue_book(inventory)
            elif choice == "3":
                handle_return_book(inventory)
            elif choice == "4":
                handle_view_all(inventory)
            elif choice == "5":
                handle_search(inventory)
            elif choice == "6":
                print("Exiting... Goodbye!")
                logging.info("Exiting Library Inventory Manager CLI")
                break
            else:
                print("Invalid choice. Please select a number between 1 and 6.")
        except Exception as e:
            logging.error(f"Unhandled error in main loop: {e}")
            print("An unexpected error occurred. Please check logs.")

if __name__ == "__main__":
    main()
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

