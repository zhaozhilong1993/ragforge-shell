#!/usr/bin/env python3
"""
测试加密和解密功能
"""

import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5

def test_encryption():
    """测试加密功能"""
    # 使用与CLI相同的公钥
    public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAr1KlvagFKU0wgjhJkXnF
a6n9GlxKoOW55rLaITYof+I2rjNBA7ddW22v804MqJSPyC4d4gKbApul5BYXnAhK
8Z6qf9sUMRsks+dc+sxVU/sBUJt1w31HM+KRw4gAias/qRpE9i+VCG7zijZQVpLr
OlZ4a/ia8CZ6dHsknpMq/TU2pPJcp2yJsGb7hroogn1V4lz+H0mRw9idGM0ebs2W
agtNbrO28UZ6tugMK5MQPb1puKlOGVS7EviR+82Cl56jV0NmYDYO7YJlne+X46uB
c5hfhByznXSrmwhZHsgB9wYsWYQf1pO58JtE+gb1GEjoYWN2psJhlGh+23v+DnlP
rQIDAQAB
-----END PUBLIC KEY-----"""
    
    test_password = "testpass123"
    print(f"原始密码: {test_password}")
    
    try:
        # 加密
        rsa_key = RSA.importKey(public_key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        password_base64 = base64.b64encode(test_password.encode('utf-8')).decode("utf-8")
        encrypted_password = cipher.encrypt(password_base64.encode())
        encrypted_b64 = base64.b64encode(encrypted_password).decode('utf-8')
        
        print(f"加密后: {encrypted_b64}")
        
        # 解密（模拟API的decrypt函数）
        # 读取私钥
        with open("/Users/zhaozhilong/Desktop/cursor/ragforge/ragforge/conf/private.pem", "r") as f:
            private_key_content = f.read()
        
        rsa_key_decrypt = RSA.importKey(private_key_content, "Welcome")
        cipher_decrypt = Cipher_pkcs1_v1_5.new(rsa_key_decrypt)
        
        # 解密
        decrypted = cipher_decrypt.decrypt(base64.b64decode(encrypted_b64), "Fail to decrypt password!")
        
        print(f"解密结果类型: {type(decrypted)}")
        print(f"解密结果: {decrypted}")
        
        if isinstance(decrypted, bytes):
            result = decrypted.decode('utf-8')
        else:
            result = decrypted
            
        print(f"最终结果: {result}")
        
        # 解码base64
        final_password = base64.b64decode(result).decode('utf-8')
        print(f"最终密码: {final_password}")
        
        if final_password == test_password:
            print("✅ 加密解密测试成功！")
        else:
            print("❌ 加密解密测试失败！")
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_encryption() 