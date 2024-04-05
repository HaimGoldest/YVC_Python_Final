class UserDataModel:
    _user_name = ''
    _user_type = ''

    @classmethod
    def set_user_data(cls, user_name, user_type):
        cls._user_name = user_name
        cls._user_type = user_type

    @classmethod
    def get_user_name(cls):
        return cls._user_name

    @classmethod
    def get_user_type(cls):
        return cls._user_type
