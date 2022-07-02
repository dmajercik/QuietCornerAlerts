from typing import List

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import configparser
from pydantic import BaseSettings
config = configparser.RawConfigParser()
configFilePath = r'resources/secret.config'
config.read(configFilePath)

import fastapi
from fastapi.middleware.cors import CORSMiddleware

from routes import personmanager, cad, incidentmanager, addressmanager, usermanager, website, news
from mongoengine import connect

class Settings(BaseSettings):
    app_name: str = "Quiet Corner Alerts"
    MONGODB_SETTINGS: str = config.get('key','mongodb')
    CKEDITOR_PKG_TYPE: str = "standard"

settings = Settings()
app = fastapi.FastAPI(
    title="Quiet Corner Alerts API",
    description="The backend API for the Quiet Corner Alerts CAD system",
    version="0.0.1"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(incidentmanager.router)
app.include_router(cad.router)
app.include_router(usermanager.router)
app.include_router(personmanager.router)
app.include_router(addressmanager.router)
app.include_router(website.router)
app.include_router(news.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def initialize_db():
    print(settings.MONGODB_SETTINGS)
    connect(host=settings.MONGODB_SETTINGS)
    print("Mongo Connected successfully")

initialize_db()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    await manager.broadcast('New User')
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

if __name__ == '__main__':
    uvicorn.run("application:app", host="0.0.0.0", port=3321, reload=True)
