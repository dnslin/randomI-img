# Random Image API

一个基于FastAPI的随机图片API服务。

## 功能特点

- 随机返回图片URL
- 支持直接重定向到图片
- 支持JSON格式返回图片信息
- 使用SQLite本地数据库存储图片URL
- 支持Docker部署

## 本地安装

1. 克隆项目
2. 安装依赖：

```bash
pip install -r requirements.txt
```

## 本地运行

```bash
uvicorn main:app --reload
```

## Docker部署

### 方式一：从GitHub Packages拉取镜像

```bash
# 1. 拉取最新镜像
docker pull ghcr.io/你的用户名/项目名:latest

# 2. 创建数据卷（用于持久化数据库）
docker volume create random-img-data

# 3. 运行容器
docker run -d \
  --name random-img-api \
  -p 8000:8000 \
  -v random-img-data:/app/data \
  ghcr.io/你的用户名/项目名:latest
```

### 方式二：本地构建镜像

```bash
# 1. 构建镜像
docker build -t random-img-api .

# 2. 创建数据卷
docker volume create random-img-data

# 3. 运行容器
docker run -d \
  --name random-img-api \
  -p 8000:8000 \
  -v random-img-data:/app/data \
  random-img-api
```

### 访问服务

服务启动后，可以通过以下地址访问：

- API文档：`http://localhost:8000/docs`
- 健康检查：`http://localhost:8000/`

## API接口

- `GET /`: 欢迎页面
- `GET /random`: 随机返回一张图片（重定向）
- `GET /random/json`: 随机返回一张图片的信息（JSON格式）
- `GET /random/batch?limit=10`: 批量返回随机图片（默认10张，最多100张）

## 数据库结构

SQLite数据库文件位置：`/app/data/images.db`

表结构：

```sql
CREATE TABLE image_urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page INTEGER,
    url TEXT
);
```

## 数据持久化

Docker部署时，数据库文件存储在 `random-img-data` 数据卷中，确保容器重启后数据不会丢失。

## 环境要求

- Python 3.11+
- Docker（可选）