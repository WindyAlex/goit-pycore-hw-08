import pickle
from pathlib import Path

from AddressBook import AddressBook, Record


FILENAME = "addressbook.pkl"


def save_data(book: AddressBook, filename: str = FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename: str = FILENAME) -> AddressBook:
    path = Path(filename)
    if not path.exists():
        return AddressBook()
    with open(filename, "rb") as f:
        return pickle.load(f)


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Enter the argument for the command"
        except KeyboardInterrupt:
            return ""
    return inner


@input_error
def parse_input(user_input: str):
    cmd, *args = user_input.split()
    if not cmd:
        return "", []
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book):
    if len(args) < 2:
        raise ValueError("Use input standart: add [name] [phone]")
    name, phone = args[0], args[1]

    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added"
        if phone:
            record.add_phone(phone)
    else:
        if phone:
            record.add_phone(phone)
            message = "Contact updated"

    return message


@input_error
def change_contact(args, book):
    if len(args) < 3:
        raise ValueError("Use input standart: "
                         "change [name] [oldphone] [newphone]")
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = book.find(name)

    if record is None:
        raise KeyError(name)

    record.edit_phone(old_phone, new_phone)
    return "Contact updated"


@input_error
def show_phone(args, book):
    if not args:
        raise ValueError("Use format: phone [name]")

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError(name)

    if not record.phones:
        return f"{name} has no phones"

    phones_str = ", ".join(p.value for p in record.phones)
    return f"{name}: {phones_str}"


@input_error
def show_all(book):
    if not book.data:
        return "No contacts yet"

    lines = [str(record) for record in book.values()]
    return "\n".join(lines)


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError("Use format: add-birthday [name] [DD.MM.YYYY]")

    name, birthday_str = args[0], args[1]
    record = book.find(name)

    if record is None:
        record = Record(name)
        book.add_record(record)

    record.add_birthday(birthday_str)
    return "Birthday added"


@input_error
def show_birthday(args, book: AddressBook):
    if not args:
        raise ValueError("Use format: show-birthday [name]")

    name = args[0]
    record = book.find(name)

    if record is None:
        raise KeyError(name)

    if record.birthday is None:
        return f"Birthday is not set for contact [{name}]"

    return f"{name}: {record.birthday}"


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays(7)

    if not upcoming:
        return "No birthdays in the next week"

    lines = ["Upcoming birthdays:"]

    for item in upcoming:
        date_str = item["congratulation_date"].strftime("%d.%m.%Y")
        name = item["name"]
        lines.append(f"{name} - {date_str}")

    return "\n".join(lines)


@input_error
def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input:
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


main()
