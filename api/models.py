from dataclasses import dataclass
from datetime import datetime
from typing import List, Self

@dataclass
class User:
    # id: str
    username: str
    password: str

    # def is_online(self) -> bool:
    #     return bool(get_session(self.id))
    #
    # def get_friends(self) -> List[Self]:
    #     pass


@dataclass
class Chat:
    id: str

@dataclass
class Message:
    sender: User
    chat_id: str
    content: str
    timestamp: datetime
    


