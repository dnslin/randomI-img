# Random Image API

一个基于FastAPI的随机图片API服务。

## 功能特点

- 随机返回图片URL
- 支持直接重定向到图片
- 支持JSON格式返回图片信息
- 使用MySQL存储图片URL

## 安装

1. 克隆项目
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 配置环境变量：
复制 `.env.example` 到 `.env` 并修改数据库配置

## 运行

```bash
uvicorn main:app --reload
```

## API接口

- `GET /`: 欢迎页面
- `GET /random`: 随机返回一张图片（重定向）
- `GET /random/json`: 随机返回一张图片的信息（JSON格式）

## 数据库结构

```sql
CREATE TABLE `image_urls` (
  `id` int NOT NULL AUTO_INCREMENT,
  `page` int DEFAULT NULL,
  `url` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
``` 