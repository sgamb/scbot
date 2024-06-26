import json

from telegram import InlineKeyboardButton

from request_model import Model
from task_model import Model as TaskModel


def get_some_requests():
    with open("requests.json", "r") as f:
        raw_data = f.read()
    data = json.loads(raw_data)
    serialized_data = Model(**data)
    return serialized_data.requests


def get_request_by_callback_data(callback_data):
    request_id = callback_data.split("_")[-1]
    # TODO: handle StopIteration exception
    return next(request for request in get_some_requests() if request.id == request_id)


def read_task():
    with open("tasks.json", "r") as f:
        raw_data = f.read()
    data = json.loads(raw_data)
    serialized_data = TaskModel(**data)
    return serialized_data.tasks


tasks = read_task()


def get_some_tasks():
    return tasks


def compose_keyboard(objects, param, name):
    simplified_objects = []
    for obj in objects:
        simplified_objects.append(obj.representation())
    keyboard = []
    for obj in simplified_objects:
        button = InlineKeyboardButton(
            text=f"#{obj.get('id')} {obj.get(param)}",
            callback_data=f"{name}_{obj.get('id')}"
        )
        keyboard.append(button)
    return keyboard


def get_task_by_callback_data(callback_data):
    task_id = callback_data.split("_")[-1]
    # TODO: handle StopIteration exception
    return next(task for task in get_some_tasks() if task.id == task_id)


back_to_menu_button = InlineKeyboardButton(
    text="Go back",
    callback_data="menu"
)


def delete_task(task_id):
    new_tasks = []
    global tasks
    for task in tasks:
        if task.id != task_id:
            new_tasks.append(task)
    tasks = new_tasks
