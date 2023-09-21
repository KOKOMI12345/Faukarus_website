import hashlib

def encrypt_password(password):
    # 创建一个SHA256加密对象
    sha256 = hashlib.sha256()
    # 更新加密对象的内容
    sha256.update(password.encode('utf-8'))
    # 获取加密后的结果
    encrypted_password = sha256.hexdigest()
    # 返回加密后的密码
    return encrypted_password

# 示例用法
password = ""
encrypted_password = encrypt_password(password)
print(encrypted_password)