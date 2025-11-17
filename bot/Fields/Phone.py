from Fields.Field import Field


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone must contain 10 digits")
        super().__init__(value)
