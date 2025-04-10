from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User
from entity.expense import Expense
from exception.myexceptions import UserNotFoundException, ExpenseNotFoundException

class FinanceApp:
    def __init__(self):
        self.repo = FinanceRepositoryImpl()

    def menu(self):
        while True:
            print("\n=== Finance Management System ===")
            print("1. Add User")
            print("2. Add Expense")
            print("3. Delete User")
            print("4. Delete Expense")
            print("5. Update Expense")
            print("6. View All Expenses")
            print("7. Exit")
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    email = input("Enter email: ")
                    user = User(username=username, password=password, email=email)
                    if self.repo.create_user(user):
                        cursor = self.repo.connection.cursor()
                        cursor.execute("SELECT LAST_INSERT_ID()")
                        user_id = cursor.fetchone()[0]
                        print(f"User added successfully! User ID: {user_id}")

                elif choice == "2":
                    user_id = int(input("Enter user ID: "))
                    amount = float(input("Enter amount: "))
                    category_id = int(input("Enter category ID: "))
                    date = input("Enter date (YYYY-MM-DD): ")
                    description = input("Enter description: ")
                    expense = Expense(user_id=user_id, amount=amount, category_id=category_id, date=date, description=description)
                    if self.repo.create_expense(expense):
                        print("Expense added successfully!")

                elif choice == "3":
                    user_id = int(input("Enter user ID to delete: "))
                    if self.repo.delete_user(user_id):
                        print("User deleted successfully!")

                elif choice == "4":
                    expense_id = int(input("Enter expense ID to delete: "))
                    if self.repo.delete_expense(expense_id):
                        print("Expense deleted successfully!")

                elif choice == "5":
                    user_id = int(input("Enter user ID: "))
                    expense_id = int(input("Enter expense ID to update: "))
                    amount = float(input("Enter new amount: "))
                    category_id = int(input("Enter new category ID: "))
                    date = input("Enter new date (YYYY-MM-DD): ")
                    description = input("Enter new description: ")
                    expense = Expense(expense_id=expense_id, user_id=user_id, amount=amount, category_id=category_id, date=date, description=description)
                    if self.repo.update_expense(user_id, expense):
                        print("Expense updated successfully!")

                elif choice == "6":
                    user_id = int(input("Enter user ID to view expenses: "))
                    expenses = self.repo.get_all_expenses(user_id)
                    for exp in expenses:
                        print(f"ID: {exp.expense_id}, Amount: {exp.amount}, Date: {exp.date}, Description: {exp.description}")

                elif choice == "7":
                    print("Exiting...")
                    break

                else:
                    print("Invalid choice!")

            except UserNotFoundException as e:
                print(f"Error: {e}")
            except ExpenseNotFoundException as e:
                print(f"Error: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = FinanceApp()
    app.menu()