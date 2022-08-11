from datetime import date, datetime
from pydantic import BaseModel

class Request_model(BaseModel):
    title: str

class input_request(BaseModel):
    id        : int
    title     : str
    author    : str
    pages     : int
    published : date
    price     : int

class post_request(BaseModel):
    id        : int
    title     : str
    author    : str
    pages     : int
    published : date
    price     : int