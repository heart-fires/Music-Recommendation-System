from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# 生成私钥
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# 将私钥序列化为PEM格式
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# 保存私钥到文件
with open('private_key.pem', 'wb') as f:
    f.write(private_pem)

# 从私钥中提取公钥
public_key = private_key.public_key()

# 将公钥序列化为PEM格式
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# 保存公钥到文件
with open('public_key.pem', 'wb') as f:
    f.write(public_pem)

print("私钥和公钥文件已生成。")
