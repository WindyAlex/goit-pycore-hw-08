from collections import UserDict
from datetime import date, timedelta

from Fields.Name import Name
from Fields.Phone import Phone
from Fields.Birthday import Birthday


class Record:
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone: str, new_phone: str):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                break

    def find_phone(self, phone: str):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday_str: str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = str(self.birthday)
        result = f"Contact name: {self.name.value}, phones: [{phones_str}]"
        result += f", birthday: [{birthday_str}]"
        return result


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        return self.data.get(name)

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7) -> list[dict]:
        today = date.today()
        end_date = today + timedelta(days=days)

        result = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            bday = record.birthday.value

            # Find nearest birthday (this year)
            try:
                birthday_this_year = date(today.year, bday.month, bday.day)
            except ValueError:
                # 29 Feb to 28 Feb
                birthday_this_year = date(today.year, bday.month, bday.day - 1)

            if birthday_this_year < today:
                try:
                    next_birthday = date(today.year + 1, bday.month, bday.day)
                except ValueError:
                    # 29 Feb to 28 Feb
                    next_birthday = date(
                        today.year + 1, bday.month, bday.day - 1)
            else:
                next_birthday = birthday_this_year

            if today <= next_birthday <= end_date:
                congrats_date = next_birthday

                if congrats_date.weekday() == 5:  # Saturday
                    congrats_date += timedelta(days=2)
                elif congrats_date.weekday() == 6:  # Sunday
                    congrats_date += timedelta(days=1)

                result.append({
                    "name": record.name.value,
                    "congratulation_date": congrats_date,
                })

        result.sort(key=lambda x: x["congratulation_date"])
        return result
