from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sqlite3
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os

app = FastAPI(title="Server Board API")

# データベースファイルのパスを絶対パスで設定
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'server_board.db')

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
    invite_url: Optional[str] = None

@app.get("/api/servers", response_model=List[Server])
async def get_servers():
    if not os.path.exists(DB_PATH):
        raise HTTPException(status_code=500, detail=f"Database file not found at {DB_PATH}")
    
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # テーブルが存在するか確認
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='servers'")
            if not cursor.fetchone():
                raise HTTPException(status_code=500, detail="Servers table does not exist")
            
            # データを取得（rank_pointsが同じ場合は最後のup時間が新しい順、NULLは最後に）
            cursor.execute('''
                SELECT * FROM servers 
                ORDER BY 
                    rank_points DESC,
                    CASE WHEN last_up_time IS NULL THEN 0 ELSE 1 END DESC,
                    last_up_time DESC,
                    registered_at DESC
            ''')
            servers = cursor.fetchall()
            
            if not servers:
                return []
                
            return [dict(server) for server in servers]
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/api/servers/{server_id}", response_model=Server)
async def get_server(server_id: int):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM servers WHERE server_id = ?', (server_id,))
            server = cursor.fetchone()
            
            if server is None:
                raise HTTPException(status_code=404, detail="Server not found")
                
            return dict(server)
    except sqlite3.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# 静的ファイルの設定（APIエンドポイントの後に配置）
app.mount("/", StaticFiles(directory="public", html=True), name="static")

if __name__ == "__main__":
    print(f"Database path: {DB_PATH}")
    print(f"Database exists: {os.path.exists(DB_PATH)}")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)