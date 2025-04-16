from abc import ABC, abstractmethod
from entity.expense import Expense
from entity.user import User

class IFinanceRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> int:
        pass

    @abstractmethod
    def login(self, user_id: int, password: str) -> bool:
        pass

    @abstractmethod
    def create_expense(self, expense: Expense) -> bool:
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> bool:
        pass

    @abstractmethod
    def delete_expense(self, expense_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_expenses(self, user_id: int) -> dict:
        pass

    @abstractmethod
    def get_monthly_expenses(self, user_id: int, month: int, year: int) -> dict:
        pass

    @abstractmethod
    def update_expense(self, user_id: int, expense: Expense) -> bool:
        pass