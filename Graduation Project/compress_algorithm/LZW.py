import pickle
import os
import time
from collections import OrderedDict
# 最近最少使用缓存
class LRUDict:
    def __init__(self, capacity):
        self.capacity = capacity
        # capacity 作为缓存最大容量
        self.cache = OrderedDict()
    #     保存缓存的键值对，orderdict 是字典，他存储键值对被插入的顺序

    # 用于获取缓存中指定键的值。
    def get(self, key):
        if key not in self.cache:
            return None
        # 使用 pop 方法从缓存中移除该键值对
        value = self.cache.pop(key)
        # 然后将该键值对重新添加到缓存中
        # 最近访问的键值对总是在 OrderedDict 的末尾
        self.cache[key] = value
        return value
    # 用于将一个键值对添加到缓存中。
    def put(self, key, value):
        if key in self.cache:
            self.cache.pop(key)
        # 键不存在并且缓存已满
        elif len(self.cache) == self.capacity:
            self.cache.popitem(last=False)
        #     移除最旧的键值对
        self.cache[key] = value
#         将新的键值对添加到缓存中。

# 压缩文件
def compress_file(input_file_path, output_file_path,max_dict_size=4096):
    with open(input_file_path, 'rb') as f:
        data = f.read()
    #     输入文件的所有内容储存在data变量中

    # 设置字典初始大小为256（一字节可以表示256个可能的值，表示所有的单字节值）
    # 创建字典的目的：根据一个字节串（键）快速查找到对应的字节值（值）。
    dict_size = 256
    # dictionary = LRUDict(max_dict_size)
    # for i in range(256):
    #     dictionary.put(bytes([i]), i)
    dictionary = {bytes([i]): i for i in range(dict_size)}
    # bytes([i])会创建一个只有一个字节的字节串，字节值为i，i的值是随机生成的

    w = bytes()
    # w 用于存储当前的输入序列
    result = []
    # 定义了一个空的列表 result。这个列表用于存储压缩结果
    # 遍历输入数据data的每个字节
    for c in data:
        # 取c值对应的字符串
        c = bytes([c])
        # 尝试在字典中查找当前序列 w + 当前字符c
        wc = w + c
        # 如果找到，则下一轮从w+c开始
        # if dictionary.get(wc) is not None:
        #     w = wc
        # else:
        #     result.append(dictionary.get(w))
        #     dictionary.put(wc, len(dictionary.cache))
        #     w = c

        if wc in dictionary:
            w = wc
        # 如果没找到，将w的字典值加到结果列表result中，把新序列wc加到字典中，把当前字节c设置为新的字节序列w
        else:
            result.append(dictionary[w])
            if dict_size < max_dict_size:
                dictionary[wc] = dict_size
                dict_size += 1
            w = c

    # 如果w非空，就把w的字典值添加到结果中。这是因为输入数据已经处理完毕，但是w可能还包含未处理的数据。
    if w:
        # dictionary_value = dictionary.get(w)

        # result.append(dictionary.get(w))
        result.append(dictionary[w])

    # print(dictionary)

    with open(output_file_path, 'wb') as f:
        # pickle.dump(result, f)
        for num in result:
            # bytes_to_write = num.to_bytes((num.bit_length() + 7) // 8, 'big')  # Converts int to bytes
            bytes_to_write = num.to_bytes(2,'big')
            f.write(bytes_to_write)
    #   将Python对象转化为二进制格式

    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(output_file_path)

    print(f'Current compress file: {input_file_path}')
    print(f'Original file size: {original_size} bytes')
    print(f'Compressed file size: {compressed_size} bytes')
    print(f'Compression ratio: {compressed_size / original_size:.2f}')

# 解压文件
def decompress_file(input_file_path, output_file_path):
    # 打开压缩之后的文件，用load函数把压缩的数据加载到变量compressed中
    with open(input_file_path, 'rb') as f:
        # compressed = pickle.load(f)
        compressed = []
        while byte := f.read(2):
            compressed.append(int.from_bytes(byte, 'big'))

            # 创建一个反向字典，由字节的值找对应的字节串
    dict_size = 256
    dictionary = {i: bytes([i]) for i in range(dict_size)}
    # 从compressed中取出第一个字节值并转换为字节串，存储到变量w中
    w = bytes([compressed.pop(0)])
    result = [w]
    for k in compressed:
        if k in dictionary:
            # 当前正在处理的压缩编码 k 的字节串。
            entry = dictionary[k]
            # print(entry)
        elif k == dict_size:
            entry = w + w[0:1]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.append(entry)
        # 在字典中添加一个新的条目，其键是字典的当前大小，值是w与entry的第一个字节相连的字节串。
        dictionary[dict_size] = w + entry[0:1]
        dict_size += 1
        w = entry

    with open(output_file_path, 'wb') as f:
        f.write(b''.join(result))

# 验证原始文件和压缩文件是否一致
def verify_file(original_file_path, decompressed_file_path):
    with open(original_file_path, 'rb') as f1, open(decompressed_file_path, 'rb') as f2:
        original_content = f1.read()
        decompressed_content = f2.read()

    if original_content == decompressed_content:
        print("Verification successful: the original file and the decompressed file are identical.")

    else:
        print("Verification failed: the original file and the decompressed file are different.")


print('-----------------This is LZW compress algorithm-----------------')

# How to use:

start_time = time.time()
compress_file('../dataset/text1.txt', 'LZW_compressed.bin')
end_time = time.time()
print('-----------------LZW compress time-----------------')
execution_time = end_time - start_time
print("Compression time:", execution_time, "seconds")

start_time = time.time()
decompress_file('LZW_compressed.bin', 'LZW_decompressed.txt')
end_time = time.time()
print('-----------------LZW decompress time-----------------')
execution_time = end_time - start_time
print("Decompression time:", execution_time, "seconds")



# 使用该函数来验证：

verify_file('../dataset/text1.txt', 'LZW_decompressed.txt')

