import os
from fastapi import FastAPI
from .routers import list_router, item_router

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )

# Station 14
# 別モジュールに分割したルーターを読み込む
app.include_router(list_router.router)
app.include_router(item_router.router)

# Station4
@app.get("/health", tags=["System"])
def get_health():
    return { "status": "ok" }

# Station3
@app.get("/echo")
def get_echo(message, name):
    return {"Message":	message + ' ' + name + '!'}

# Station2
@app.get("/hello", tags=["Hello"])
def get_hello():
    return {"Message": "Hello TechTrain!"}