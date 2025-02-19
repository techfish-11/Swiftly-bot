from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Server Board API")

# 静的ファイルの設定
app.mount("/", StaticFiles(directory="public", html=True), name="static")

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Server(BaseModel):
    server_id: int
    server_name: str
    icon_url: Optional[str] = None
    description: Optional[str] = None
    rank_points: int
    last_up_time: Optional[datetime] = None
    registered_at: datetime

@app.get("/servers", response_model=List[Server])
async def get_servers():
    try:
        with sqlite3.connect('server_board.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # ランクポイントの高い順、登録日時の新しい順にソート
            cursor.execute('''
                SELECT * FROM servers 
                ORDER BY rank_points DESC, registered_at DESC
            ''')
            servers = cursor.fetchall()
            return [dict(server) for server in servers]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/servers/{server_id}", response_model=Server)
async def get_server(server_id: int):
    try:
        with sqlite3.connect('server_board.db') as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM servers WHERE server_id = ?', (server_id,))
            server = cursor.fetchone()
            
            if server is None:
                raise HTTPException(status_code=404, detail="Server not found")
                
            return dict(server)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)