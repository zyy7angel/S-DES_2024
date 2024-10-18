import S_DES
import threading
import time

def brute_force(cipher_text_pairs):
    # 密钥空间大小
    key_space = 1024
    found_keys = []
    first_key_time = None  # 用于记录找到第一个密钥的时间
    first_key_found_event = threading.Event()  # 事件对象用于记录是否找到第一个密钥

    def try_keys(start, end):
        nonlocal first_key_time
        for key in range(start, end):
            # 将密钥转换为10位的二进制格式
            key_bin = format(key, '010b')
            # 检查该密钥是否适用于所有的明密文对
            all_match = True
            for cipher_text, known_plain_text in cipher_text_pairs:
                decrypted_text = S_DES.s_des_decrypt(cipher_text, key_bin)
                if decrypted_text != known_plain_text:
                    all_match = False
                    break
            if all_match:
                found_keys.append(key)
                # 如果这是找到的第一个密钥，记录时间
                if not first_key_found_event.is_set():
                    first_key_time = time.perf_counter()
                    first_key_found_event.set()  # 标记已经找到第一个密钥

    # 记录开始时间
    start_time = time.perf_counter()

    # 启动多个线程
    threads = []
    num_threads = 4  # 使用4个线程
    keys_per_thread = key_space // num_threads
    for i in range(num_threads):
        start = i * keys_per_thread
        end = (i + 1) * keys_per_thread
        t = threading.Thread(target=try_keys, args=(start, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()  # 等待所有线程完成

    # 记录结束时间
    end_time = time.perf_counter()

    if found_keys:
        print(f"Found {len(found_keys)} key(s): {[format(key, '010b') for key in found_keys]}")
        if first_key_time:
            print(f"Time to find the first key: {first_key_time - start_time:.4f} seconds")
    else:
        print("No key found")

    print(f"Total brute force time: {end_time - start_time:.4f} seconds")

    return found_keys

# 假设已经有一个明密文对列表
cipher_text_pairs = [
    ("11111111", "00001111"),  # 第一个密文和对应的明文
]

brute_force(cipher_text_pairs)
