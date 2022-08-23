from fastapi import FastAPI
from ProxyTools import pm

app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/proxy")
async def get_random_proxy():
    proxy = pm.get_random_proxy(pm.collect_conn)
    return {'status': 200, 'proxy': [proxy]}


@app.get("/proxy_all")
async def get_proxy():
    proxy_list = pm.select(pm.collect_conn, 'wait_proxy')
    return {'status': 200, 'proxy': proxy_list}