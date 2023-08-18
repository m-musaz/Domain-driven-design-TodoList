from flask import Flask, request, render_template, redirect
from ..Command import commands, unit_of_work
app = Flask(__name__)


@app.route("/")
def returninguser():
    return render_template("login_user.html")


@app.route("/s")
def newuser():
    return render_template("create_user.html")


@app.route('/Signup', methods=["POST"])
def Signup():
    with unit_of_work.UnitOfWork() as uow:
        name = request.form['Name']
        email = request.form['Email']
        password = request.form['Password']
        user_list = commands.create_list(uow=uow)
        log_list = commands.create_loglist(uow=uow)
        user = commands.create_user(
            name=name, email=email, password=password, uow=uow, list_id=user_list.id, loglist_id=log_list.id)
        new_task = commands.add_task(
            "First Task is Added as Demo", False, uow, user_list.id, log_list.id)

        return redirect("/Todolist?id="+str(user.todolist_id)+"&username="+str(user.name)+"&logsID="+str(user.Loglist_id))


@app.route('/login', methods=["POST"])
def Login():
    with unit_of_work.UnitOfWork() as uow:
        name = request.form['Name']
        try:
            user = commands.get_user(uow=uow, name=name)
        except:
            return "<h1>USER NOT FOUND</h1>"
        return redirect("/Todolist?id="+str(user.todolist_id)+"&username="+str(user.name)+"&logsID="+str(user.Loglist_id))


@app.route('/Todolist')
def Show_list():
    args = request.args
    user = args.get('username')
    with unit_of_work.UnitOfWork() as uow:
        user_list_id = args.get('id')
        loglist_id = args.get('logsID')
        try:
            todolist = commands.get_list(uow=uow, list_id=user_list_id)
        except:
            print("No list found")

        loglist = commands.get_loglist(uow=uow, list_id=loglist_id)

    return render_template("show_list.html", tasks=todolist.tasks.values(), user=user, list_id=user_list_id, logs=loglist.logs.values(), loglist_id=loglist_id)


@app.route('/add-task', methods=["POST"])
def add_task():
    with unit_of_work.UnitOfWork() as uow:
        user_list_id = request.form['ListID']
        log_list_id = request.form['LogsID']
        user = request.form['UserName']
        body = request.form['Body']
        try:
            commands.add_task(body=body, status=False,
                              uow=uow, list_id=user_list_id, loglist_id=log_list_id)
        except:
            print("Error adding")

    return redirect("/Todolist?id="+str(user_list_id)+"&username="+str(user)+"&logsID="+str(log_list_id))


@app.route('/change-order', methods=["POST"])
def change_order():
    with unit_of_work.UnitOfWork() as uow:
        user_list_id = request.form['ListID']
        log_list_id = request.form['LogsID']
        user = request.form['UserName']
        old = int(request.form['CurrentOrder'])
        new = int(request.form['NewOrder'])
        try:
            commands.change_order(
                old=old, new=new, uow=uow, list_id=user_list_id, loglist_id=log_list_id)
        except:
            print("Error changing")

    return redirect("/Todolist?id="+str(user_list_id)+"&username="+str(user)+"&logsID="+str(log_list_id))


@app.route('/edit-task', methods=["POST"])
def edit_task():
    with unit_of_work.UnitOfWork() as uow:
        user_list_id = request.form['ListID']
        log_list_id = request.form['LogsID']
        user = request.form['UserName']
        old = int(request.form['CurrentOrder'])
        body = request.form['Body']
        try:
            commands.edit_task(task_id=old, uow=uow,
                               body=body, list_id=user_list_id, loglist_id=log_list_id)
        except:
            print("Error Editing")

    return redirect("/Todolist?id="+str(user_list_id)+"&username="+str(user)+"&logsID="+str(log_list_id))


@app.route('/completed', methods=["POST"])
def mark_complete():
    with unit_of_work.UnitOfWork() as uow:
        user_list_id = request.form['ListID']
        log_list_id = request.form['LogsID']
        user = request.form['UserName']
        old = int(request.form['CurrentOrder'])
        try:
            commands.mark_complete(task_id=old, uow=uow,
                                   list_id=user_list_id, loglist_id=log_list_id)
        except:
            print('Error')

    return redirect("/Todolist?id="+str(user_list_id)+"&username="+str(user)+"&logsID="+str(log_list_id))


@app.route('/delete', methods=["POST"])
def delete_task():
    with unit_of_work.UnitOfWork() as uow:
        user_list_id = request.form['ListID']
        log_list_id = request.form['LogsID']
        user = request.form['UserName']
        old = int(request.form['CurrentOrder'])
        try:
            commands.delete_task(task_order=old, uow=uow,
                                 list_id=user_list_id, loglist_id=log_list_id)
        except:
            print("Error")

    return redirect("/Todolist?id="+str(user_list_id)+"&username="+str(user)+"&logsID="+str(log_list_id))
