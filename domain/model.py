from dataclasses import dataclass, field
from typing import List, Dict
from uuid import uuid4


@dataclass
class Task:
    id: str
    body: str
    status: bool
    order: int


@dataclass
class TodoList:
    id: str
    tasks: Dict[int, Task] = field(default_factory=dict)

    def add_task(self, task: Task):
        self.tasks[task.order] = task

    def mark_complete(self, order: str):
        self.tasks[order].status = True

    def edit_task(self, order, edit):
        self.tasks[order].body = edit

    def delete_task(self, order):
        self.tasks.pop(order)
        temp = {}
        for i in self.tasks.values():
            if (i.order > order):
                i.order -= 1
            temp[i.order] = i
        self.tasks = temp
        print(self.tasks)

    def change_order(self, old: int, new: int):

        temp_task = self.tasks.pop(old)
        try:
            self.tasks[old] = self.tasks[new]
            self.tasks[new] = temp_task

            self.tasks[old].order = old
            self.tasks[new].order = new
        except:
            print(self.tasks)
            raise Exception("Task Doesnt exist")


@dataclass
class Log:
    id: str
    body: str
    order: int


@dataclass
class LogList:
    id: str
    logs: Dict[int, Log] = field(default_factory=list)

    def add_log(self, log: str, body: str, edited_body: str = ""):
        new_log = log+" Task: "+body
        if (edited_body != ""):
            new_log += " to "+edited_body

        self.logs[len(self.logs)] = Log(
            id=str(uuid4()), body=new_log, order=len(self.logs))


@dataclass
class User:
    id: str
    name: str
    email: str
    password: str
    todolist_id: str
    Loglist_id: str
