import os
import time
import json
class TrieNode:
    def __init__(self, label=None, value=None):

        self.label = label
        self.value = value
        self.children = {}

class Trie:
    def __init__(self, unique_chars):
        self.root = TrieNode()
        self.index = len(unique_chars)
        for i, char in enumerate(unique_chars):
            self.insert(char, i)

    def insert(self, string, value):
        node = self.root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode(label=char, value=value)
                node = node.children[char]
                value += 1
            else:
                node = node.children[char]
        return value
        # new_node = TrieNode(label=char, value=value)
        # self.root.children[char] = new_node

    def search(self, string):
        node = self.root
        for char in string:
            if char in node.children:
                node = node.children[char]
            else:
                return None
        return node.value
        # return self.root.children.get(char)

    def serialize(self):
        def node_to_dict(node):
            return {
                'label': node.label,
                'value': node.value,
                'children': {k: node_to_dict(v) for k, v in node.children.items()}
            }

        return json.dumps(node_to_dict(self.root), ensure_ascii=False)

    def deserialize(s):
        def dict_to_node(d):
            node = TrieNode(label=d['label'], value=d['value'])
            node.children = {k: dict_to_node(v) for k, v in d['children'].items()}
            return node

        trie = Trie([])
        trie.root = dict_to_node(json.loads(s))
        return trie
    # def search_by_index(self, index):
    #     for child in self.root.children.values():
    #         if child.value == bin(index)[2:]:
    #             return child.label

# 使用这个方法来保存 Trie 到文件
def save_trie_to_file(trie, file_path):
    with open(file_path, 'w') as f:
        f.write(trie.serialize())
# 使用这个方法来从文件中加载 Trie
def load_trie_from_file(file_path):
    with open(file_path, 'r') as f:
        return Trie.deserialize(f.read())
# 读取文件，获取所有不同的字符
def count_unique_chars(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return sorted(list(set(content)))
# 自定义一个转换函数，当转换整数到二进制字符串时，保持二进制字符串的长度。这可以通过在转换后的字符串前面添加足够数量的'0'来实现

def int_to_bin(integer, length):
    # Convert integer to binary and remove '0b' prefix
    bin_str = bin(integer)[2:]
    # Pad binary string with zeros to the left
    return bin_str.zfill(length)

def print_trie(node, depth=0, prefix=""):
    # 打印当前节点
    if node.value is not None:
        print(f"{' ' * depth}{prefix}: {node.value}")
        # print(f"{prefix}: {node.value}")
    # 递归打印子节点
    for char, child in node.children.items():
        print_trie(child, depth + 1, prefix + char)

# def write_to_file(filename, data):
#     with open(filename, 'w') as f:
#         for item in data:
#             f.write(int(item, 2).to_bytes((len(item) + 7) // 8, byteorder='big'))

            # f.write("%s\n" % item)

def file_size(filename):
    return os.stat(filename).st_size

def compression_rate(original_size, compressed_size):
    return (original_size - compressed_size) / original_size


# LZW压缩
def lzw_compression(input_file_path,output_file_path):
    unique_chars = count_unique_chars(input_file_path)
    trie = Trie(unique_chars)
    result = []

    # 按老师新改的
    #确定初始编码长度
    length = len(bin(len(unique_chars) - 1)[2:])
    max_length = length
    # 判断需不需要增加码字长度，比如到了 8 才需要增加一位
    increase_length = False

    with open(input_file_path, 'r') as f:
        s = f.read(1)
        c = f.read(1)
        while c:
            if trie.search(s+c) is not None:
                s = s+c
            else:
                # 打印正在处理的字符串和它的编码
                # print(f"Current string: {s}, Its binary code: {int_to_bin(trie.search(s),max_length)}")
                # 按老师新改的
                # 将 trie.search(s) 的值转换为固定长度的二进制字符串
                result.append(int_to_bin(trie.search(s), max_length))

                # 检查是否需要增加编码长度
                if len(bin(trie.index)[2:]) > length:  # check if we need to increase the encoding length
                    # 一旦Trie的大小（即当前字符串的索引值）的二进制表示长度超过了当前的码字长度，就需要增加码字长度
                    increase_length = True
                    length += 1
                    max_length = length

                # print(f"New substring added to the Trie: '{s + c}' with index {trie.index}")  # 这里添加了打印语句

                trie.insert(s+c, trie.index)
                trie.index += 1


            # 如果 increase_length 标记为 True，那么增加编码长度
            #     if increase_length:
                   # length += 1
                   # max_length = length
                   # increase_length = False

                s = c
            c = f.read(1)

        # 按老师新改的
        result.append(int_to_bin(trie.search(s),max_length))


        with open(output_file_path, 'wb') as f:

            #     # f.write(length.to_bytes(1, byteorder='big'))  # 写入编码的长度

            for num in result:
                # f.write(num)

                f.write(int(num, 2).to_bytes((len(num) + 7) // 8, byteorder='big'))  # 使用二进制写入
        #         # 按老师新改的
        #         bit_string = int_to_bin(num, max_length)
        #         bytes_to_write = int(num, 2).to_bytes((len(num) + 7) // 8, 'big')  # Converts string to bytes
        # #
        #         f.write(bytes_to_write)

        # 在压缩的最后保存 Trie
        # trie_file_path = 'trie.json'  # 选择路径和文件名
        # save_trie_to_file(trie, trie_file_path)

    return result


def lzw_decompression(original_file_path, input_file_path, output_file_path, ):
    # 初始化字典
    unique_chars = count_unique_chars(original_file_path)
    print(f"Unique Characters: {unique_chars}")
    dict_size = len(unique_chars)
    dictionary = {i: char for i, char in enumerate(unique_chars)}

    # print(f"Unique Characters: {unique_chars},Code:{}")

    # 初始化其他参数
    string = ""
    result = []

    # 确定初始码字长度
    length = len(bin(len(unique_chars) - 1)[2:])
    print(length)
    max_length = length

    with open(input_file_path, 'rb') as f:
        data = f.read()


    binary_string = [format(b, '08b') for b in data]
    binary_string = ''.join(binary_string)
    # print([item for item in binary_string])

    i = 0
    while i < len(binary_string):
        # 检查是否需要增加码字长度
        if len(bin(dict_size)[2:]) > length:  # check if we need to increase the encoding length
            length += 1
            max_length = length
        # 读取固定长度的码字
        # 检查剩余的位数是否足够
        if i + max_length > len(binary_string):
            # If not, use all remaining bits to form a codeword
            code = binary_string[i:]
            i = len(binary_string)
        else:
            # Otherwise, use the maximum length to form a codeword
            code = binary_string[i][max_length:]
            # code = binary_string[i:i + max_length]
            i += max_length
        # if len(binary_string[i]) < max_length:
        #     break
        # code = binary_string[i][max_length:]

        # 解码
        if string == "":
            string = dictionary[int(code, 2)]
            result.append(string)
        else:
            if int(code, 2) in dictionary:  # if the new code is in the dictionary
                entry = dictionary[int(code, 2)]
            else:
                entry = string + string[0]

            # print(f"Current code: {code}, Its corresponding string: {entry}")  # 打印当前读取的码字和它对应的字符串

            result.append(entry)
            dictionary[dict_size] = string + entry[0]
            dict_size += 1
            string = entry
        # i += 1
        i += max_length


    with open(output_file_path, 'w') as f:
        f.write(''.join(result))

def verify_file(original_file_path, decompressed_file_path):
    with open(original_file_path, 'rb') as f1, open(decompressed_file_path, 'rb') as f2:
        original_content = f1.read()
        decompressed_content = f2.read()

    if original_content == decompressed_content:
        print("Verification successful: the original file and the decompressed file are identical.")

    else:
        print("Verification failed: the original file and the decompressed file are different.")










input_file_path = '../dataset/lzw_example'
output_file_path = '../outcomes/Trie_compressed.bin'
start_time = time.time()
lzw_compression(input_file_path,output_file_path)
end_time = time.time()
print('-----------------LZW compress time-----------------')
execution_time = end_time - start_time
print("Compression time:", execution_time, "seconds")


print(lzw_compression(input_file_path,output_file_path))

# 计算压缩前后的文件大小

original_size = file_size(input_file_path)
compressed_size = file_size('../outcomes/Trie_compressed.bin')
print(f'Current compress file: {input_file_path}')
print(f'Original file size: {original_size} bytes')
print(f'Compressed file size: {compressed_size} bytes')

# 计算压缩率
rate = compression_rate(original_size, compressed_size)
print(f"Compression rate: {rate*100:.2f}%")
#
# lzw_decompression('lzw_example','Trie_compressed.bin','Trie_decompressd.txt')


# 使用该函数来验证：

# verify_file('lzw_example', 'Trie_decompressd.txt')

