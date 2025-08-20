import pymysql

DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'release_atd',
    'charset': 'utf8mb4'
}

def get_db_connection():
    """获取数据库连接"""
    return pymysql.connect(**DB_CONFIG)

def init_db():
    """初始化数据库表"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 创建用户表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            
            # 创建数据查询记录表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS query_logs (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT,
                    query_date VARCHAR(8) NOT NULL,
                    total_request_count INT DEFAULT 0,
                    total_error_count INT DEFAULT 0,
                    query_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # 创建错误统计表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS error_statistics (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    query_log_id INT,
                    error_type VARCHAR(50) NOT NULL,
                    error_count INT DEFAULT 0,
                    account_id VARCHAR(20),
                    FOREIGN KEY (query_log_id) REFERENCES query_logs(id)
                )
            """)
            
            # 检查是否存在默认用户，如果不存在则创建
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            result = cursor.fetchone()
            if result[0] == 0:
                from werkzeug.security import generate_password_hash
                admin_password = generate_password_hash('admin123')
                cursor.execute("""
                    INSERT INTO users (username, password_hash, email) 
                    VALUES ('admin', %s, 'admin@example.com')
                """, (admin_password,))
            
            connection.commit()
            print("数据库初始化完成")
            
    except Exception as e:
        print(f"数据库初始化错误: {e}")
        connection.rollback()
    finally:
        connection.close()

def execute_query(sql, params=None):
    """执行查询语句"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.fetchall()
    finally:
        connection.close()

def execute_update(sql, params=None):
    """执行更新语句"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params)
            connection.commit()
            return cursor.rowcount
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        connection.close()
