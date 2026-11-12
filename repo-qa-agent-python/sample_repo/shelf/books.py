from shelf.storage import load_books, save_books

MAX_TITLE_LENGTH = 80


def add_book(title, author, path=None):
    """Add a book. Raises ValueError if the title is empty or longer than 80 characters."""
    title = title.strip()
    if not title or len(title) > MAX_TITLE_LENGTH:
        raise ValueError("title must be 1 to 80 characters")
    books = load_books(path) if path else load_books()
    books.append({"title": title, "author": author.strip(), "read": False})
    save_books(books, path) if path else save_books(books)
    return books[-1]


def mark_read(title, path=None):
    """Mark the first book with this title as read. Returns False if no book matches."""
    books = load_books(path) if path else load_books()
    for book in books:
        if book["title"] == title:
            book["read"] = True
            save_books(books, path) if path else save_books(books)
            return True
    return False
