import mysql.connector
from dao.ifinance_repository import IFinanceRepository
from entity.expense import Expense
from entity.user import User
from exception.myexceptions import UserNotFoundException, ExpenseNotFoundException
from util.db_conn_util import DBConnUtil

class FinanceRepositoryImpl(IFinanceRepository):
    def __init__(self):
        self.connection = DBConnUtil.get_connection()

    def create_user(self, user: User) -> bool:
        cursor = self.connection.cursor()
        query = "INSERT INTO Users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.username, user.password, user.email))
        self.connection.commit()
        return True

    def create_expense(self, expense: Expense) -> bool:
        cursor = self.connection.cursor()
        query = "INSERT INTO Expenses (user_id, amount, category_id, date, description) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (expense.user_id, expense.amount, expense.category_id, expense.date, expense.description))
        self.connection.commit()
        return True

    def delete_user(self, user_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            raise UserNotFoundException(f"User with ID {user_id} not found")
        cursor.execute("DELETE FROM Expenses WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM Users WHERE user_id = %s", (user_id,))
        self.connection.commit()
        return True

    def delete_expense(self, expense_id: int) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s", (expense_id,))
        if not cursor.fetchone():
            raise ExpenseNotFoundException(f"Expense with ID {expense_id} not found")
        cursor.execute("DELETE FROM Expenses WHERE expense_id = %s", (expense_id,))
        self.connection.commit()
        return True

    def get_all_expenses(self, user_id: int) -> list:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Expenses WHERE user_id = %s", (user_id,))
        rows = cursor.fetchall()
        if not rows:
            raise UserNotFoundException(f"No expenses found for user ID {user_id}")
        expenses = []
        for row in rows:
            expense = Expense(row[0], row[1], row[2], row[3], row[4], row[5])
            expenses.append(expense)
        return expenses

    def update_expense(self, user_id: int, expense: Expense) -> bool:
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Expenses WHERE expense_id = %s AND user_id = %s", (expense.expense_id, user_id))
        if not cursor.fetchone():
            raise ExpenseNotFoundException(f"Expense with ID {expense.expense_id} not found for user {user_id}")
        query = "UPDATE Expenses SET amount = %s, category_id = %s, date = %s, description = %s WHERE expense_id = %s"
        cursor.execute(query, (expense.amount, expense.category_id, expense.date, expense.description, expense.expense_id))
        self.connection.commit()
        return True