from .unit_of_work import AbstractUnitOfWork
from ..domain.model import User, TodoList, Task, LogList
from uuid import uuid4


def create_user(
    name: str,
    email: str,
    password: str,
    uow: AbstractUnitOfWork,
    list_id: str,
    loglist_id: str,
):
    with uow:
        new_User: User = User(
            id=str(uuid4()),
            name=name,
            email=email,
            password=password,
            todolist_id=list_id,
            Loglist_id=loglist_id
        )
        uow.Users.add(new_User)
    return new_User


def get_user(uow: AbstractUnitOfWork, name: str):
    with uow:
        user = uow.Users.get(name=name)
        return user


def create_list(uow: AbstractUnitOfWork):
    with uow:
        new_list: TodoList = TodoList(id=str(uuid4()), tasks={})
        uow.TodoLists.add(new_list)

        return new_list


def create_loglist(uow: AbstractUnitOfWork):
    with uow:
        new_list: LogList = LogList(id=str(uuid4()), logs={})
        uow.LogLists.add(new_list)

        return new_list


def get_list(uow: AbstractUnitOfWork, list_id: str):
    with uow:
        ret_list = uow.TodoLists.get(list_id=list_id)
        return ret_list


def get_loglist(uow: AbstractUnitOfWork, list_id: str):
    with uow:
        ret_list = uow.LogLists.get(list_id=list_id)
        return ret_list


def add_task(
        body: str,
        status: bool,
        uow: AbstractUnitOfWork,
        list_id: str,
        loglist_id: str,

):
    with uow:
        todolist = uow.TodoLists.get(list_id)
        loglist = uow.LogLists.get(loglist_id)

        new_task: Task = Task(id=str(uuid4()), body=body,
                              order=len(todolist.tasks), status=status)

        todolist.add_task(new_task)
        loglist.add_log("CREATE", new_task.body)

        uow.LogLists.save(loglist)
        uow.TodoLists.save(todolist)

    return new_task


def delete_task(
        task_order: str,
        uow: AbstractUnitOfWork,
        list_id: str,
        loglist_id: str,

):
    with uow:
        todolist = uow.TodoLists.get(list_id)
        loglist = uow.LogLists.get(loglist_id)

        body = todolist.tasks[task_order].body
        todolist.delete_task(task_order)
        loglist.add_log("DELETE", body)

        uow.LogLists.save(loglist)
        uow.TodoLists.save(todolist)


def change_order(old: str, new: str, uow: AbstractUnitOfWork, list_id: str, loglist_id: str):
    with uow:
        todolist = uow.TodoLists.get(list_id)
        loglist = uow.LogLists.get(loglist_id)

        todolist.change_order(old, new)

        loglist.add_log("CHANGE ORDER", str(old), str(new))

        uow.TodoLists.save(todolist)
        uow.LogLists.save(loglist)


def mark_complete(
        task_id: str,
        uow: AbstractUnitOfWork,
        list_id: str,
        loglist_id: str

):
    with uow:
        todolist = uow.TodoLists.get(list_id)
        loglist = uow.LogLists.get(loglist_id)

        todolist.mark_complete(task_id)

        loglist.add_log("MARK COMPLETE", todolist.tasks[task_id].body)

        uow.TodoLists.save(todolist)
        uow.LogLists.save(loglist)


def edit_task(
        task_id: str,
        uow: AbstractUnitOfWork,
        body: str,
        list_id: str,
        loglist_id: str
):
    with uow:
        todolist = uow.TodoLists.get(list_id)
        loglist = uow.LogLists.get(loglist_id)

        oldbody = todolist.tasks[task_id].body
        todolist.edit_task(task_id, body)

        loglist.add_log("EDIT", oldbody, body)

        uow.TodoLists.save(todolist)
        uow.LogLists.save(loglist)
