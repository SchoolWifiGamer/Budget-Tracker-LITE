import json
import datetime
import os

#Created by Gao Le 
class BudgetTracker:
    def __init__(self, filename="budget_data.json"):
        self.filename = filename
        self.transactions = []
        self.load_data()

    def load_data(self):
        """Load transaction data from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    self.transactions = json.load(file)
            except:
                self.transactions = []

    def save_data(self):
        """Save transaction data to file"""
        with open(self.filename, 'w') as file:
            json.dump(self.transactions, file, indent=2)

    def add_transaction(self, amount, category, transaction_type, description=""):
        """Add a new transaction (income or expense)"""
        transaction = {
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'amount': amount,
            'category': category,
            'type': transaction_type,
            'description': description
        }
        self.transactions.append(transaction)
        self.save_data()
        print(f"{transaction_type.capitalize()} of ${amount:.2f} added successfully!")

    def get_balance(self):
        """Calculate current balance"""
        income = sum(t['amount']
                     for t in self.transactions if t['type'] == 'income')
        expenses = sum(t['amount']
                       for t in self.transactions if t['type'] == 'expense')
        return income - expenses

    def view_spending_by_category(self):
        """Show spending breakdown by category"""
        categories = {}
        for transaction in self.transactions:
            if transaction['type'] == 'expense':
                category = transaction['category']
                amount = transaction['amount']
                categories[category] = categories.get(category, 0) + amount

        print("\n--- Spending by Category ---")
        for category, amount in categories.items():
            print(f"{category}: ${amount:.2f}")

    def view_transactions(self):
        """Display all transactions"""
        print("\n--- Transaction History ---")
        for i, transaction in enumerate(self.transactions, 1):
            sign = "+" if transaction['type'] == 'income' else "-"
            print(f"{i}. {transaction['date']} | {sign}${transaction['amount']:.2f} | "
                  f"{transaction['category']} | {transaction['description']}")


def main():
    budget = BudgetTracker()

    while True:
        print("\n" + "="*50)
        print("PERSONAL BUDGET TRACKER")
        print("="*50)
        print(f"Current Balance: ${budget.get_balance():.2f}")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Transactions")
        print("4. View Spending by Category")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice == '1':
            try:
                amount = float(input("Enter income amount: $"))
                category = input("Enter category (e.g., Salary, Gift): ")
                description = input("Enter description: ")
                budget.add_transaction(amount, category, 'income', description)
            except ValueError:
                print("Please enter a valid amount!")

        elif choice == '2':
            try:
                amount = float(input("Enter expense amount: $"))
                category = input("Enter category (e.g., Food, Rent): ")
                description = input("Enter description: ")
                budget.add_transaction(
                    amount, category, 'expense', description)
            except ValueError:
                print("Please enter a valid amount!")

        elif choice == '3':
            budget.view_transactions()

        elif choice == '4':
            budget.view_spending_by_category()

        elif choice == '5':
            print("Thank you for using Budget Tracker!")
            break

        else:
            print("Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
