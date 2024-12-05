from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func, text
import models
from database import get_db
from fastapi.responses import RedirectResponse
from typing import List

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
    # 使用SQLite的RANDOM()函数获取随机图片URL
    random_image = db.query(models.ImageUrl).order_by(text("RANDOM()")).first()
    if not random_image:
        raise HTTPException(status_code=404, detail="No images found")
    
    # 重定向到实际图片URL
    return RedirectResponse(url=random_image.url)

@app.get("/random/json")
async def get_random_image_json(db: Session = Depends(get_db)):
    # 使用SQLite的RANDOM()函数获取随机图片URL
    random_image = db.query(models.ImageUrl).order_by(text("RANDOM()")).first()
    if not random_image:
        raise HTTPException(status_code=404, detail="No images found")
    
    return {
        "id": random_image.id,
        "page": random_image.page,
        "url": random_image.url
    }

@app.get("/random/batch")
async def get_random_images_batch(
    limit: int = Query(default=10, ge=1, le=100, description="返回的图片数量，范围1-100"),
    db: Session = Depends(get_db)
):
    """
    批量返回随机图片
    - limit: 返回的图片数量，默认10张，最多100张
    """
    random_images = db.query(models.ImageUrl).order_by(text("RANDOM()")).limit(limit).all()
    if not random_images:
        raise HTTPException(status_code=404, detail="No images found")
    
    return {
        "count": len(random_images),
        "images": [
            {
                "id": img.id,
                "page": img.page,
                "url": img.url
            }
            for img in random_images
        ]
    } 