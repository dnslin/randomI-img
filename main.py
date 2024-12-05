from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
import models
from database import get_db
from fastapi.responses import RedirectResponse

app = FastAPI(title="Random Image API")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Random Image API"}

@app.get("/random")
async def get_random_image(db: Session = Depends(get_db)):
    # 获取随机图片URL
    random_image = db.query(models.ImageUrl).order_by(func.rand()).first()
    if not random_image:
        raise HTTPException(status_code=404, detail="No images found")
    
    # 重定向到实际图片URL
    return RedirectResponse(url=random_image.url)

@app.get("/random/json")
async def get_random_image_json(db: Session = Depends(get_db)):
    # 获取随机图片URL（返回JSON格式）
    random_image = db.query(models.ImageUrl).order_by(func.rand()).first()
    if not random_image:
        raise HTTPException(status_code=404, detail="No images found")
    
    return {
        "id": random_image.id,
        "page": random_image.page,
        "url": random_image.url
    } 