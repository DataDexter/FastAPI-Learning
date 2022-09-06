from fastapi import FastAPI
import schemas


app = FastAPI()

fakeDataBase = {
    1:{'task':'Maditation'},
    2:{'task':'Read book'},
    3:{'task':'Code'},
}
@app.get("/{id}")
def getItems(id:int):
    return fakeDataBase[id]


@app.post("/")
def addItem(task:str):
    newId = len(fakeDataBase.keys()) + 1
    fakeDataBase[newId] = {"task":task}
    return fakeDataBase