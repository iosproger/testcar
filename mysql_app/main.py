import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mysql_app.node_views import router as node_router
from mysql_app.vin_views import router as vin_router
from mysql_app.bind_views import router as bind_router
from mysql_app.location_views import router as loc_router
from mysql_app.mobile_views import router as mb_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://192.168.0.102",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(node_router)
app.include_router(vin_router)
app.include_router(bind_router)
app.include_router(loc_router)
app.include_router(mb_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Backend!"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True, host="0.0.0.0",port=8001)
