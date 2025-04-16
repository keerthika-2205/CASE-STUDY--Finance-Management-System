class ExpenseCategory:
    def __init__(self, category_id=None, category_name=None):
        self._category_id = category_id
        self._category_name = category_name

    # Getters and Setters
    @property
    def category_id(self):
        return self._category_id

    @category_id.setter
    def category_id(self, value):
        self._category_id = value

    @property
    def category_name(self):
        return self._category_name

    @category_name.setter
    def category_name(self, value):
        self._category_name = value