#!/usr/bin/env python3
"""
RAGForge 密码加密工具
使用RSA公钥加密密码，与前端保持一致
"""

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5


def encrypt_password(password: str) -> str:
    """
    使用RSA公钥加密密码
    
    Args:
        password: 原始密码
        
    Returns:
        加密后的密码字符串
    """
    # RSA公钥（与前端使用相同的公钥）
    public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArq9XTUSeYr2+N1h3Afl/
z8Dse/2yD0ZGrKwx+EEEcdsBLca9Ynmx3nIB5obmLlSfmskLpBo0UACBmB5rEjBp2
Q2f3AG3Hjd4B+gNCG6BDaawuDlgANIhGnaTLrIqWrrcm4EMzJOnAOI1fgzJRsOOUE
faS318Eq9OVO3apEyCCt0lOQK6PuksduOjVxtltDav+guVAA068NrPYmRNabVKRNL
JpL8w4D44sfth5RvZ3q9t+6RTArpEtc5sh5ChzvqPOzKGMXW83C95TxmXqpbK6olN
4RevSfVjEAgCydH6HN6OhtOQEcnrU97r9H0iZOWwbw3pVrZiUkuRD1R56Wzs2wID
AQAB
-----END PUBLIC KEY-----"""
    
    try:
        # 将密码进行base64编码
        password_base64 = base64.b64encode(password.encode('utf-8')).decode("utf-8")
        
        # 使用RSA公钥加密
        rsa_key = RSA.importKey(public_key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        encrypted_password = cipher.encrypt(password_base64.encode())
        
        # 返回base64编码的加密结果
        return base64.b64encode(encrypted_password).decode('utf-8')
    except Exception as e:
        raise Exception(f"密码加密失败: {e}")


def test_encryption():
    """测试密码加密功能"""
    test_password = "test123"
    print(f"原始密码: {test_password}")
    
    try:
        encrypted = encrypt_password(test_password)
        print(f"加密后: {encrypted}")
        print("✅ 密码加密测试成功")
        return True
    except Exception as e:
        print(f"❌ 密码加密测试失败: {e}")
        return False


if __name__ == "__main__":
    test_encryption() 