import mysql.connector
from dao.ifinance_repository import IFinanceRepository
from entity.expense import Expense
from entity.user import User
from exception.myexceptions import UserNotFoundException, ExpenseNotFoundException
from util.db_conn_util import DBConnUtil


class FinanceRepositoryImpl(IFinanceRepository):
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def create_user(self, user: User) -> int:
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (user.username, user.password, user.email))
            self.connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()[0]
            return user_id
        finally:
            cursor.close()

    def login(self, user_id: int, password: str) -> bool:
        cursor = self.connection.cursor()
        try:
            query = "SELECT * FROM Users WHERE user_id = %s AND password = %s"
            cursor.execute(query, (user_id, password))
            if cursor.fetchone():
                return True
            raise UserNotFoundException("Invalid user ID or password")
        finally:
            cursor.close()

    def create_expense(self, expense: Expense) -> bool:
        cursor = self.connection.cursor()
        try:
            query = "INSERT INTO Expenses (user_id, amount, category_id, date, description) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query,
                           (expense.user_id, expense.amount, expense.category_id, expense.date, expense.description))
            self.connection.commit()
            return True
        finally:
            cursor.close()

    def delete_user(self, user_id: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
            if not cursor.fetchone():
                raise UserNotFoundException(f"User with ID {user_id} not found")
            cursor.execute("DELETE FROM Expenses WHERE user_id = %s", (user_id,))
            cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
            self.connection.commit()
            return True
        finally:
            cursor.close()

    def delete_expense(self, expense_id: int) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s", (expense_id,))
            if not cursor.fetchone():
                raise ExpenseNotFoundException(f"Expense with ID {expense_id} not found")
            cursor.execute("DELETE FROM Expenses WHERE expense_id = %s", (expense_id,))
            self.connection.commit()
            return True
        finally:
            cursor.close()

    def get_all_expenses(self, user_id: int) -> dict:
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT e.expense_id, e.user_id, e.amount, e.category_id, e.date, e.description, c.category_name
            FROM Expenses e
            JOIN ExpenseCategories c ON e.category_id = c.category_id
            WHERE e.user_id = %s
            ORDER BY c.category_name, e.date
            """
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()
            if not rows:
                raise UserNotFoundException(f"No expenses found for user ID {user_id}")

            expenses_by_category = {}
            for row in rows:
                expense = Expense(row[0], row[1], row[2], row[3], row[4], row[5])
                category_name = row[6]
                if category_name not in expenses_by_category:
                    expenses_by_category[category_name] = []
                expenses_by_category[category_name].append(expense)

            return expenses_by_category
        finally:
            cursor.close()

    def get_monthly_expenses(self, user_id: int, month: int, year: int) -> dict:
        cursor = self.connection.cursor()
        try:
            query = """
            SELECT e.expense_id, e.user_id, e.amount, e.category_id, e.date, e.description, c.category_name
            FROM Expenses e
            JOIN ExpenseCategories c ON e.category_id = c.category_id
            WHERE e.user_id = %s AND MONTH(e.date) = %s AND YEAR(e.date) = %s
            ORDER BY c.category_name, e.date
            """
            cursor.execute(query, (user_id, month, year))
            rows = cursor.fetchall()

            expenses_by_category = {}
            for row in rows:
                expense = Expense(row[0], row[1], row[2], row[3], row[4], row[5])
                category_name = row[6]
                if category_name not in expenses_by_category:
                    expenses_by_category[category_name] = []
                expenses_by_category[category_name].append(expense)

            return expenses_by_category
        finally:
            cursor.close()

    def update_expense(self, user_id: int, expense: Expense) -> bool:
        cursor = self.connection.cursor()
        try:
            cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s AND user_id = %s",
                           (expense.expense_id, user_id))
            if not cursor.fetchone():
                raise ExpenseNotFoundException(f"Expense with ID {expense.expense_id} not found for user {user_id}")
            query = "UPDATE Expenses SET amount = %s, category_id = %s, date = %s, description = %s WHERE expense_id = %s"
            cursor.execute(query,
                           (expense.amount, expense.category_id, expense.date, expense.description, expense.expense_id))
            self.connection.commit()
            return True
        finally:
            cursor.close()