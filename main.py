from fastapi import FastAPI, Body,Depends
import schemas
import models


from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        
app = FastAPI()

fakeDataBase = {
    1:{'task':'Maditation'},
    2:{'task':'Read book'},
    3:{'task':'Code'},
}

# @app.get("/{id}")
# def getItems(id:int):
#     return fakeDataBase[id]


# @app.post("/")
# def addItem(task:str):
#     newId = len(fakeDataBase.keys()) + 1
#     fakeDataBase[newId] = {"task":task}
#     return fakeDataBase


# @app.post("/")
# def addItem(body = Body()):
#     newId = len(fakeDataBase.keys()) + 1
#     fakeDataBase[newId] = {"task": body['task']}
#     return fakeDataBase

# @app.put("/{id}")
# def updateItem(id:int, item:schemas.Item):
#     fakeDataBase[id]['task'] = item.task
#     return fakeDataBase

# @app.delete("/{id}")
# def deleteItem(id:int):
#     del fakeDataBase[id]
#     return fakeDataBase


@app.get("/")
def getItem(session: Session = Depends(get_session)):
    items = session.query(models.Item).all()
    return items

@app.post("/")
def addItem(item:schemas.Item, session: Session = Depends(get_session)):
    item = models.Item(task = item.task)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item

@app.get("/{id}")
def getItem(id:int, session: Session = Depends(get_session)):
    item = session.query(models.Item).get(id)
    return item

@app.put("/{id}")
def updateItem(id:int, item:schemas.Item, session:Session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    itemObject.task = item.task
    session.commit()
    return itemObject

@app.delete("/{id}")
def deleteItem(id:int, session = Depends(get_session)):
    itemObject = session.query(models.Item).get(id)
    session.delete(itemObject)
    session.commit()
    session.close()
    return 'Item was deleted'

