import sys

from shelf.books import add_book
from shelf.storage import load_books


def main(argv):
    if len(argv) >= 3 and argv[0] == "add":
        book = add_book(argv[1], argv[2])
        print(f"added: {book['title']}")
    elif argv[:1] == ["list"]:
        for book in load_books():
            mark = "x" if book["read"] else " "
            print(f"[{mark}] {book['title']} - {book['author']}")
    else:
        print("usage: cli.py add TITLE AUTHOR | list")


if __name__ == "__main__":
    main(sys.argv[1:])
