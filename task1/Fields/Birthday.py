from datetime import datetime

from Fields.Field import Field


class Birthday(Field):
    def __init__(self, value: str):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Birthday must be valid and in format DD.MM.YYYY")

        super().__init__(birthday_date)

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")
