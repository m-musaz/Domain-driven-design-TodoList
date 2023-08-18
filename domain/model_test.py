import pytest
from uuid import uuid4
from .model import User, TodoList, Task, LogList
from typing import List, Dict
from dataclasses import field

"""
Use Cases / Requirements:
- Multiple users
- Users can access their own todo lists
- One user has only one todo list
- Users can add tasks to their todo list
- Users can mark tasks as completed
- Users can edit a task
- Users can delete a task
- Users can reorder their tasks
- Users can view the history of their todo list, (create / edit/ delete operations on the todolist)
"""


def create_User(list_id: str, logs_id: str):
    return User(
        id=str(uuid4),
        name="Musa",
        email="mz@hotmail.com",
        password="123456",
        todolist_id=list_id,
        Loglist_id=logs_id,
    )


def create_task(Body: str, Order: int):
    return Task(id=str(uuid4), body=Body, status=False, order=Order)


def create_lists():
    todolists = {}
    return todolists


def test_create_user():
    test_user = create_User(list_id=str(uuid4), logs_id=str(uuid4))

    assert test_user.name == "Musa"
    assert test_user.email == "mz@hotmail.com"
    assert test_user.password == "123456"


def test_add_task():
    todolists = {}
    loglists = {}
    test_user = create_User(list_id=str(uuid4), logs_id=str(uuid4))
    new_list = TodoList(test_user.todolist_id, {})
    new_logs = LogList(id=test_user.Loglist_id, logs={})
    todolists[new_list.id] = new_list
    loglists[new_logs.id] = new_logs

    test_task = create_task("Task1", len(new_list.tasks))
    todolists[new_list.id].add_task(test_task)

    loglists[new_logs.id].add_log("CREATE", test_task.body)

    assert todolists[new_list.id].tasks[0].body == "Task1"
    assert loglists[new_logs.id].logs[0].body == "CREATE Task: Task1"


def test_delete_task():
    todolists = {}
    loglists = {}
    test_user = create_User(list_id=str(uuid4), logs_id=str(uuid4))
    new_list = TodoList(test_user.todolist_id, {})
    new_logs = LogList(id=test_user.Loglist_id, logs={})
    todolists[new_list.id] = new_list
    loglists[new_logs.id] = new_logs

    test_task = create_task("Task1", len(new_list.tasks))
    todolists[new_list.id].add_task(test_task)
    loglists[new_logs.id].add_log("CREATE", test_task.body)

    todolists[new_list.id].delete_task(0)

    loglists[new_logs.id].add_log("DELETE", test_task.body)

    assert not len(todolists[new_list.id].tasks)
    assert loglists[new_logs.id].logs[0].body == "CREATE Task: Task1"
    assert loglists[new_logs.id].logs[1].body == "DELETE Task: Task1"


def test_edit_task():
    todolists = {}
    loglists = {}
    test_user = create_User(list_id=str(uuid4), logs_id=str(uuid4))
    new_list = TodoList(test_user.todolist_id, {})
    new_logs = LogList(id=test_user.Loglist_id, logs={})
    todolists[new_list.id] = new_list
    loglists[new_logs.id] = new_logs

    test_task = create_task("Task1", len(new_list.tasks))
    todolists[new_list.id].add_task(test_task)
    loglists[new_logs.id].add_log("CREATE", test_task.body)

    old_body = test_task.body

    todolists[new_list.id].edit_task(0, "Task2")
    loglists[new_logs.id].add_log("EDIT", old_body, test_task.body)

    assert todolists[new_list.id].tasks[0].body == "Task2"
    assert loglists[new_logs.id].logs[0].body == "CREATE Task: Task1"
    assert loglists[new_logs.id].logs[1].body == "EDIT Task: Task1 to Task2"


def test_marked_complete():
    todolists = {}
    loglists = {}
    test_user = create_User(list_id=str(uuid4), logs_id=str(uuid4))
    new_list = TodoList(test_user.todolist_id, {})
    new_logs = LogList(id=test_user.Loglist_id, logs={})
    todolists[new_list.id] = new_list
    loglists[new_logs.id] = new_logs

    test_task = create_task("Task1", len(new_list.tasks))
    todolists[new_list.id].add_task(test_task)
    loglists[new_logs.id].add_log("CREATE", test_task.body)

    todolists[new_list.id].mark_complete(0)
    loglists[new_logs.id].add_log("MARK COMPLETE", test_task.body)

    assert todolists[new_list.id].tasks[0].status == True
    assert loglists[new_logs.id].logs[0].body == "CREATE Task: Task1"
    assert loglists[new_logs.id].logs[1].body == "MARK COMPLETE Task: Task1"


def test_order_change():
    todolists = {}
    loglists = {}
    test_user = create_User(list_id=str(uuid4), logs_id=str(uuid4))
    new_list = TodoList(test_user.todolist_id, {})
    new_logs = LogList(id=test_user.Loglist_id, logs={})
    todolists[new_list.id] = new_list
    loglists[new_logs.id] = new_logs

    test_task = create_task("Task1", len(new_list.tasks))
    todolists[new_list.id].add_task(test_task)
    loglists[new_logs.id].add_log("CREATE", test_task.body)

    test_task = create_task("Task2", len(new_list.tasks))
    todolists[new_list.id].add_task(test_task)
    loglists[new_logs.id].add_log("CREATE", test_task.body)

    todolists[new_list.id].change_order(0, 1)

    loglists[new_logs.id].add_log("CHANGE ORDER", "0", "1")

    assert todolists[new_list.id].tasks[0].body == "Task2"
    assert todolists[new_list.id].tasks[1].body == "Task1"
    loglists[new_logs.id].logs[0].body == "CREATE Task: Task1"
    loglists[new_logs.id].logs[1].body == "CREATE Task: Task2"
    loglists[new_logs.id].logs[2].body == "CHANGE ORDER Task: 0 to 1"
