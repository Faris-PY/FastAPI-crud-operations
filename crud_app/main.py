from fastapi import FastAPI
import validators
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
import secrets
from fastapi.responses import RedirectResponse, JSONResponse

from  . import models, schema, crud
from .database import SessionLocal, engine

app = FastAPI()

def get_db():
    db =  SessionLocal()
    try:
        yield db
    finally:
        db.close()


def raise_bad_title(message): 
    raise HTTPException(status_code=400, detail=message)


@app.get('/')
def get_home():
    return 'Home Page'


@app.get('/books/{title}')
def get_single_Book(data: str, db:Session = Depends(get_db)):
    
    if db_data := crud.get_indiv_book(db=db, dataT = data):
        return db_data
        

@app.get('/books')
def get_all_book(db: Session = Depends(get_db)):
    
    if db_data := crud.get_all_book(db=db):
        return JSONResponse(content=db_data)


@app.post('/books')
def create_book(data: schema.input_request, db:Session = Depends(get_db)):
    
    db_upload = crud.create_book(db=db, data=data)

    return 'Record successfully inserted in Table'

@app.put('/books/{title}')
def update_book(title: str, Book: schema.post_request, db:Session = Depends(get_db)):
    
    db_updated = crud.update_book(Title=title, bookI=Book, db=db)

    return db_updated

@app.delete('/books/{title}')
def delete_book(title: str, db:Session = Depends(get_db)):
    
    db_deleted =  crud.delete_indi_book(Title=title, db=db)

    return 'The record of ' + db_deleted + ' is deleted'