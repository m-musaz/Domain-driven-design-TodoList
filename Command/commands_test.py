from .commands import *

from ..Command import unit_of_work


def test_create_user():
    with unit_of_work.FakeUnitOfWork() as uow:
        test_user = create_user(
            "Musa", email="mz@hotmail.com", password="123456", uow=uow, list_id=0, loglist_id=0)

    assert test_user.name == "Musa"
    assert test_user.email == "mz@hotmail.com"
    assert test_user.password == "123456"
    assert test_user.todolist_id == 0
    assert test_user.Loglist_id == 0


def test_add_task():
    with unit_of_work.FakeUnitOfWork() as uow:

        test_list = create_list(uow)
        test_loglist = create_loglist(uow)

        test_user = create_user("Musa", "mz@hotmail.com",
                                "12345", uow, test_list.id, test_loglist.id)

        add_task(body="TestBody", status=False,
                 uow=uow, list_id=test_user.todolist_id, loglist_id=test_user.Loglist_id)

        add_task(body="TestBody2", status=False,
                 uow=uow, list_id=test_user.todolist_id, loglist_id=test_user.Loglist_id)

    assert test_list.tasks[0].body == "TestBody"
    assert test_list.tasks[0].status == False
    assert test_list.tasks[1].body == "TestBody2"
    assert test_list.tasks[1].status == False
    assert test_loglist.logs[0].body == "CREATE Task: TestBody"


def test_remove_task():
    with unit_of_work.FakeUnitOfWork() as uow:

        test_list = create_list(uow)
        test_loglist = create_loglist(uow)

        test_user = create_user("Musa", "mz@hotmail.com",
                                "12345", uow, test_list.id, test_loglist.id)

        task1 = add_task(body="TestBody", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        task2 = add_task(body="TestBody2", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        delete_task(task1.order, uow, test_user.todolist_id, test_loglist.id)
        delete_task(task2.order, uow, test_user.todolist_id, test_loglist.id)

        assert len(test_list.tasks) == 0
        assert test_loglist.logs[2].body == "DELETE Task: TestBody"
        assert test_loglist.logs[3].body == "DELETE Task: TestBody2"


def test_change_order():
    with unit_of_work.FakeUnitOfWork() as uow:

        test_list = create_list(uow)
        test_loglist = create_loglist(uow)

        test_user = create_user("Musa", "mz@hotmail.com",
                                "12345", uow, test_list.id, test_loglist.id)

        task1 = add_task(body="TestBody", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        task2 = add_task(body="TestBody2", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        task3 = add_task(body="TestBody3", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        change_order(old=task1.order, new=task2.order,
                     list_id=test_user.todolist_id, uow=uow, loglist_id=test_loglist.id)
        change_order(old=task3.order, new=task1.order,
                     list_id=test_user.todolist_id, uow=uow, loglist_id=test_loglist.id)

        assert test_list.tasks[0].body == "TestBody2"
        assert test_list.tasks[1].body == "TestBody3"
        assert test_list.tasks[2].body == "TestBody"

        assert test_loglist.logs[3].body == "CHANGE ORDER Task: 0 to 1"
        assert test_loglist.logs[4].body == "CHANGE ORDER Task: 2 to 1"


def test_mark_complete():
    with unit_of_work.FakeUnitOfWork() as uow:

        test_list = create_list(uow)
        test_loglist = create_loglist(uow)

        test_user = create_user("Musa", "mz@hotmail.com",
                                "12345", uow, test_list.id, test_loglist.id)

        task1 = add_task(body="TestBody", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        mark_complete(task_id=task1.order, uow=uow,
                      list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        assert test_list.tasks[0].status == True
        assert test_loglist.logs[1].body == "MARK COMPLETE Task: TestBody"


def test_edit():
    with unit_of_work.FakeUnitOfWork() as uow:

        test_list = create_list(uow)
        test_loglist = create_loglist(uow)

        test_user = create_user("Musa", "mz@hotmail.com",
                                "12345", uow, test_list.id, test_loglist.id)

        task1 = add_task(body="TestBody", status=False,
                         uow=uow, list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        edit_task(task_id=task1.order, uow=uow, body="EditedBody",
                  list_id=test_user.todolist_id, loglist_id=test_loglist.id)

        assert test_list.tasks[0].body == "EditedBody"
        assert test_loglist.logs[1].body == "EDIT Task: TestBody to EditedBody"
