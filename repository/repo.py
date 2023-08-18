from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import uuid4
from typing import List, Dict
from ..domain.model import User, Task, TodoList, LogList, Log


class UserAbstractRepository(ABC):
    @abstractmethod
    def add(self, User: User):
        pass

    @abstractmethod
    def get(self, name: str) -> User:
        pass

    @abstractmethod
    def save(self, User: User):
        pass


class FakeUserRepository(UserAbstractRepository):
    def __init__(self):
        self.Users: dict[str, User] = {}

    def add(self, User: User):
        self.Users[User.id] = User

    def get(self, User_id: str) -> User:
        try:
            return self.Users[User_id]
        except:
            raise Exception("No such User exists!")

    def save(self, User: User):
        self.Users[User.id] = User


class UserRepository(UserAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, User: User):
        sql = """
            insert into Users (id, name, email,password,todolist_id,loglist_id)
            values (%s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(
            sql,
            [
                User.id,
                User.name,
                User.email,
                User.password,
                User.todolist_id,
                User.Loglist_id
            ],
        )

    def get(self, name: str) -> User:
        sql = """
            select id, name, email,password,todolist_id,loglist_id
            from Users
            where name = %s
        """
        self.cursor.execute(sql, [name])
        row = self.cursor.fetchone()

        if row is None:
            raise Exception("No such User exists!")
        else:
            return User(
                id=row[0],
                name=row[1],
                email=row[2],
                password=row[3],
                todolist_id=row[4],
                Loglist_id=row[5]
            )

    def save(self, User: User):
        sql = """
            update Users 
            set name=%s, email=%s, password=%s , todolist_id=%s, loglist_id=%s
            where id=%s
        """
        self.cursor.execute(
            sql,
            [
                User.name,
                User.email,
                User.password,
                User.todolist_id,
                User.id,
                User.Loglist_id
            ],
        )


class LogsAbstractRepository(ABC):
    @abstractmethod
    def add(self, LogList: LogList):
        pass

    @abstractmethod
    def get(self, list_id: str) -> LogList:
        pass

    @abstractmethod
    def remove(self, list_id: str):
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass

    @abstractmethod
    def save(self, LogList: LogList):
        pass


class FakeLogListRepository(LogsAbstractRepository):
    def __init__(self):
        self.Lists: Dict[str, LogList] = {}

    def add(self, LogList: LogList):
        self.Lists[LogList.id] = LogList

    def get(self, list_id: str) -> LogList:
        try:
            return self.Lists[list_id]
        except:
            raise Exception("No such LogList exists!")

    def get_length(self) -> int:
        try:
            return len(self.Lists)
        except:
            return 0

    def remove(self, list_id: str):
        try:
            self.Lists.pop(list_id)
        except:
            raise Exception("No such LogList exists!")

    def save(self, LogList: LogList):
        self.Lists[LogList.id] = LogList


class LogsRepository(LogsAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, LogList: LogList):
        sql2 = """
            insert into LogList (id)
            values (%s)
            """
        self.cursor.execute(
            sql2,
            [
                LogList.id
            ],
        )

        for log in LogList.logs.values():
            sql = """
            insert into Log (id,body,order_num)
            values (%s, %s,%s)
            """

            self.cursor.execute(
                sql,
                [
                    log.id,
                    log.body,
                    log.order,
                ],
            )
            sql = """
            insert into LogListLogs (List_id,Log_id)
            values (%s, %s)
            """
            self.cursor.execute(
                sql,
                [
                    LogList.id,
                    log.id,
                ],
            )

    def get_length(self) -> int:
        sql = """
            select id
            from LogList
        """
        self.cursor.execute(sql)
        row = self.cursor.fetchall()

        return len(row)

    def remove(self, list_id: str):
        sql = """DELETE FROM LogList WHERE id= %s """
        self.cursor.execute(sql, [list_id])

    def get(self, list_id: str) -> TodoList:
        logs = {}

        sql = """
            select Log_id
            from LogListLogs
            where List_id = %s
        """
        self.cursor.execute(sql, [list_id])
        row = self.cursor.fetchall()

        if row is None:
            raise Exception("No such Logs exist!")
        else:
            for r in row:
                sql = """
                    select id,body,order_num
                    from Logs
                    where id = %s
                """
                self.cursor.execute(sql, [r[0]])
                res = self.cursor.fetchone()
                log = Log(id=res[0], body=res[1], order=res[2])
                logs[log.order] = log

            return LogList(id=list_id, logs=dict(sorted(logs.items())))

    def save(self, LogList: LogList):

        log_ids = []
        for log in LogList.logs.values():
            log_ids.append(log.id)
            sql = """
            insert into Logs (id,body,order_num)
            values (%s, %s,%s) ON CONFLICT (id) DO UPDATE
            SET body = EXCLUDED.body,
            order_num = EXCLUDED.order_num
            """
            self.cursor.execute(
                sql,
                [
                    log.id,
                    log.body,
                    log.order
                ],
            )
            sql = """
            insert into LogListLogs (List_id,Log_id)
            values (%s, %s) ON CONFLICT (List_id,Log_id) DO UPDATE
            SET List_id = EXCLUDED.List_id,
            Log_id = EXCLUDED.Log_id
            """
            self.cursor.execute(
                sql,
                [
                    LogList.id,
                    log.id,
                ],
            )

        sql = """
            select Log_id
            from LogListLogs
            where List_id = %s
            """
        self.cursor.execute(sql, [LogList.id])
        row = self.cursor.fetchall()
        for r in row:
            if r[0] not in log_ids:
                sql2 = """DELETE FROM LogListLogs WHERE Log_id= %s """
                self.cursor.execute(sql2, [r[0]])
                sql2 = """DELETE FROM Logs WHERE id= %s """
                self.cursor.execute(sql2, [r[0]])


class TodoListAbstractRepository(ABC):
    @abstractmethod
    def add(self, TodoList: TodoList):
        pass

    @abstractmethod
    def get(self, list_id: str) -> TodoList:
        pass

    @abstractmethod
    def remove(self, list_id: str):
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass

    @abstractmethod
    def save(self, TodoList: TodoList):
        pass


class FakeTodoListRepository(TodoListAbstractRepository):
    def __init__(self):
        self.Lists: Dict[str, TodoList] = {}

    def add(self, TodoList: TodoList):
        self.Lists[TodoList.id] = TodoList

    def get(self, list_id: str) -> TodoList:
        try:
            return self.Lists[list_id]
        except:
            raise Exception("No such TodoList exists!")

    def get_length(self) -> int:
        try:
            return len(self.Lists)
        except:
            return 0

    def remove(self, list_id: str):
        try:
            self.Lists.pop(list_id)
        except:
            raise Exception("No such TodoList exists!")

    def save(self, TodoList: TodoList):
        self.Lists[TodoList.id] = TodoList


class TodoListRepository(TodoListAbstractRepository):
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def add(self, TodoList: TodoList):
        sql2 = """
            insert into TodoList (id)
            values (%s)
            """
        self.cursor.execute(
            sql2,
            [
                TodoList.id
            ],
        )

        for t in TodoList.tasks.values():
            sql = """
            insert into Task (id,body,status,order_num)
            values (%s, %s,%s, %s, %s)
            """
            self.cursor.execute(
                sql,
                [
                    t.id,
                    t.body,
                    t.status,
                    t.order
                ],
            )
            sql = """
            insert into TodoListTask (todolist_id,task_id)
            values (%s, %s)
            """
            self.cursor.execute(
                sql,
                [
                    TodoList.id,
                    t.id,
                ],
            )

    def get_length(self) -> int:
        sql = """
            select id
            from TodoList
        """
        self.cursor.execute(sql)
        row = self.cursor.fetchall()

        return len(row)

    def remove(self, list_id: str):
        sql = """DELETE FROM Todolist WHERE id= %s """
        self.cursor.execute(sql, [list_id])

    def get(self, list_id: str) -> TodoList:
        tasks = {}

        sql = """
            select task_id
            from TodoListTask
            where todolist_id = %s
        """
        self.cursor.execute(sql, [list_id])
        row = self.cursor.fetchall()

        if row is None:
            raise Exception("No such TodoList exists!")
        else:
            for r in row:
                sql = """
                    select id,body,status,order_num
                    from Task
                    where id = %s
                """
                self.cursor.execute(sql, [r[0]])
                task = self.cursor.fetchone()
                task = Task(id=task[0], body=task[1],
                            status=task[2], order=task[3])
                tasks[task.order] = task

            return TodoList(id=list_id, tasks=dict(sorted(tasks.items())))

    def save(self, TodoList: TodoList):

        task_ids = []
        for t in TodoList.tasks.values():
            task_ids.append(t.id)
            sql = """
            insert into Task (id,body,status,order_num)
            values (%s, %s,%s, %s) ON CONFLICT (id) DO UPDATE
            SET body = EXCLUDED.body,
            status = EXCLUDED.status,
            order_num = EXCLUDED.order_num
            """
            self.cursor.execute(
                sql,
                [
                    t.id,
                    t.body,
                    t.status,
                    t.order
                ],
            )
            sql = """
            insert into TodoListTask (todolist_id,task_id)
            values (%s, %s) ON CONFLICT (todolist_id,task_id) DO UPDATE
            SET todolist_id = EXCLUDED.todolist_id,
            task_id = EXCLUDED.task_id
            """
            self.cursor.execute(
                sql,
                [
                    TodoList.id,
                    t.id,
                ],
            )

        sql = """
            select task_id
            from TodoListTask
            where todolist_id = %s
            """
        self.cursor.execute(sql, [TodoList.id])
        row = self.cursor.fetchall()
        for r in row:
            if r[0] not in task_ids:
                sql2 = """DELETE FROM TodoListTask WHERE task_id= %s """
                self.cursor.execute(sql2, [r[0]])
                sql2 = """DELETE FROM Task WHERE id= %s """
                self.cursor.execute(sql2, [r[0]])
