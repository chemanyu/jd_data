from flask import Flask
# from flask_login import LoginManager  # 已注释掉登录管理器
from app.database import init_db
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # ===== 反向代理支持配置 =====
    # 添加ProxyFix中间件处理nginx代理头部
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,        # X-Forwarded-For
        x_proto=1,      # X-Forwarded-Proto  
        x_host=1,       # X-Forwarded-Host
        x_prefix=1      # X-Forwarded-Prefix
    )
    
    # 配置子路径 - 匹配nginx反向代理路径
    app.config['APPLICATION_ROOT'] = 'guangyixin'
    
    # 添加子路径处理中间件
    class SubPathMiddleware:
        def __init__(self, app, script_name=None):
            self.app = app
            self.script_name = script_name

        def __call__(self, environ, start_response):
            # 处理子路径
            if self.script_name:
                environ['SCRIPT_NAME'] = self.script_name
                path_info = environ['PATH_INFO']
                if path_info.startswith(self.script_name):
                    environ['PATH_INFO'] = path_info[len(self.script_name):]
            return self.app(environ, start_response)
    
    # 应用中间件
    app.wsgi_app = SubPathMiddleware(app.wsgi_app, 'guangyixin')
    
    # 如果使用HTTPS，强制使用HTTPS scheme
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    
    # 初始化登录管理器 - 已注释掉登录功能
    # login_manager = LoginManager()
    # login_manager.init_app(app)
    # login_manager.login_view = 'auth.login'
    # login_manager.login_message = '请先登录访问该页面。'
    
    # 用户加载回调 - 已注释掉
    # @login_manager.user_loader
    # def load_user(user_id):
    #     from app.models import User
    #     return User.get(user_id)
    
    # 注册蓝图
    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    # app.register_blueprint(auth_bp, url_prefix='/auth')  # 注释掉认证蓝图
    
    # 添加模板上下文处理器，提供假的current_user对象
    @app.context_processor
    def inject_user():
        # 创建一个假的用户对象，避免模板报错
        class FakeUser:
            is_authenticated = False
            username = "匿名用户"
            email = ""
            created_at = None
            is_active = True
        
        return dict(current_user=FakeUser())
    
    # 初始化数据库
    with app.app_context():
        init_db()
    
    return app
