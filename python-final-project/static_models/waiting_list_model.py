class WaitingListModel:
    _waiting_list = {}

    @classmethod
    def add_to_waiting_list(cls, book_id, member_id):
        if book_id not in cls._waiting_list:
            cls._waiting_list[book_id] = []
        cls._waiting_list[book_id].append(member_id)

    @classmethod
    def get_members_by_book(cls, book_id):
        return cls._waiting_list.get(book_id, [])

    @classmethod
    def get_waiting_list(cls):
        return cls._waiting_list.copy()
