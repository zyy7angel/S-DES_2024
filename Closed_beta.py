import S_DES
from collections import defaultdict

def find_key_collisions(plain_text):
    # 密钥空间大小
    key_space = 1024  # 10位二进制密钥的所有可能性
    collision_dict = defaultdict(list)  # 存储密文和对应的密钥列表

    # 遍历所有可能的密钥
    for key in range(key_space):
        # 将密钥转换为10位二进制格式
        key_bin = format(key, '010b')
        # 使用该密钥加密明文
        cipher_text = S_DES.s_des_encrypt(plain_text, key_bin)
        # 将加密结果存储在字典中，密文作为键，密钥作为值
        collision_dict[cipher_text].append(key_bin)

    # 查找有冲突的密文
    collisions = {cipher: keys for cipher, keys in collision_dict.items() if len(keys) > 1}

    # 输出冲突结果
    if collisions:
        print("Found key collisions!")
        for cipher, keys in collisions.items():
            print(f"Cipher Text: {cipher} - Keys: {keys}")
    else:
        print("No key collisions found.")

    return collisions

# 示例明文（可以替换为其他明文进行测试）
plain_text = "00001111"

# 查找密钥冲突
find_key_collisions(plain_text)
