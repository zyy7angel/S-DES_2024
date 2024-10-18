import tkinter as tk
import tkinter.messagebox as messagebox

# 置换表
IP = [2, 6, 3, 1, 4, 8, 5, 7]  # IP置换表
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]  # IP逆置换表
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]  # 选择置换1表
P8 = [6, 3, 7, 4, 8, 5, 10, 9]  # 选择置换2表
P4 = [2, 4, 3, 1]  # 选择置换3表
EP = [4, 1, 2, 3, 2, 3, 4, 1]  # EP扩展置换表

# S盒表
S_BOX = [
    [
        [1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]
    ],
    [
        [0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]
    ]
]

# 生成子密钥
def get_K(key):
    # print("主密钥")
    # print(key)

    # P10置换
    key_P10 = [key[i-1] for i in P10]

    # print("P10置换")
    # print(key_P10)

    L = key_P10[:5]
    R = key_P10[5:]

    # 生成子密钥
    K = []

    for i in range(2):
        # # 循环左移:第一轮左移一位，第二轮左移两位
        # L.append(L.pop(0))  # a=L.pop(0)：将列表L的第一个元素移除，L.append(a)：将a添加到L的末尾；
        # R.append(R.pop(0))

        if i == 0:
            L.append(L.pop(0))  # a=L.pop(0)：将列表L的第一个元素移除，L.append(a)：将a添加到L的末尾；
            R.append(R.pop(0))
        else:
            L.append(L.pop(0))  # a=L.pop(0)：将列表L的第一个元素移除，L.append(a)：将a添加到L的末尾；
            R.append(R.pop(0))
            L.append(L.pop(0))  # a=L.pop(0)：将列表L的第一个元素移除，L.append(a)：将a添加到L的末尾；
            R.append(R.pop(0))

        # 合并左右半部分
        L_R = L + R

        # P8置换
        k = [L_R[i-1] for i in P8]

        # 添加子密钥
        K.append(k)

        #左移后的L、R继续作为下一轮初始值，得到K1、K2，均为10位

    return K

# S盒替代
def s_box_substitution(input):
    output = []
    S1 = input[:4] #左半
    S2 = input[4:] #右半

    # print("S1左半")
    # print(S1)
    # print("S2右半")
    # print(S2)

    # 在S1、S2中，分别将第1位与第4位结合，形成2位代表S盒的行号，分别将第2位与第3位结合，形成2位代表S盒的列号，从而得到S盒的输出
    S1_row = int(str(S1[0]) + str(S1[3]), 2)
    S1_col = int(str(S1[1]) + str(S1[2]), 2)

    S2_row = int(str(S2[0]) + str(S2[3]), 2)
    S2_col = int(str(S2[1]) + str(S2[2]), 2)

    S1_output = S_BOX[0][S1_row][S1_col]
    S2_output = S_BOX[1][S2_row][S2_col]

    output.extend(format(S1_output, '02b'))  # extend区别于append:传入是整个列表时，将整个列表的元素一一添加在末尾，而不是将整个列表视作一个元素添加
    output.extend(format(S2_output, '02b'))

    return output

"""S-DES加密算法"""
def s_des_encrypt(text, key):
    # 输入明文为8位二进制字符串，主密钥为10位

    # 将明文和密钥转换为列表形式：list()将字符串转化为列表，更有利于对每一位进行操作
    text = list(text)
    key = list(key)

    # 初始IP置换
    text_IPreplace = [text[i-1] for i in IP]

    # print("初始IP置换")
    # print(text_IPreplace)

    #左半、右半
    L =  text_IPreplace[:4]
    R =  text_IPreplace[4:]


    # 生成子密钥
    K = get_K(key)

    # print("子密钥")
    #
    # print(K)

    # 迭代加密（S-DES只有两轮）
    for i in range(2):

        # print("左半")
        # print(L)
        # print("右半")
        # print(R)

        # F函数运算
        # (1)右半部分R进行EP扩展置换
        E_R = [R[j-1] for j in EP] #将4位扩展为8位

        # print("右半扩展")
        # print(E_R)

        # (2)扩展后的E_R与子密钥K按位异或,输出8位
        E_R_xor_K = [int(E_R[j]) ^ int(K[i][j]) for j in range(8)]

        # print("扩展后异或")
        # print(E_R_xor_K)

        # (3)S盒替代,返回4位
        s_box_replace = s_box_substitution(E_R_xor_K)

        # print("S盒后")
        # print(s_box_replace)

        # (4)P置换
        p_replace = [s_box_replace[j-1] for j in P4]

        # print("P4置换")
        # print(p_replace)

        # 左半部分L与F函数的结果按位异或
        new_R = [int(L[j]) ^ int(p_replace[j]) for j in range(4)]

        if i == 0:
            # 更新左右半部分
            L = R
            R = new_R
        else:
            L =new_R

        # print("下一轮输入")
        # print(L+R)


    # 结合左右半部分
    L_R = L + R

    # print("F函数后")
    # print(L_R)

    # 初始置换逆置换
    L_R_IP_inv = [L_R[i-1] for i in IP_inv]

    # print("逆置换后")
    # print(L_R_IP_inv)

    # 将结果列表转换为字符串
    cipher_text = ''.join([str(bit) for bit in L_R_IP_inv])

    return cipher_text

"""S-DES解密算法"""
def s_des_decrypt(text, key):
    # 输入明文为8位二进制字符串，主密钥为10位

    # 将明文和密钥转换为列表形式：list()将字符串转化为列表，更有利于对每一位进行操作
    text = list(text)
    key = list(key)

    # 初始IP置换
    text_IPreplace = [text[i - 1] for i in IP]

    # print("初始IP置换")
    # print(text_IPreplace)

    # 左半、右半
    L = text_IPreplace[:4]
    R = text_IPreplace[4:]

    # 生成子密钥
    K = get_K(key)

    # print("子密钥")
    #
    # print(K)

    # 迭代加密（S-DES只有两轮）
    for i in range(2):
        # print("左半")
        # print(L)
        # print("右半")
        # print(R)

        # F函数运算
        # (1)右半部分R进行EP扩展置换
        E_R = [R[j - 1] for j in EP]  # 将4位扩展为8位

        # print("右半扩展")
        # print(E_R)

        # (2)扩展后的E_R与子密钥K按位异或,输出8位
        E_R_xor_K = [int(E_R[j]) ^ int(K[1-i][j]) for j in range(8)]

        # print("扩展后异或")
        # print(E_R_xor_K)

        # (3)S盒替代,返回4位
        s_box_replace = s_box_substitution(E_R_xor_K)

        # print("S盒后")
        # print(s_box_replace)

        # (4)P置换
        p_replace = [s_box_replace[j - 1] for j in P4]

        # print("P4置换")
        # print(p_replace)

        # 左半部分L与F函数的结果按位异或
        new_R = [int(L[j]) ^ int(p_replace[j]) for j in range(4)]

        # print("左半与F函数异或后")
        # print(new_R)

        # 更新左右半部分
        if i == 0:
            L = R
            R = new_R
        else:

            L=new_R

        # print("下一轮输入")
        # print(L + R)

    # 结合左右半部分
    L_R = L + R

    # print("F函数后")
    # print(L_R)

    # 初始置换逆置换
    L_R_IP_inv = [L_R[i - 1] for i in IP_inv]

    # print("逆置换后")
    # print(L_R_IP_inv)

    # 将结果列表转换为字符串
    cipher_text = ''.join([str(bit) for bit in L_R_IP_inv])

    return cipher_text


# # 测试
# ciphertext = "00001111"
# key = "1111111111"
# plaintext = s_des_decrypt(ciphertext, key)
# print("明文：" + plaintext) #0001 0110

"""ASCALL加密"""
def ascii_encrypt(input_string, key):
    encrypted_result = ""
    encrypted_result_char = ""

    # 将输入的每个字符转换为二进制，再加密
    for char in input_string:
        binary_data = format(ord(char), '08b')  # 将字符转换为8位二进制
        encrypted_data = s_des_encrypt(binary_data, key)  # 对二进制数据加密
        encrypted_result += encrypted_data  # 结果拼接

    # 将加密后的二进制数据转换为字符形式
    for i in range(0, len(encrypted_result), 8):  # 每8位对应一个字符
        binary_data = encrypted_result[i:i + 8]
        encrypted_char = chr(int(binary_data, 2))  # 二进制转为整数再转为字符
        encrypted_result_char += encrypted_char  # 拼接加密后的字符

    return encrypted_result_char


def ascii_decrypt(encrypted_string, key):
    decrypted_result = ""

    # 逐个字符处理，转换为二进制形式
    for char in encrypted_string:
        binary_data = format(ord(char), '08b')  # 将字符转换为8位二进制
        decrypted_data = s_des_decrypt(binary_data, key)  # 解密二进制数据
        decrypted_result += chr(int(decrypted_data, 2))  # 解密后转为字符

    return decrypted_result


# 检查是否为 ASCII 字符
def is_ascii(s):
    return all((ord(c)>64 and ord(c) < 123) for c in s)

# GUI 界面设计
def create_gui():
    # 初始化窗口
    window = tk.Tk()
    window.title("S-DES加密解密工具")
    window.geometry("500x400")

    # 标签和输入框：明文/密文
    label_input = tk.Label(window, text="输入明文或密文：")
    label_input.pack(pady=5)
    input_text = tk.Entry(window, width=50)
    input_text.pack(pady=5)

    # 标签和输入框：密钥
    label_key = tk.Label(window, text="输入密钥(10位二进制)：")
    label_key.pack(pady=5)
    key_text = tk.Entry(window, width=50)
    key_text.pack(pady=5)

    # 显示加密或解密结果的文本框
    output_label = tk.Label(window, text="输出结果：")
    output_label.pack(pady=5)
    output_text = tk.Text(window, height=5, width=50)
    output_text.pack(pady=5)

    # 按钮功能：加密
    def encrypt():
        plaintext = input_text.get()
        key = key_text.get()

        # 验证输入是否合法
        if len(plaintext) == 0 or len(key) != 10:
            messagebox.showerror("输入错误", "请输入明文和10位密钥")
            return

        cipher_text = s_des_encrypt(plaintext, key)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, cipher_text)

    # 按钮功能：解密
    def decrypt():
        ciphertext = input_text.get()
        key = key_text.get()

        # 验证输入是否合法
        if len(ciphertext) == 0 or len(key) != 10:
            messagebox.showerror("输入错误", "请输入密文和10位密钥")
            return

        plain_text = s_des_decrypt(ciphertext, key)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, plain_text)

    # 按钮功能：ASCII加密
    def ascii_encrypt_action():
        plaintext = input_text.get()
        key = key_text.get()

        # 验证输入是否合法
        if len(plaintext) == 0 or len(key) != 10:
            messagebox.showerror("输入错误", "请输入明文和10位密钥")
            return

        cipher_text = ascii_encrypt(plaintext, key)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, cipher_text)

    # 按钮功能：ASCII解密
    def ascii_decrypt_action():
        ciphertext = input_text.get()
        key = key_text.get()

        # 验证输入是否合法
        if len(ciphertext) == 0 or len(key) != 10:
            messagebox.showerror("输入错误", "请输入密文和10位密钥")
            return

        plain_text = ascii_decrypt(ciphertext, key)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, plain_text)

    # 加密按钮
    encrypt_button = tk.Button(window, text="加密", command=encrypt)
    encrypt_button.pack(side=tk.LEFT, padx=20, pady=10)

    # 解密按钮
    decrypt_button = tk.Button(window, text="解密", command=decrypt)
    decrypt_button.pack(side=tk.LEFT, padx=20, pady=10)

    # ASCII加密按钮
    ascii_encrypt_button = tk.Button(window, text="ASCII加密", command=ascii_encrypt_action)
    ascii_encrypt_button.pack(side=tk.LEFT, padx=20, pady=10)

    # ASCII解密按钮
    ascii_decrypt_button = tk.Button(window, text="ASCII解密", command=ascii_decrypt_action)
    ascii_decrypt_button.pack(side=tk.LEFT, padx=20, pady=10)

    # 运行主循环
    window.mainloop()

# 运行程序
if __name__ == "__main__":
    create_gui()
