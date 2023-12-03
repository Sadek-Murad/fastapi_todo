from fastapi import Form, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
import mysql.connector
from typing import Annotated
from mysql.connector import Error
from dotenv import load_dotenv
from pathlib import Path
import os



load_dotenv()
app = FastAPI()
templates = Jinja2Templates(directory="templates")






#class TodoItem(BaseModel):
    #description: str
    #id: int = None 
    #status: str 


def get_database_connection():
    cnx = mysql.connector.connect(
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_DATABASE')
    )
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

def insertIntoDB(cnx, description):
  
  
  cursor = cnx.cursor()
    
  sql = "INSERT INTO items (description) VALUES (%s);"
  data = [description]
  
  cursor.execute(sql, data)
  cnx.commit()
    


@app.post("/additem", response_class=RedirectResponse)
def create_todo(description: Annotated[str, Form()]):
    cnx = get_database_connection()
    insertIntoDB(cnx, description)
    #cursor.close()
    #cnx.close()
    return RedirectResponse(url="/", status_code=303)
    cnx.close()
    

    

@app.post("/delete", response_class=RedirectResponse)
def delete_todo(id: Annotated[int, Form()]):
    
        cnx = get_database_connection()
        cursor = cnx.cursor()

        sql = "DELETE FROM items WHERE id = %s;"
        
        cursor.execute(sql, id)
       
        cnx.commit()
        cursor.close()
        cnx.close()
        return RedirectResponse(url="/", status_code=303)

@app.post("/update", response_class=RedirectResponse)
def update_todo(id: Annotated[int, Form()]):
    cnx = get_database_connection()
    cursor = cnx.cursor()
    
    
    
    sql = """
    UPDATE items
    SET status = CASE
        WHEN status = 'open' THEN 'in progress'
        WHEN status = 'in progress' THEN 'finished'
        ELSE status
    END
    WHERE id = %s;
    """
    
    cursor.execute(sql, (id,))


    
    cnx.commit()
    cursor.close()
    cnx.close()
    
    return RedirectResponse(url="/", status_code=303)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv('UVICORN_HOST'), port=8000)
