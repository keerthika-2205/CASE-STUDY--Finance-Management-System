class User:
    def __init__(self, user_id=None, username=None, password=None, email=None):
        self._user_id = user_id
        self._username = username
        self._password = password
        self._email = email

    # Getters and Setters
    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value