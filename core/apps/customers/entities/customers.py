from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    id: int
    created_at: datetime
    updated_at: datetime
    username: str
    phone: str
