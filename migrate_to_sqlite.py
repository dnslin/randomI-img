import os
from dotenv import load_dotenv
import pymysql
import sqlite3
from tqdm import tqdm

# 加载环境变量
load_dotenv()

# MySQL连接配置
mysql_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'db': os.getenv('MYSQL_DATABASE'),
    'port': int(os.getenv('MYSQL_PORT', 3306))
}

def migrate_to_sqlite():
    print("开始数据迁移...")
    
    # 连接MySQL
    mysql_conn = pymysql.connect(**mysql_config)
    mysql_cursor = mysql_conn.cursor()
    
    # 创建SQLite数据库
    sqlite_conn = sqlite3.connect('images.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    try:
        # 创建SQLite表
        sqlite_cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page INTEGER,
            url TEXT
        )
        ''')
        
        # 获取MySQL数据
        mysql_cursor.execute('SELECT COUNT(*) FROM image_urls')
        total_rows = mysql_cursor.fetchone()[0]
        
        print(f"总共需要迁移 {total_rows} 条数据")
        
        # 分批获取数据
        batch_size = 1000
        for offset in tqdm(range(0, total_rows, batch_size)):
            mysql_cursor.execute(f'SELECT page, url FROM image_urls LIMIT {batch_size} OFFSET {offset}')
            batch_data = mysql_cursor.fetchall()
            
            # 插入到SQLite
            sqlite_cursor.executemany(
                'INSERT INTO image_urls (page, url) VALUES (?, ?)',
                batch_data
            )
            sqlite_conn.commit()
        
        print("数据迁移完成！")
        
    finally:
        mysql_cursor.close()
        mysql_conn.close()
        sqlite_cursor.close()
        sqlite_conn.close()

if __name__ == '__main__':
    migrate_to_sqlite() 