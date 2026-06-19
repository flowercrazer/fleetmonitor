from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio  # 💡 이 부분이 누락되어 에러가 났었습니다!
import math
import json

app = FastAPI()

# 1. 원운동을 위한 좌표 리스트 미리 생성 (반시계방향)
circle_path = []
center_x, center_y, radius = 500, 200, 120
for i in range(16):  
    angle = (i / 16) * (2 * math.pi)
    circle_path.append({
        "x": int(center_x - radius * math.cos(angle)), 
        "y": int(center_y - radius * math.sin(angle))
    })

# 2. JSON 형태의 디바이스 경로 설정 데이터
devices_config = {
    "D001": {
        "color": "#2ed573",
        "path": [
            {"x": 100, "y": 150},
            {"x": 700, "y": 150}
        ],
        "options": {"yoyo": True, "duration": 1}  
    },
    "D002": {
        "color": "#eccc68",
        "path": [
            {"x": 450, "y": 20},
            {"x": 300, "y": 200},
            {"x": 600, "y": 200}
            
        ],
        "options": {"yoyo": False, "duration": 2} 
    },
    "D003": {
        "color": "#ff4757",
        "path": [{"x": 500, "y": 200}], # 중심점 좌표 딱 하나만 전송
        "options": {"type": "spin", "radius": 100,"show_trace":True, "duration": 3} # 5초 동안 한 바퀴 회전
    },
    "D004": {
        "color": "#2e92d5",
        "path": [
            {"x": 100, "y": 50},
            {"x": 100, "y": 450}
        ],
        "options": {"yoyo": True, "duration": 4}  
    },
}

@app.get("/")
def get_dashboard():
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # 웹 브라우저가 연결되면 설정된 JSON 데이터를 보냅니다.
    await websocket.send_text(json.dumps(devices_config))
    
    try:
        while True:
            # 웹소켓 연결이 끊어지지 않도록 무한 대기 루프를 돕니다.
            await asyncio.sleep(1)
    except Exception as e:
        print("웹소켓 연결 종료:", e)