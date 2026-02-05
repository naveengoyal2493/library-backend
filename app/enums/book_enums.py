from enum import Enum

class BookStatus(str, Enum):
    BORROWED = 'borrowed'
    RETURNED = 'returned'
    OVERDUE = 'overdue'