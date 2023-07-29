# import heapq
# import os
# import pickle
# import time
#
# class TrieNode:
#     def __init__(self, char=None):
#         self.char = char
#         self.children = {}
#         self.end_of_word = False
#         self.index = None
# class Trie:
#     def __init__(self):
#         self.root = TrieNode()
#         self.index = 256
#
#     def insert(self, word):
#         node = self.root
#         for char in word:
#             if char in node.children:
#                 node = node.children[char]
#             else:
#                 new_node = TrieNode(char)
#                 node.children[char] = new_node
#                 node = new_node
#         node.end_of_word = True
#         node.index = self.index
#         self.index += 1
#
#     def search(self, word):
#         node = self.root
#         for char in word:
#             if char in node.children:
#                 node = node.children[char]
#             else:
#                 return None
#         if node.end_of_word:
#             return node.index
#         return None
#
# def compress_file(input_file_path, output_file_path):
#     with open(input_file_path, 'rb') as f:
#         data = f.read()
#
#     trie = Trie()
#     for i in range(256):
#         trie.insert(bytes([i]))
#
#     w = bytes()
#     result = []
#     for c in data:
#         c = bytes([c])
#         wc = w + c
#         if trie.search(wc) is not None:
#             w = wc
#         else:
#             result.append(trie.search(w))
#             trie.insert(wc)
#             w = c
#
#     if w:
#         result.append(trie.search(w))
#
#     with open(output_file_path, 'wb') as f:
#         pickle.dump(result, f)
#
#     original_size = os.path.getsize(input_file_path)
#     compressed_size = os.path.getsize(output_file_path)
#
#     print(f'Current compress file: {input_file_path}')
#     print(f'Original file size: {original_size} bytes')
#     print(f'Compressed file size: {compressed_size} bytes')
#     print(f'Compression ratio: {compressed_size / original_size:.2f}')
#
# def decompress_file(input_file_path, output_file_path):
#     with open(input_file_path, 'rb') as f:
#         compressed = pickle.load(f)
#
#     trie = Trie()
#     for i in range(256):
#         trie.insert(bytes([i]))
#
#     w = bytes([compressed.pop(0)])
#     result = [w]
#     for k in compressed:
#         entry = trie.root
#         for _ in range(k):
#             entry = next(iter(entry.children.values()))
#         result.append(entry.char)
#         trie.insert(w + entry.char[0:1])
#         w = entry.char
#
#     with open(output_file_path, 'wb') as f:
#         f.write(b''.join(result))
#
# # How to use:
# start_time = time.time()
# compress_file('string2.txt', 'LZW_compressed.bin')
# end_time = time.time()
# execution_time = end_time - start_time
# print("Compression time:", execution_time, "seconds")
#
# start_time = time.time()
# decompress_file('LZW_compressed.bin', 'LZW_decompressed.txt')
# end_time = time.time()
# execution_time = end_time - start_time
# print("Decompression time:", execution_time, "seconds")


import pickle
import os

def count_unique_chars(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return len(set(content))

file_path = 'your_file_path'
unique_chars_count = count_unique_chars(file_path)
# trie = Trie(unique_chars_count)

# Trie Node定义
class TrieNode:
    def __init__(self,value=None):
        self.children = {}     #[]
        self.value = value     #（code lenth）（store string）
        # （存储分支 label）
        # self.isEndOfWord = False
# (go through file,统计出现的不同字符，再把这个值代替 256)使用列表存储不同的字符，并获得的他的大小。
class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.index = unique_chars_count
        for i in range(unique_chars_count):
            self.insert(chr([i]), i)

    def insert(self, word,value):
        current = self.root
        for letter in word:
            if letter not in current.children:  # 如果当前字符不在子节点中，就新建一个子节点，并设置其编码值
                current.children[letter] = TrieNode(self.index)
                self.index += 1
            current = current.children[letter]
            # node = current.children.get(letter)
            # if node is None:
            #     node = TrieNode()
            #     current.children[letter] = node
            # current = node
        current.isEndOfWord = True
        current.value = self.index
        self.index += 1
        return self.index - 1

    def search(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:  # 如果当前字符不在子节点中，说明单词不存在
                return None
            current = current.children[letter]
            return current.value  # 返回单词的最后一个字符对应的编码值
        #     node = current.children.get(letter)
        #     if node is None:
        #         return None
        #     current = node
        # return current.value if current.isEndOfWord else None
        # return current.isEndOfWord

    def search_by_index(self, index):
        # Note: this function is not optimized
        def _search(node):
            if node.value == index:
                return node
            for child in node.children.values():
                result = _search(child)
                if result is not None:
                    return result
            return None

        node = _search(self.root)
        if node is not None:
            word = []
            while node is not self.root:
                word.append(next(key for key, child in node.parent.children.items() if child is node))
                node = node.parent
            return ''.join(reversed(word))  # 将字节串转换为字符串
            # return bytes(reversed(word))

# 压缩文件
def compress_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f:
        data = f.read()

    trie = Trie()
    # dictionary = {}
    # for i in range(256):
    #     dictionary[i] = bytes([i])
    #     trie.insert(bytes([i]),)

    w = bytes()
    result = []
    for c in data:
        c = bytes([c])
        wc = w + c
        if trie.search(wc) is not None:
            w = wc
        else:
            result.append(trie.insert(w, trie.index))
            w = c
            # index = trie.insert(w)
            # result.append(index)
            # dictionary[index] = w
            # w = c


    if w:
        result.append(trie.insert(w,trie.index))

    with open(output_file_path, 'wb') as f:
        pickle.dump(result, f)

    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(output_file_path)

    print(f'Original file size: {original_size} bytes')
    print(f'Compressed file size: {compressed_size} bytes')
    print(f'Compression ratio: {compressed_size / original_size:.2f}')

# 解压文件，由于Trie树是一种非对称的数据结构，解压还是需要使用字典
def decompress_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as f:
        compressed = pickle.load(f)
    # dict_size = 256
    # dictionary = {i: bytes([i]) for i in range(dict_size)}
    trie = Trie()
    w = trie.search_by_index(compressed.pop(0))
    result = [w]
    for k in compressed:
        entry = trie.search_by_index(k)
        if entry is not None:
            result.append(entry)
            trie.insert(w + entry[0:1], trie.index)
            w = entry
        else:
            raise ValueError('Bad compressed k: %s' % k)

        # if k in dictionary:
        #     entry = dictionary[k]
        # elif k == dict_size:
        #     entry = w + w[0:1]
        # else:
        #     raise ValueError('Bad compressed k: %s' % k)
        # result.append(entry)
        # # dictionary[dict_size] = w + entry[0:1]
        # dictionary[len(dictionary)] = w + entry[0:1]
        # # dict_size += 1
        # w = entry

    with open(output_file_path, 'wb') as f:
        f.write(b''.join(result))

# 调用函数
compress_file('../dataset/string2.txt', 'compressed.dat')
decompress_file('compressed.dat', 'decompressed.txt')
