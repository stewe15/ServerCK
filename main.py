import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import requests as rq
from bs4 import BeautifulSoup

app = FastAPI()

@app.websocket('/ws/parse')
async def send_parsed(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            page = rq.get(data)
            soup = BeautifulSoup(page.text, "html.parser")
            mas = soup.findAll('html')
            for i in mas:
                await websocket.send_text(str(i))
    except WebSocketDisconnect:
        print("Client disconnected")

@app.websocket('/ws/parseViaTeg')
async def send_parsed_with_teg(websocked: WebSocket):
    await websocked.accept()
    try:
        while True:
            data = await websocked.receive_text()
            data_parsed = data.split('\t')
            page = rq.get(data_parsed[0])
            soup = BeautifulSoup(page.text, "html.parser")
            mas = soup.findAll(f'{data_parsed[1]}')
            for i in mas:
                await websocked.send_text(i.text)
    except WebSocketDisconnect:
        print("Client disconected")




