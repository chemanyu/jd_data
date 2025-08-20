from app import create_app
from app.database import init_db

if __name__ == '__main__':
    app = create_app()
    
    # 初始化数据库
    with app.app_context():
        init_db()
        print("数据库初始化完成")
    
    # 启动应用
    app.run(debug=True, host='127.0.0.1', port=5002)
