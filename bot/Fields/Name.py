from Fields.Field import Field


class Name(Field):
    def __init__(self, value):
        if not value.isalpha():
            raise ValueError("Name contains not only letters")
        super().__init__(value)
