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
    使用RSA公钥加密密码，与后端/前端一致
    """
    public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr1KlvagFKU0wgjhJkXnF
a6n9GlxKoOW55rLaITYof+I2rjNBA7ddW22v804MqJSPyC4d4gKbApul5BYXnAhK
8Z6qf9sUMRsks+dc+sxVU/sBUJt1w31HM+KRw4gAias/qRpE9i+VCG7zijZQVpLr
OlZ4a/ia8CZ6dHsknpMq/TU2pPJcp2yJsGb7hroogn1V4lz+H0mRw9idGM0ebs2W
agtNbrO28UZ6tugMK5MQPb1puKlOGVS7EviR+82Cl56jV0NmYDYO7YJlne+X46uB
c5hfhByznXSrmwhZHsgB9wYsWYQf1pO58JtE+gb1GEjoYWN2psJhlGh+23v+DnlP
rQIDAQAB
-----END PUBLIC KEY-----"""
    rsa_key = RSA.importKey(public_key)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    password_base64 = base64.b64encode(password.encode('utf-8')).decode('utf-8')
    encrypted_password = cipher.encrypt(password_base64.encode())
    return base64.b64encode(encrypted_password).decode('utf-8')


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