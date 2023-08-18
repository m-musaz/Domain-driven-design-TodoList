drop table if exists Users cascade;
drop table if exists TodoList cascade;
drop table if exists Task cascade;
drop table if exists TodoListTask cascade;
drop table if exists LogList cascade;
drop table if exists Logs cascade;
drop table if exists LogListLogs cascade;


create table Task (
    id uuid,
    body varchar(512),
    status boolean,
    order_num int,

    primary key (id)
);

create table TodoList (
    id uuid UNIQUE NULL,

    primary key (id)
);

CREATE TABLE TodoListTask (
    todolist_id uuid REFERENCES TodoList(id),
    task_id uuid REFERENCES Task(id),
    PRIMARY KEY (todolist_id, task_id)
);

create table Logs (
    id uuid,
    body varchar(512),
    order_num int,

    primary key (id)
);

create table LogList (
    id uuid UNIQUE NULL,

    primary key (id)
);

CREATE TABLE LogListLogs (
    List_id uuid REFERENCES LogList(id),
    Log_id uuid REFERENCES Logs(id),
    PRIMARY KEY (List_id, Log_id)
);

create table Users (
    id uuid,
    name varchar(100),
    email varchar(100),
    password varchar(100),
    todolist_id uuid,
    loglist_id uuid,
  
    primary key (id),

    foreign key (todolist_id)
        references Todolist(id),
    
    foreign key (loglist_id)
        references LogList(id)
);

