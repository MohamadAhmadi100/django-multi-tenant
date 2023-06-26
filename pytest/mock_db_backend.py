from django.db.backends.base.creation import BaseDatabaseCreation
from django.db.backends.postgresql import base


class MockDatabaseCreation(BaseDatabaseCreation):
    def create_test_db(self, *args, **kwargs):
        pass


class DatabaseWrapper(base.DatabaseWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.creation = MockDatabaseCreation(self)
