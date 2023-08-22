from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import producto, orden, sucursal


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(producto.router)
app.include_router(orden.router)
app.include_router(sucursal.router)