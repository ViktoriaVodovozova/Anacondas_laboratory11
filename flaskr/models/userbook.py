from dataclasses import dataclass

@dataclass
class UserBook:
    user_id: int
    book_id: int
    rating: int | None = None      # оценка от 1 до 5 (или None)
    review: str | None = None      # текст отзыва