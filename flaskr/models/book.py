from dataclasses import dataclass, field

@dataclass
class Book:
    name: str
    author: str
    year: int
    annotation: str
    genre: str
    id: int = field(init=False)
    _id_counter: int = field(init=False, default=1, repr=False)
    def __post_init__(self):
        self.id = Book._id_counter
        Book._id_counter += 1