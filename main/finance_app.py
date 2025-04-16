from dao.finance_repository_impl import FinanceRepositoryImpl
from entity.user import User
from entity.expense import Expense
from exception.myexceptions import UserNotFoundException, ExpenseNotFoundException

class FinanceApp:
    def __init__(self):
        self.repo = FinanceRepositoryImpl()
        self.logged_in_user_id = None

    def login(self):
        print("\n=== Login ===")
        try:
            user_id = int(input("Enter User ID: "))
            password = input("Enter Password: ")
            if self.repo.login(user_id, password):
                self.logged_in_user_id = user_id
                print("Login successful!")
                return True
            return False
        except UserNotFoundException as e:
            print(f"Error: {e}")
            return False
        except ValueError:
            print("Error: Invalid input for User ID")
            return False

    def add_user(self):
        print("\n=== Add User ===")
        try:
            username = input("Enter username: ")
            password = input("Enter password: ")
            email = input("Enter email: ")
            user = User(username=username, password=password, email=email)
            user_id = self.repo.create_user(user)
            print(f"User added successfully! Your User ID is {user_id}")
        except Exception as e:
            print(f"Error: {e}")

    def menu(self):
        while True:
            if self.logged_in_user_id is None:
                print("\n=== Finance Management System ===")
                print("1. Login")
                print("2. Add User")
                print("3. Exit")
                choice = input("Enter your choice: ")

                try:
                    if choice == "1":
                        if self.login():
                            self.show_expense_menu()
                    elif choice == "2":
                        self.add_user()
                    elif choice == "3":
                        print("Exiting...")
                        break
                    else:
                        print("Invalid choice!")
                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                self.show_expense_menu()

    def show_expense_menu(self):
        while True:
            print("\n=== Expense Management Menu ===")
            print("1. Add Expense")
            print("2. Update Expense")
            print("3. Delete Expense")
            print("4. View All Expenses")
            print("5. View Monthly Report")
            print("6. Logout")
            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    amount = float(input("Enter amount: "))
                    category_id = int(input("Enter category ID (1=Food, 2=Transportation, 3=Utilities, 4=Entertainment, 5=Healthcare): "))
                    date = input("Enter date (YYYY-MM-DD): ")
                    description = input("Enter description: ")
                    expense = Expense(user_id=self.logged_in_user_id, amount=amount, category_id=category_id, date=date, description=description)
                    if self.repo.create_expense(expense):
                        print("Expense added successfully!")

                elif choice == "2":
                    expense_id = int(input("Enter expense ID to update: "))
                    amount = float(input("Enter new amount: "))
                    category_id = int(input("Enter new category ID (1=Food, 2=Transportation, 3=Utilities, 4=Entertainment, 5=Healthcare): "))
                    date = input("Enter new date (YYYY-MM-DD): ")
                    description = input("Enter new description: ")
                    expense = Expense(expense_id=expense_id, user_id=self.logged_in_user_id, amount=amount, category_id=category_id, date=date, description=description)
                    if self.repo.update_expense(self.logged_in_user_id, expense):
                        print("Expense updated successfully!")

                elif choice == "3":
                    expense_id = int(input("Enter expense ID to delete: "))
                    if self.repo.delete_expense(expense_id):
                        print("Expense deleted successfully!")

                elif choice == "4":
                    expenses_by_category = self.repo.get_all_expenses(self.logged_in_user_id)
                    print("\n=== Expense Report (Clustered by Category) ===")
                    if not expenses_by_category:
                        print("No expenses found.")
                    else:
                        for category_name, expenses in expenses_by_category.items():
                            print(f"\nCategory: {category_name}")
                            print("-------------------")
                            for exp in expenses:
                                print(f"ID: {exp.expense_id}, Amount: {exp.amount}, Date: {exp.date}, Description: {exp.description}")

                elif choice == "5":
                    month = int(input("Enter month (1-12): "))
                    year = int(input("Enter year (e.g., 2025): "))
                    expenses_by_category = self.repo.get_monthly_expenses(self.logged_in_user_id, month, year)
                    print(f"\n=== Monthly Expense Report for {month}/{year} (Clustered by Category) ===")
                    if not expenses_by_category:
                        print("No expenses found for this month.")
                    else:
                        for category_name, expenses in expenses_by_category.items():
                            print(f"\nCategory: {category_name}")
                            print("-------------------")
                            for exp in expenses:
                                print(f"ID: {exp.expense_id}, Amount: {exp.amount}, Date: {exp.date}, Description: {exp.description}")

                elif choice == "6":
                    print("Logging out...")
                    self.logged_in_user_id = None
                    break

                else:
                    print("Invalid choice!")

            except UserNotFoundException as e:
                print(f"Error: {e}")
            except ExpenseNotFoundException as e:
                print(f"Error: {e}")
            except ValueError:
                print("Error: Invalid input")
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    app = FinanceApp()
    app.menu()