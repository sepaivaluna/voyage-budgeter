def add_expenses(expenditures):
    total = 0
    for expenditure in expenditures:
        total += expenditure
    return total

def get_remaining_balance(funds, expenses):
    return funds - expenses
