from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    title : str
    status : str

class UpdateTodo(BaseModel):
    title : Optional[str]= None
    status : Optional[str]= None

todos = {
    1: Todo(title = "Chase deadline for work", status = "pending"),
    2: Todo(title = "Mow the lawn", status = "completed")
}

@app.get("/")
def index():
    return { "Data" : "Hello! This is a To Do List powered by FastAPI."}

#path paramater
# domain/get-todo/1

@app.get("/get-task/{id}")
def get_task(id : int = Path(description = "Search the ID of the desired task")):
    return todos[id]

#query parameter
#domain / get-todo?search="title"
## (Igonre this if it doesn't work, it was only for demo) (and it failed (sad))
@app.get("/get-todo-by-title/{title}")
def get_todo(title: str): 
    for todo_id in todos:
        if todos[todo_id].title == title:
            return todos[todo_id]
    return {"Error":"The title you have entered does not exist. Please retry. (It is case sensitive)"}

#POST method
@app.post("/create-todo/{todo_id}")
def add_todo(todo_id: int, todo :Todo):
    if todo_id in todos:
        return {"error" : "Creating task failed. This ID already exists"}
    todos[todo_id] = todo
    return todos[todo_id]

#PUT method
@app.put("/update-todo/{todo_id}")
def update_todo(todo_id: int, todo: UpdateTodo):
    if todo_id not in todos:
        return {"error" : "Update failed. ID does not exist"}

    if todo.title != None:
        todos[todo_id].title = todo.title
    if todo.status != None:
        todos[todo_id].status = todo.status
        
    return todos[todo_id]

#DELETE method
@app.delete("/delete-todo/{todo_id}")
def delete_todo(todo_id:int = Path(description="Please choose a task to delete")):
    if todo_id not in todos:
        return {"error" : "Deleting failed. ID does not exist"}
    del todos[todo_id]
    return {"data" : "Deletion Complete"}