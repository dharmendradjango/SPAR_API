from django.db import models

class BitBooleanField(models.Field):
    def db_type(self, connection):
        return 'bit(1)'

    def from_db_value(self, value, expression, connection, context=None):
        if value is None:
            return None
        return value == b'\x01'

    def to_python(self, value):
        if value is None:
            return None
        if isinstance(value, bool):
            return value
        return value == b'\x01'

    def get_prep_value(self, value):
        if value is None:
            return None
        return b'\x01' if value else b'\x00'