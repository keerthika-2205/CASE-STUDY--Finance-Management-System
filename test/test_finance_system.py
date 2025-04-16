import unittest
from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User
from entity.expense import Expense
from exception.myexceptions import UserNotFoundException, ExpenseNotFoundException
from util.db_conn_util import DBConnUtil


class TestFinanceSystem(unittest.TestCase):
    def setUp(self):
        self.repo = FinanceRepositoryImpl()
        # Clear database tables to ensure clean state
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Expenses")
        cursor.execute("DELETE FROM Users")
        # Ensure categories exist without deleting existing ones
        cursor.execute(
            "INSERT IGNORE INTO ExpenseCategories (category_id, category_name) VALUES (1, 'Food'), (2, 'Transportation'), (3, 'Utilities'),(4, 'Entertainment'), (5, 'Healthcare')")
        conn.commit()
        cursor.close()

    def tearDown(self):
        # Clean up after each test and reset AUTO_INCREMENT
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Expenses")
        cursor.execute("ALTER TABLE Expenses AUTO_INCREMENT = 1")
        cursor.execute("DELETE FROM Users")
        cursor.execute("ALTER TABLE Users AUTO_INCREMENT = 1")
        conn.commit()
        cursor.close()

    def get_user_id(self, username):
        conn = DBConnUtil.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id FROM Users WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result else None

    def test_create_user(self):
        user = User(username="testuser", password="pass123", email="test@example.com")
        user_id = self.repo.create_user(user)
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        print(f"Created User: username=testuser, user_id={user_id}")

    def test_login_success(self):
        user = User(username="testuser2", password="pass123", email="test2@example.com")
        user_id = self.repo.create_user(user)
        self.assertTrue(self.repo.login(user_id, "pass123"))
        print(f"Logged in User: username=testuser2, user_id={user_id}")

    def test_login_failure(self):
        with self.assertRaises(UserNotFoundException):
            self.repo.login(999, "wrongpass")

    def test_create_expense(self):
        user = User(username="testuser3", password="pass123", email="test3@example.com")
        user_id = self.repo.create_user(user)
        expense = Expense(user_id=user_id, amount=100.50, category_id=1, date="2025-04-05", description="Test expense")
        self.assertTrue(self.repo.create_expense(expense))
        print(
            f"Created Expense: user_id={user_id}, amount=100.50, category_id=1 (Food), date=2025-04-05, description=Test expense")

    def test_get_all_expenses(self):
        user = User(username="testuser4", password="pass123", email="test4@example.com")
        user_id = self.repo.create_user(user)
        expense1 = Expense(user_id=user_id, amount=50.00, category_id=1, date="2025-04-05", description="Lunch")
        expense2 = Expense(user_id=user_id, amount=20.00, category_id=2, date="2025-04-06", description="Bus fare")
        self.repo.create_expense(expense1)
        self.repo.create_expense(expense2)

        print(f"Created User: username=testuser4, user_id={user_id}")
        print(f"Created Expenses:")
        print(
            f"  - Amount: {expense1.amount}, Category: Food, Date: {expense1.date}, Description: {expense1.description}")
        print(
            f"  - Amount: {expense2.amount}, Category: Transportation, Date: {expense2.date}, Description: {expense2.description}")

        expenses_by_category = self.repo.get_all_expenses(user_id)
        print("All Expenses:")
        for category, expenses in expenses_by_category.items():
            print(f"Category: {category}")
            for exp in expenses:
                print(
                    f"  - ID: {exp.expense_id}, Amount: {exp.amount}, Date: {exp.date}, Description: {exp.description}")

        self.assertIsInstance(expenses_by_category, dict)
        self.assertEqual(len(expenses_by_category), 2)
        self.assertIn("Food", expenses_by_category)
        self.assertIn("Transportation", expenses_by_category)
        self.assertEqual(len(expenses_by_category["Food"]), 1)
        self.assertEqual(len(expenses_by_category["Transportation"]), 1)
        self.assertEqual(len(expenses_by_category.get("Utilities", [])), 0)

    def test_get_monthly_expenses(self):
        user = User(username="testuser5", password="pass123", email="test5@example.com")
        user_id = self.repo.create_user(user)
        expense1 = Expense(user_id=user_id, amount=50.00, category_id=1, date="2025-04-05", description="Lunch")
        expense2 = Expense(user_id=user_id, amount=20.00, category_id=2, date="2025-04-06", description="Bus fare")
        expense3 = Expense(user_id=user_id, amount=30.00, category_id=1, date="2025-05-01", description="Dinner")
        self.repo.create_expense(expense1)
        self.repo.create_expense(expense2)
        self.repo.create_expense(expense3)

        print(f"Created User: username=testuser5, user_id={user_id}")
        print(f"Created Expenses:")
        print(
            f"  - Amount: {expense1.amount}, Category: Food, Date: {expense1.date}, Description: {expense1.description}")
        print(
            f"  - Amount: {expense2.amount}, Category: Transportation, Date: {expense2.date}, Description: {expense2.description}")
        print(
            f"  - Amount: {expense3.amount}, Category: Food, Date: {expense3.date}, Description: {expense3.description}")

        expenses_by_category = self.repo.get_monthly_expenses(user_id, 4, 2025)
        print("Monthly Expenses for April 2025:")
        for category, expenses in expenses_by_category.items():
            print(f"Category: {category}")
            for exp in expenses:
                print(
                    f"  - ID: {exp.expense_id}, Amount: {exp.amount}, Date: {exp.date}, Description: {exp.description}")

        self.assertIsInstance(expenses_by_category, dict)
        self.assertEqual(len(expenses_by_category), 2)
        self.assertEqual(len(expenses_by_category.get("Food", [])), 1)
        self.assertEqual(len(expenses_by_category.get("Transportation", [])), 1)
        self.assertEqual(len(expenses_by_category.get("Utilities", [])), 0)

        expenses_by_category = self.repo.get_monthly_expenses(user_id, 6, 2025)
        self.assertEqual(len(expenses_by_category), 0)

    def test_user_not_found_exception(self):
        with self.assertRaises(UserNotFoundException):
            self.repo.get_all_expenses(999)

    def test_expense_not_found_exception(self):
        with self.assertRaises(ExpenseNotFoundException):
            self.repo.delete_expense(999)


if __name__ == "__main__":
    unittest.main()