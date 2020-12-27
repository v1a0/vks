from typing import List


class User:
    def __init__(self, uid: int = None, is_closed: bool = True, friends: List[int] = None,
                 hidden_friends: List[int] = None, candidates: List[int] = None):

        if hidden_friends is None:
            hidden_friends = []

        if friends is None:
            friends = []

        if candidates is None:
            candidates = []

        self.id = uid
        self.is_closed = is_closed
        self.friends = friends
        self.hidden_friends = hidden_friends
        self.candidates = candidates
