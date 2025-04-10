class Expense:
    def __init__(self, expense_id=None, user_id=None, amount=None, category_id=None, date=None, description=None):
        self._expense_id = expense_id
        self._user_id = user_id
        self._amount = amount
        self._category_id = category_id
        self._date = date
        self._description = description

    # Getters and Setters
    @property
    def expense_id(self):
        return self._expense_id

    @expense_id.setter
    def expense_id(self, value):
        self._expense_id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, value):
        self._category_id = value

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        self._date = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value