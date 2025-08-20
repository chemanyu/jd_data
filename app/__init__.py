from flask import Flask
from flask_login import LoginManager
from app.database import init_db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    
    # 初始化登录管理器
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请先登录访问该页面。'
    
    # 用户加载回调
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.get(user_id)
    
    # 注册蓝图
    from app.routes import main_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    # 初始化数据库
    with app.app_context():
        init_db()
    
    return app
