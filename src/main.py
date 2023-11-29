from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import mysql.connector
from mysql.connector import Error

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class TodoItem(BaseModel):
    description: str
    id: int = None 
    status: str 

DB_USER = "todo"
DB_PASSWORD = "1234"
DB_HOST = "127.0.0.1"
DB_DATABASE = "TODO"

def create_database():
    
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
        cursor = cnx.cursor()
        cnx.commit()
        cursor.close()
        cnx.close()
    
create_database()

def get_database_connection():
    return mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)


@app.get("/")
async def read_index(request: Request):
   
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
        cursor = cnx.cursor()
        select_sql = "SELECT * FROM items;"
        cursor.execute(select_sql)
        items = cursor.fetchall()
        cursor.close()
        cnx.close()
        return templates.TemplateResponse("index.html", {"request": request})


@app.post("/todos/")
async def create_todo(todo: TodoItem):
   
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
        cursor = cnx.cursor()
        
        sql = "INSERT INTO items (description, status) VALUES (%s, %s)"
        cursor.execute(sql, (todo.description, todo.status))

        cnx.commit()
        new_todo_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return {"id": new_todo_id, "description": todo.description, "status": todo.status}
    

@app.post("/delete")
async def delete_todo(todo: TodoItem):
    
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
        cursor = cnx.cursor()

        sql = "DELETE FROM items WHERE id = %s;"
        cursor.execute(sql, (id,))

        cnx.commit()
        cursor.close()
        cnx.close()
        return {"message": "Todo item deleted successfully"}

@app.post("/update")
async def update_todo(todo: TodoItem):
    
        cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
        cursor = cnx.cursor()

        sql = "UPDATE items SET description = %s, status = %s WHERE id = %s;"
        cursor.execute(sql, (todo.description, todo.status, todo.id))

        cnx.commit()
        cursor.close()
        cnx.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
