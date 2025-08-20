from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import execute_query, execute_update

class User(UserMixin):
    def __init__(self, id, username, password_hash, email, is_active=True):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self._is_active = is_active
    
    @property
    def is_active(self):
        """返回用户是否处于活跃状态"""
        return self._is_active
    
    @staticmethod
    def get(user_id):
        """根据用户ID获取用户"""
        sql = "SELECT id, username, password_hash, email, is_active FROM users WHERE id = %s"
        result = execute_query(sql, (user_id,))
        if result:
            user_data = result[0]
            return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
        return None
    
    @staticmethod
    def get_by_username(username):
        """根据用户名获取用户"""
        sql = "SELECT id, username, password_hash, email, is_active FROM users WHERE username = %s"
        result = execute_query(sql, (username,))
        if result:
            user_data = result[0]
            return User(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
        return None
    
    def check_password(self, password):
        """检查密码是否正确"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def create(username, password, email):
        """创建新用户"""
        password_hash = generate_password_hash(password)
        sql = "INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)"
        try:
            execute_update(sql, (username, password_hash, email))
            return True
        except Exception as e:
            print(f"创建用户失败: {e}")
            return False

class QueryLog:
    def __init__(self, id, user_id, query_date, total_request_count, total_error_count, query_time):
        self.id = id
        self.user_id = user_id
        self.query_date = query_date
        self.total_request_count = total_request_count
        self.total_error_count = total_error_count
        self.query_time = query_time
    
    @staticmethod
    def create(user_id, query_date, total_request_count, total_error_count):
        """创建查询记录"""
        sql = """
            INSERT INTO query_logs (user_id, query_date, total_request_count, total_error_count) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            execute_update(sql, (user_id, query_date, total_request_count, total_error_count))
            return True
        except Exception as e:
            print(f"创建查询记录失败: {e}")
            return False
    
    @staticmethod
    def get_user_logs(user_id, limit=10):
        """获取用户的查询记录"""
        sql = """
            SELECT id, user_id, query_date, total_request_count, total_error_count, query_time 
            FROM query_logs 
            WHERE user_id = %s 
            ORDER BY query_time DESC 
            LIMIT %s
        """
        results = execute_query(sql, (user_id, limit))
        logs = []
        for row in results:
            logs.append(QueryLog(row[0], row[1], row[2], row[3], row[4], row[5]))
        return logs

class ErrorStatistic:
    def __init__(self, id, query_log_id, error_type, error_count, account_id):
        self.id = id
        self.query_log_id = query_log_id
        self.error_type = error_type
        self.error_count = error_count
        self.account_id = account_id
    
    @staticmethod
    def create(query_log_id, error_type, error_count, account_id=None):
        """创建错误统计记录"""
        sql = """
            INSERT INTO error_statistics (query_log_id, error_type, error_count, account_id) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            execute_update(sql, (query_log_id, error_type, error_count, account_id))
            return True
        except Exception as e:
            print(f"创建错误统计记录失败: {e}")
            return False
