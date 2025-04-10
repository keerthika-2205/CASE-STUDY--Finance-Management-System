from abc import ABC, abstractmethod
from entity.expense import Expense
from entity.user import User

class IFinanceRepository(ABC):

    def create_user(self, user: User) -> bool:
        pass


    def create_expense(self, expense: Expense) -> bool:
        pass


    def delete_user(self, user_id: int) -> bool:
        pass


    def delete_expense(self, expense_id: int) -> bool:
        pass


    def get_all_expenses(self, user_id: int) -> list:
        pass


    def update_expense(self, user_id: int, expense: Expense) -> bool:
        pass