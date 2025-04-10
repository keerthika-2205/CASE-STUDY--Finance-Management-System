import unittest
from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User
from entity.expense import Expense
from exception.myexceptions import UserNotFoundException, ExpenseNotFoundException

class TestFinanceSystem(unittest.TestCase):
    def setUp(self):
        self.repo = FinanceRepositoryImpl()

    def test_create_user(self):
        user = User(username="testuser3", password="pass123", email="test@example.com")
        self.assertTrue(self.repo.create_user(user))

    def test_create_expense(self):
        user = User(username="testuser4", password="pass123", email="test2@example.com")
        self.repo.create_user(user)
        expense = Expense(user_id=1, amount=100.50, category_id=1, date="2025-04-05", description="Test expense")
        self.assertTrue(self.repo.create_expense(expense))

    def test_get_all_expenses(self):
        expenses = self.repo.get_all_expenses(1)
        self.assertGreater(len(expenses), 0)

    def test_user_not_found_exception(self):
        with self.assertRaises(UserNotFoundException):
            self.repo.get_all_expenses(999)

    def test_expense_not_found_exception(self):
        with self.assertRaises(ExpenseNotFoundException):
            self.repo.delete_expense(999)

if __name__ == "__main__":
    unittest.main()