from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
# from flask_login import login_user, logout_user, login_required, current_user  # 已注释掉登录相关导入
from datetime import datetime, timedelta
from app.models import User, QueryLog
from app.api_client import APIClient

# 创建蓝图
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# 认证相关路由 - 已注释掉登录功能
# @auth_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     # 调试信息
#     print(f"Login request - URL: {request.url}")
#     print(f"Login request - Headers: {dict(request.headers)}")
#     
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         
#         user = User.get_by_username(username)
#         if user and user.check_password(password):
#             login_user(user)
#             next_page = request.args.get('next')
#             
#             # 调试重定向
#             if next_page:
#                 print(f"Redirecting to next_page: {next_page}")
#                 return redirect(next_page)
#             else:
#                 dashboard_url = url_for('main.dashboard')
#                 print(f"Redirecting to dashboard: {dashboard_url}")
#                 return redirect(dashboard_url)
#         else:
#             flash('用户名或密码错误', 'error')
#     
#     return render_template('login.html')

# @auth_bp.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('您已成功退出登录', 'success')
#     return redirect(url_for('auth.login'))

# 主页面路由 - 已移除登录要求
@main_bp.route('/')
# @login_required  # 已注释掉登录要求
def dashboard():
    # 获取用户最近的查询记录 - 暂时注释掉用户相关功能
    # recent_logs = QueryLog.get_user_logs(current_user.id, limit=5)
    recent_logs = []  # 临时设置为空列表
    return render_template('dashboard.html', recent_logs=recent_logs)

@main_bp.route('/query', methods=['GET', 'POST'])
# @login_required  # 已注释掉登录要求
def query_data():
    if request.method == 'POST':
        date_input = request.form.get('date')
        if not date_input:
            flash('请输入查询日期', 'error')
            return render_template('query.html')
        
        # 格式化日期
        api_client = APIClient()
        formatted_date = api_client.format_date(date_input)
        
        # 调用API获取数据
        raw_data = api_client.get_attribution_data(formatted_date)
        if raw_data is None:
            flash('获取数据失败，请检查日期格式或网络连接', 'error')
            return render_template('query.html')
        
        # 解析数据
        parsed_data = api_client.parse_api_response(raw_data)
        if parsed_data is None:
            flash('数据解析失败', 'error')
            return render_template('query.html')
        
        # 保存查询记录到数据库 - 暂时注释掉用户相关功能
        # summary = parsed_data.get('summary', {})
        # QueryLog.create(
        #     current_user.id,
        #     formatted_date,
        #     summary.get('total_request_count', 0),
        #     summary.get('total_error_count', 0)
        # )
        
        return render_template('query_result.html', data=parsed_data, query_date=formatted_date)
    
    return render_template('query.html')

@main_bp.route('/api/data')
# @login_required  # 已注释掉登录要求
def api_data():
    """提供JSON格式的数据接口"""
    date = request.args.get('date')
    if not date:
        return jsonify({'error': '缺少日期参数'}), 400
    
    api_client = APIClient()
    formatted_date = api_client.format_date(date)
    
    raw_data = api_client.get_attribution_data(formatted_date)
    if raw_data is None:
        return jsonify({'error': '获取数据失败'}), 500
    
    parsed_data = api_client.parse_api_response(raw_data)
    if parsed_data is None:
        return jsonify({'error': '数据解析失败'}), 500
    
    return jsonify(parsed_data)

@main_bp.route('/history')
# @login_required  # 已注释掉登录要求
def query_history():
    """查询历史记录页面"""
    page = request.args.get('page', 1, type=int)
    # logs = QueryLog.get_user_logs(current_user.id, limit=20)  # 暂时注释掉
    logs = []  # 临时设置为空列表
    return render_template('history.html', logs=logs)

@main_bp.route('/profile')
# @login_required  # 已注释掉登录要求
def profile():
    """用户资料页面"""
    return render_template('profile.html')
