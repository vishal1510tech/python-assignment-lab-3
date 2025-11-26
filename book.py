

from dataclasses import dataclass, asdict

@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # "available" or "issued"

    def __post_init__(self):
        # Normalize status
        self.status = self.status.lower()
        if self.status not in ("available", "issued"):
            self.status = "available"

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - Status: {self.status}"

    def to_dict(self) -> dict:
        return asdict(self)

    def issue(self) -> bool:
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self) -> bool:
        if not self.is_available():
            self.status = "available"
            return True
        return False

    def is_available(self) -> bool:
        return self.status == "available"
