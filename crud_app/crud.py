from statistics import mode
from turtle import title
from sqlalchemy.orm import Session
from sqlalchemy import update

import xml.etree.ElementTree as ET
from fastapi.encoders import jsonable_encoder

from . import models, schema

# Function to get individual book.  
def get_indiv_book(db: Session, dataT: str) -> models.books:
    db_data = (db.query(models.books)
                .filter(models.books.title == dataT)
              .first()
            )
    if db_data is None:
        response = 'Title not found'
        return response
    else:
        response = {'title': db_data.title, 
        'author': db_data.author,
        'pages': db_data.pages,
        'published': db_data.published,
        'prices': db_data.price 
                }
        
    return response


# Function to get all the books details from table
def get_all_book(db: Session):

    db_data = db.query(models.books).all()

    root = ET.Element('Library')
    library_dict = {}

    i = 1
    for data in db_data:
        sub = ET.Element('Book')
        root.append(sub)

        title = data.title
        b1 = ET.SubElement(sub, 'title')
        b1.text = title
        
        author = data.author
        b2 = ET.SubElement(sub, 'author')
        b2.text = author

        pages = data.pages 
        b3 = ET.SubElement(sub, "pages")
        b3.text = str(pages)
        
        published = data.published
        b4 = ET.SubElement(sub, 'published')
        b4.text = str(published)

        price = data.price
        b5 = ET.SubElement(sub, 'price')
        b5.text = str(price)

        #creating dictionary
        #sub dictionary
        sub_dic = {}
        sub_dic['title'] = title
        sub_dic['author'] = author
        sub_dic['pages'] = pages
        sub_dic['published'] = published
        sub_dic['price'] = price

        main_key = 'Book' + '_' + str(i)
        i = i+1

        library_dict[main_key] = sub_dic

    jsonData = jsonable_encoder(library_dict)

    tree = ET.ElementTree(root)  
    
    # xmlNeeded Flag set to True, if table records needed in XML form
    xmlNeeded = False

    if xmlNeeded:
        with open ('File Location', "wb") as files :
            tree.write(files)

    return jsonData



# fucntion to create a book
def create_book(db: Session, data: schema.input_request) -> models.books:
    
    db_upload = models.books(
        id = data.id,
        title = data.title,
        author = data.author,
        pages = data.pages,
        published = data.published,
        price = data.price
    )
    db.add(db_upload)
    db.commit()
    db.refresh(db_upload)
    
    return db_upload


# function to update the book record
def update_book(Title: title, bookI: schema.post_request, db: Session) -> models.books:

    db.query(models.books).filter(models.books.title==Title).update(
         {models.books.id: bookI.id, 
          models.books.title: bookI.title, 
          models.books.author: bookI.author, 
          models.books.pages: bookI.pages,
          models.books.published: bookI.published,
          models.books.price: bookI.price
          }, synchronize_session=False )
    db.commit()
    
    db_updatedF = db.query(models.books).filter(models.books.title==bookI.title).first()
    
    response = {'title': db_updatedF.title, 
        'author': db_updatedF.author,
        'pages': db_updatedF.pages,
        'published': db_updatedF.published,
        'prices': db_updatedF.price 
                }
        

    return response

# function to delete a specifi book
def delete_indi_book(Title: title, db: Session):


    db.query(models.books).filter(models.books.title == Title).delete(synchronize_session= False)
    db.commit()

    return Title

