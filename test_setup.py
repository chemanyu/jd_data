#!/usr/bin/env python3
"""
数据库测试脚本
用于测试数据库连接和初始化
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import get_db_connection, init_db

def test_database_connection():
    """测试数据库连接"""
    try:
        connection = get_db_connection()
        print("✓ 数据库连接成功")
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✓ MySQL版本: {version[0]}")
        
        connection.close()
        return True
    except Exception as e:
        print(f"✗ 数据库连接失败: {e}")
        return False

def test_database_initialization():
    """测试数据库初始化"""
    try:
        init_db()
        print("✓ 数据库初始化成功")
        return True
    except Exception as e:
        print(f"✗ 数据库初始化失败: {e}")
        return False

def test_api_connection():
    """测试API连接"""
    try:
        from app.api_client import APIClient
        import requests
        
        api_client = APIClient()
        # 测试API连接（使用一个测试日期）
        response = requests.get(api_client.base_url, params={'date': '20250819'}, timeout=10)
        print(f"✓ API连接测试: HTTP {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✓ API响应正常: {data.get('message', 'Unknown')}")
        return True
    except Exception as e:
        print(f"✗ API连接失败: {e}")
        return False

if __name__ == '__main__':
    print("=== 数据归因分析系统 - 环境测试 ===")
    print()
    
    # 测试数据库连接
    print("1. 测试数据库连接...")
    db_ok = test_database_connection()
    print()
    
    # 测试数据库初始化
    if db_ok:
        print("2. 测试数据库初始化...")
        init_ok = test_database_initialization()
        print()
    else:
        print("2. 跳过数据库初始化测试（数据库连接失败）")
        init_ok = False
        print()
    
    # 测试API连接
    print("3. 测试API连接...")
    api_ok = test_api_connection()
    print()
    
    # 总结
    print("=== 测试结果总结 ===")
    print(f"数据库连接: {'✓ 正常' if db_ok else '✗ 失败'}")
    print(f"数据库初始化: {'✓ 正常' if init_ok else '✗ 失败'}")
    print(f"API连接: {'✓ 正常' if api_ok else '✗ 失败'}")
    print()
    
    if db_ok and init_ok:
        print("🎉 系统准备就绪！可以启动Web应用。")
        print("运行命令: python run.py")
    else:
        print("⚠️  请检查配置后重试。")
        if not db_ok:
            print("   - 确保MySQL服务正在运行")
            print("   - 检查数据库配置信息")
            print("   - 确保数据库 'release_atd' 已创建")
    
    print()
    print("默认登录账号: admin / admin123")
