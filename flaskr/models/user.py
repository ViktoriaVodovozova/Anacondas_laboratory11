from dataclasses import dataclass, field

@dataclass
class User:
    email: str
    nickname: str
    password: str
    age: int
    favorite_genre: str
    id: int = field(init=False)
    _id_counter: int = field(init=False, default=1, repr=False)
    def __post_init__(self):
        self.id = User._id_counter
        User._id_counter += 1
