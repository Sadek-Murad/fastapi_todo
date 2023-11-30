from fastapi import Form, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import mysql.connector
from typing import Annotated
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
DB_DATABASE = "todo"


def get_database_connection():
    cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_DATABASE)
    return cnx


@app.get("/")
async def read_index(request: Request):
   
        cnx = get_database_connection()
        cursor = cnx.cursor()
        select_sql = "SELECT * FROM items;"
        cursor.execute(select_sql)
        items = cursor.fetchall()
        cursor.close()
        cnx.close()
        return templates.TemplateResponse("index.html", {"request": request, "items": items})


@app.post("/", response_class=RedirectResponse)
def create_todo(description: Annotated[str, Form()]):
    cnx = get_database_connection()
    print("######", cnx)
    cursor = cnx.cursor()
    
    sql = "INSERT INTO items (description) VALUES (%s);"
    data =description
    print(sql) 
    print(data)
    cursor.execute(sql, data)
    
    cnx.commit()
    
    cursor.close()
    cnx.close()
    return RedirectResponse(url="http://127.0.0.1:8000", status_code=303)

    

@app.post("/delete")
async def delete_todo(todo_id: int):
    
        cnx = get_database_connection()
        cursor = cnx.cursor()

        sql = "DELETE FROM items WHERE id = %s;"
        cursor.execute(sql, (todo_id,))

        cnx.commit()
        cursor.close()
        cnx.close()
        return {"message": "Todo-Eintrag erfolgreich gelöscht"}

@app.post("/update")
async def update_todo(todo_id: int, new_status: str):
    
    cnx = get_database_connection()
    cursor = cnx.cursor()

    sql = "UPDATE items SET description = %s, status = %s WHERE id = %s;"
    cursor.execute(sql, (new_status, todo_id))

    cnx.commit()
    cursor.close()
    cnx.close()
    
    return {"message": "Status des Todo-Eintrags erfolgreich aktualisiert"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
