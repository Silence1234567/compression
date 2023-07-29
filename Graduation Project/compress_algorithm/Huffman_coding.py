import heapq
import os
from collections import defaultdict
from bitarray import bitarray
import pickle
import time
# 节点包含字符频率、字符本身、左孩子、右孩子
class Node:
    # 构造函数，初始化
    # self是实例对象本身的引用，对象可以访问类中的其他属性和方法
    def __init__(self, frequency, character=None, left_child=None, right_child=None):
        # 将传入的 frequency 参数赋值给 self.frequency
        self.frequency = frequency
        self.character = character
        self.left_child = left_child
        self.right_child = right_child
    # 定义小于 (<) 运算符的行为。用于比较两个 Node 对象的 frequency 属性。
    def __lt__(self, other):
        # 如果 self 对象的 frequency 小于 other 对象的 frequency，则返回 True，否则返回 False
        return self.frequency < other.frequency


# 计算并返回文本中每个字符的频率，频率信息存在默认字典defaultdict中
def calculate_frequency(file_path):
    # 打开指定路径的文件
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    # 频率信息作为一个字典
    # defaultdict(int) 创建了一个字典，它的默认值是 int() 的返回值，即0。所以，任何不存在的键都会得到值0。
    # 首次访问键 'a' 时，它不存在于字典中，因此返回默认值0。然后我们将其值增加1，所以下次访问时，它的值就是1了。
    frequency = defaultdict(int)
    # 遍历text中每个字符，
    for character in text:
        frequency[character] += 1

    for character in sorted(frequency):
        print(f"'{character}': {frequency[character]}")
    return frequency
#     返回的是一个字典，包含了文件中所有字符及其出现的频率：key是一个字符，每个值（value）是该字符在文件中出现的次数

# 根据字符频率构建huffman树，使用了 Python 的 heapq（最小堆）数据结构，先将所有的字符构建为节点插入堆中，然后每次从堆中取出频率最小的两个节点合并，
# 新的节点频率为这两个节点频率之和，然后将新的节点插入堆中，如此循环直到堆中只剩一个节点，这个节点就是 Huffman 树的根节点。
def build_huffman_tree(frequency):
    # 创建了一个空的列表heap，它将用于作为堆来存储节点
    heap = []
    # frequency字典里存的是字符和对应的频率，遍历字典里的每一项
    for character, freq in frequency.items():
        # Python标准库heapq中的一个函数，它用于将项推入堆，同时保持堆的性质。最后得到一个最小堆，频率从小到大
        heapq.heappush(heap, Node(freq, character=character))

    # 从堆中取出两个最小频率的节点
    while len(heap) > 1:
        # 从heap中弹出两个节点，并分别赋值给left_child和right_child，pop是自带的函数，它会弹出并返回堆中的最小项
        left_child = heapq.heappop(heap)
        right_child = heapq.heappop(heap)

        # 创建一个新的节点，其频率是这两个节点的频率之和，而且它的左右子节点就是这两个取出的节点
        merged_node = Node(left_child.frequency + right_child.frequency,left_child=left_child, right_child=right_child)
        heapq.heappush(heap, merged_node)


    return heap[0]  # root node，the last node

# 遍历huffman树，为每个字符生成对应的huffman编码，存在字典中
# binary_string存放根结点到当前节点的路径
# huffman_dict---字典--存放编码
def build_huffman_dict(node, binary_string='', huffman_dict={}):
    if node is None:
        return
    # 检查当前节点点是否存储了字符，叶节点存字符，合并节点不存
    if node.character is not None:
        # 把当前字符的哈夫曼编码存储到字典中，字符+对应编码
        huffman_dict[node.character] = binary_string
        return
# 左0右1
    build_huffman_dict(node.left_child, binary_string + '0', huffman_dict)
    build_huffman_dict(node.right_child, binary_string + '1', huffman_dict)

    if binary_string == '':  # print once, when we're back at root
        print('Huffman Dictionary:')
        # for character, encoding in huffman_dict.items():
        for character in sorted(huffman_dict.keys()):
            print(f'Character: {character}, Encoding: {huffman_dict[character]}')

    return huffman_dict
def get_code_from_tree(tree, code=''):
    if tree is None:
        return {}

    if tree.character is not None:
        return {tree.character: code}

    codes = {}
    codes.update(get_code_from_tree(tree.left_child, code + '0'))
    codes.update(get_code_from_tree(tree.right_child, code + '1'))
    return codes
# 读取输入文件、计算字符频率、构建huffman树和编码字典，将文件内容转为huffman编码，用pickle库将字典和编码后的文本存储到输出文件
def compress_with_huffman(input_file_path, output_file_path,huffman_tree_path):
    frequency = calculate_frequency(input_file_path)
    huffman_tree = build_huffman_tree(frequency)
    # Save the Huffman tree.
    with open(huffman_tree_path, 'wb') as file:
        pickle.dump(huffman_tree, file)
    huffman_dict = get_code_from_tree(huffman_tree)

    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    encoded_text = bitarray(''.join(huffman_dict[character] for character in text))
    # 整个文本转换为哈夫曼编码，bitarray函数将哈夫曼编码转换为二进制数组
    padding = 8 - (len(encoded_text) % 8)
    encoded_text.extend([0] * padding)
    # for _ in range(padding):
    #     encoded_text.append(0)
    # 写入压缩后的数据。
    # 首先打开输出文件，然后将哈夫曼字典和压缩后的二进制数组一起写入到输出文件
    with open(output_file_path, 'wb') as file:
        file.write(bytes([padding]))
        # pickle.dump(huffman_dict, file)
        # 将哈夫曼字典存储到输出文件中
        encoded_text.tofile(file)
    #     将压缩后的数据写入到输出文件中。


    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(output_file_path)
    # f-string格式化字符串
    print(f'Current compress file: {input_file_path}')
    print(f'Original file size: {original_size} bytes')
    print(f'Compressed file size: {compressed_size} bytes')
    print(f'Compression ratio: {compressed_size / original_size:.2f}')


# 解压huffman编码文件
# 先从文件中读取huffman字典、和编码后的文本，然后根据字典将编码替换为原来的字符，然后写到输出文件
def decompress_huffman(file_path, output_path,huffman_tree_path):
    # 读压缩后的二进制文件
    with open(file_path, 'rb') as file:
        padding = ord(file.read(1))
        encoded_text = bitarray()
        # 创建了一个新的空bitarray对象，命名为encoded_text
        encoded_text.fromfile(file)
    #   以二进制模式打开的文件对象，读取数据并将其加载到 encoded_text 这个 bitarray 对象中。
    #   存储了压缩文本的二进制序列
    with open(huffman_tree_path, 'rb') as file:
        huffman_tree = pickle.load(file)

    decoded_characters = []
    current_node = huffman_tree
    # 从根节点开始
    # 遍历二进制序列
    for bit in encoded_text[:-padding]:
        # 如果位元的值为真，那么就加入字符 '1'，否则就加入字符 '0'。
        # 因为encoded_text 是一个 bitarray 对象，所以使用bool值表示二进制位，而不是整数

        if bit:
            current_node = current_node.right_child
        else:
            current_node = current_node.left_child
            # 如果到达了叶子节点，那么该节点中的字符就是解码出来的字符
        if current_node.character is not None:
            decoded_characters.append(current_node.character)
            # 重新从根节点开始
            current_node = huffman_tree
    decoded_text = ''.join(decoded_characters)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(''.join(decoded_characters))

def verify(input_file_path, decompressed_file_path):

    # 读取原始文件和解压后的文件
    with open(input_file_path, 'r', encoding='utf-8') as original_file:
        original_text = original_file.read()

    with open(decompressed_file_path, 'r', encoding='utf-8') as decompressed_file:
        decompressed_text = decompressed_file.read()

    # 比较原始文件和解压后的文件是否相同
    if original_text == decompressed_text:
        print("Verification successful: the original file and the decompressed file are identical.")
    else:
        print("Verification failed: the original file and the decompressed file are different.")


# Call the function
# to compress
start_time = time.time()
# 插入你需要测量的函数在下面
compress_with_huffman("random_text2.txt", "Huffman_compressed.bin","Huffman_Tree.bin")

end_time = time.time()
execution_time = end_time - start_time
print("Compression time:", execution_time, "seconds")

# to decompress
start_time = time.time()
decompress_huffman("Huffman_compressed.bin", "Huffman_decompressed.txt","Huffman_Tree.bin")
end_time = time.time()
execution_time = end_time - start_time
print("Decompression time:", execution_time, "seconds")


# 使用示例
verify("random_text2.txt","Huffman_decompressed.txt")