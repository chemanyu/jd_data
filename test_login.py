#!/usr/bin/env python3
"""
测试用户登录功能
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import User

def test_user_login():
    """测试用户登录功能"""
    try:
        # 测试获取用户
        user = User.get_by_username('admin')
        if user:
            print(f"✓ 找到用户: {user.username}")
            print(f"  用户ID: {user.id}")
            print(f"  邮箱: {user.email}")
            print(f"  状态: {'活跃' if user.is_active else '未活跃'}")
            
            # 测试密码验证
            if user.check_password('admin123'):
                print("✓ 密码验证成功")
                return True
            else:
                print("✗ 密码验证失败")
                return False
        else:
            print("✗ 未找到admin用户")
            return False
            
    except Exception as e:
        print(f"✗ 测试失败: {e}")
        return False

if __name__ == '__main__':
    print("=== 用户登录测试 ===")
    if test_user_login():
        print("✓ 用户登录功能正常")
    else:
        print("✗ 用户登录功能异常")
