#!/usr/bin/env python3
"""
重置用户密码脚本
"""

import hashlib
import os
import subprocess
import sys

def generate_scrypt_hash(password, salt=None):
    """生成scrypt哈希"""
    if salt is None:
        salt = os.urandom(16)
    
    # 使用Python的hashlib.scrypt (Python 3.6+)
    hash_obj = hashlib.scrypt(
        password.encode('utf-8'),
        salt=salt,
        n=32768,  # CPU成本参数
        r=8,      # 内存成本参数
        p=1       # 并行化参数
    )
    
    # 格式: scrypt:N:r:p$salt$hash
    return f"scrypt:32768:8:1${salt.hex()}${hash_obj.hex()}"

def reset_user_password(email, new_password):
    """重置用户密码"""
    try:
        # 生成新的密码哈希
        new_hash = generate_scrypt_hash(new_password)
        
        # 更新数据库
        cmd = [
            "docker", "exec", "docker-mysql-1", "mysql", 
            "-u", "root", "-pragforge123", 
            "-e", f"USE ragforge; UPDATE user SET password='{new_hash}' WHERE email='{email}';"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ 密码重置成功: {email}")
            print(f"   新密码: {new_password}")
            return True
        else:
            print(f"❌ 密码重置失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ 重置密码时出错: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("用法: python reset_password.py <email> <new_password>")
        print("示例: python reset_password.py test@example.com newpassword123")
        sys.exit(1)
    
    email = sys.argv[1]
    new_password = sys.argv[2]
    
    print(f"🔧 重置用户密码: {email}")
    
    if reset_user_password(email, new_password):
        print("\n✅ 密码重置完成!")
        print(f"   现在可以使用新密码登录: {new_password}")
    else:
        print("\n❌ 密码重置失败!")
        sys.exit(1)

if __name__ == "__main__":
    main() 