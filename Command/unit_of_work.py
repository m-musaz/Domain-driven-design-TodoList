from abc import ABC, abstractmethod
import psycopg2
import os
from ..repository.repo import (
    UserAbstractRepository,
    FakeUserRepository,
    UserRepository,
    TodoListAbstractRepository,
    FakeTodoListRepository,
    TodoListRepository,
    LogsAbstractRepository,
    LogsRepository,
    FakeLogListRepository
)


class AbstractUnitOfWork(ABC):

    Users: UserAbstractRepository
    TodoLists: TodoListAbstractRepository
    LogLists: LogsAbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return self

    def __exit__(self, *args):
        self.commit()
        self.rollback()

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass


class FakeUnitOfWork(AbstractUnitOfWork):
    def __init__(self):
        super().__init__()
        self.Users = FakeUserRepository()
        self.TodoLists = FakeTodoListRepository()
        self.LogLists = FakeLogListRepository()

    def commit(self):
        pass

    def rollback(self):
        pass


class UnitOfWork(AbstractUnitOfWork):
    def __enter__(self):
        # self.Users = FakeUserRepository()
        # self.TodoLists = FakeTodoListRepository()
        # self.LogLists = FakeLogListRepository()
        # return self
        self.connection = psycopg2.connect(
            "postgresql://postgres:25100107@localhost:5432/postgres")

        self.cursor = self.connection.cursor()

        self.Users = UserRepository(self.connection)
        self.TodoLists = TodoListRepository(self.connection)
        self.LogLists = LogsRepository(self.connection)

        return self

    def __exit__(self, *args):
        super().__exit__(*args)

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()
