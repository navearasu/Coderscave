import csv
import os

class Person:
    def __init__(self, name):
        self.name = name
        self.owed_amount = 0
        self.paid_amount = 0

class Expense:
    def __init__(self, amount, paid_by, split_between):
        self.amount = amount
        self.paid_by = paid_by
        self.split_between = split_between

class Group:
    def __init__(self):
        self.persons = []
        self.expenses = []

    def add_person(self, person):
        self.persons.append(person)

    def add_expense(self, expense):
        self.expenses.append(expense)

    def split_bill(self, expense):
        total_split = len(expense.split_between)
        split_amount = (expense.amount - expense.paid_by.paid_amount) / total_split

        # Subtract split amount from the paid_by person
        expense.paid_by.owed_amount -= expense.amount - expense.paid_by.paid_amount
        expense.paid_by.paid_amount += expense.amount - expense.paid_by.paid_amount

        # Add split amount to each person in split_between
        for person in expense.split_between:
            person.owed_amount += split_amount
            person.paid_amount -= split_amount

    def track_owed_amounts(self):
        for person in self.persons:
            print(f"{person.name} owes: {person.owed_amount:.2f}")
            print(f"{person.name} has paid: {person.paid_amount:.2f}")

    def save_to_file(self, file_path):
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Owed Amount", "Paid Amount"])
            for person in self.persons:
                writer.writerow([person.name, person.owed_amount, person.paid_amount])

    def load_from_file(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")

        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                name, owed_amount, paid_amount = row
                person = Person(name.strip())
                person.owed_amount = float(owed_amount)
                person.paid_amount = float(paid_amount)
                self.persons.append(person)

    def display_splitted_bill(self):
        print("Splitted Bill:")
        for expense in self.expenses:
            self.split_bill(expense)  # Call split_bill only when displaying the bill
            print(f"{expense.paid_by.name} paid {expense.amount:.2f} for {', '.join(person.name for person in expense.split_between)}")


def main():
    group = Group()

    # Add persons
    person_names = input("Enter names of persons separated by comma: ").split(",")
    for name in person_names:
        group.add_person(Person(name.strip()))

    # Add expenses
    while True:
        amount = float(input("Enter expense amount: "))
        paid_by_name = input("Enter name of person who paid: ")
        paid_by = next((person for person in group.persons if person.name == paid_by_name), None)
        if paid_by is None:
            print("Person not found")
            continue
        split_between_names = input("Enter names of persons to split between (separated by comma): ").split(",")
        split_between = [person for person in group.persons if person.name in split_between_names]
        if len(split_between) == 0:
            print("No persons to split the bill with")
            continue
        group.add_expense(Expense(amount, paid_by, split_between))  # Call add_expense instead of split_bill
        if input("Do you want to add another expense? (y/n) ").lower() != 'y':
            break

    # Display splitted bill
    group.display_splitted_bill()

    # Save to file
    file_path = input("Enter file path to save to (default extension is .csv): ")
    if not file_path:
        file_path = "group_data.csv"
    group.save_to_file(file_path)

    # Load from file
    file_path = input("Enter file path to load from (default extension is .csv): ")
    if file_path:
        group.load_from_file(file_path)
        group.track_owed_amounts()
    else:
        print("Invalid file path. Data not loaded.")

if __name__ == "__main__":
    main()
