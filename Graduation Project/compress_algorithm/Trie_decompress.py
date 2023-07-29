import os
import time

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
        if type(string) is int:
            string = self.int_to_bin_string(string)  # 添加这行来将整数转换为二进制字符串
        for char in string:
            char_index = self.char_to_index(char)
            if node.children[char_index] is None:
                return False
            node = node.children[char_index]
        return node.char if node else None

    def char_to_index(self,char):
        return {
            '0': 0,
            '1': 1,
            '2': 2,
            '3': 3
        }[char]
    def int_to_bin_string(self,number):
        return format(number, 'b')

        # return self.root.children.get(char)

# 使用这个方法来保存 Trie 到文件
def save_trie_to_file(trie, file_path):
    with open(file_path, 'w') as f:
        f.write(trie.serialize())

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

def file_size(filename):
    return os.stat(filename).st_size

def compression_rate(original_size, compressed_size):
    return (original_size - compressed_size) / original_size


def count_unique_chars(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    return sorted(list(set(content)))


def lzw_decompression(original_file_path,input_file_path,output_file_path,):
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
    # binary_string = ''.join(binary_string)


    i = 0
    while i < len(binary_string):

        # 读取固定长度的码字
        code = binary_string[i][-max_length:]

        # code = binary_string[i:i + max_length]

        # 解码
        if string == "":
            # 将二进制字符串转换为整数。然后，该整数作为键用于从dictionary中检索与该码字对应的字符或字符串，
            string = dictionary[int(code, 2)]
            result.append(string)
        else:
            if int(code, 2) in dictionary:  # if the new code is in the dictionary
                # 如果码字在字典中，我们将码字转换为对应的字符或字符串，存储在entry变量中
                entry = dictionary[int(code, 2)]
            else:
                # 如果新读取的码字不在字典中，那么我们假设这个码字对应的字符串是当前字符串string后面跟着其自身的第一个字符
                entry = string + string[0]

                # dictionary[dict_size] = string + entry[0]


            # string：当前正在处理的字符串，entry：在解码新的码字时使用的临时变量
            # print(f"Current code: {code}, Its corresponding string: {entry}")  # 打印当前读取的码字和它对应的字符串
            result.append(entry)
            dictionary[dict_size] = string + entry
            dict_size += 1
            print(f"New entry added to dictionary: {string + entry[0]}, dictionary size: {dict_size}")
            string = entry

            # 将新的字符串添加到字典中。

        i += 1
        # i += max_length
        # 检查是否需要增加码字长度
        if len(bin(dict_size)[2:]) > length:  # check if we need to increase the encoding length
            length += 1
            max_length = length
        # for key, value in dictionary.items():
        #     print(f"Character: {value}, Code: {key}")

    with open(output_file_path, 'wb') as f:
        f.write(''.join(result).encode())
    # with open(output_file_path, 'w') as f:
    #     f.write(''.join(result))



def verify_file(original_file_path, decompressed_file_path):
    with open(original_file_path, 'rb') as f1, open(decompressed_file_path, 'rb') as f2:
        original_content = f1.read()
        decompressed_content = f2.read()

    if original_content == decompressed_content:
        print("Verification successful: the original file and the decompressed file are identical.")

    else:
        print("Verification failed: the original file and the decompressed file are different.")


lzw_decompression('../dataset/lzw_example', '../outcomes/Trie_compressed.bin', '../outcomes/Trie_decompressd.txt')
# verify_file('test.txt', 'Trie_decompressd.txt')