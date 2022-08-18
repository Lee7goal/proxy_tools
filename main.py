from fastapi import FastAPI
from sqlite_lee_tools.main import DataBasel

app = FastAPI()
db = DataBasel('proxy.sqlite3')


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/proxy")
async def get_proxy():
    proxy_list = db.select('proxy_available')
    return {'status': 200, 'proxy': proxy_list}
