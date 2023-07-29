# import random
# import string
# 
# def generate_random_text(length):
#     # 生成包含所有ASCII字符的列表
#     ascii_characters = list(string.printable)
#     text = ''
#     for _ in range(length):
#         # 从列表中随机选择一个字符
#         random_character = random.choice(ascii_characters)
#         text += random_character
#     return text
# 
# # 生成长度为10000的随机文本
# random_text = generate_random_text(100000)
# 
# # 将随机文本写入文件
# with open("random_text.txt", "w") as file:
#     file.write(random_text)
# import random
# import string
#
# def generate_random_text(word_count):
#     text = ""
#     for _ in range(word_count):
#         word_length = random.randint(1, 12)
#         word = "".join(random.choice(string.ascii_lowercase) for _ in range(word_length))
#         text += word + " "
#     return text.strip()
#
# # Generate 100 words, each word with a length of 5.
# random_text = generate_random_text(1000)
#
# # Save the generated text to a file.
# with open('random_text2.txt', 'w') as file:
#     file.write(random_text)

# # 现在你可以使用 'random_text.txt' 来测试你的哈夫曼编码和解码函数
# compress_with_huffman('random_text.txt', 'compressed.bin', 'huffman_tree.pkl')
# decompress_huffman('compressed.bin', 'decompressed.txt', 'huffman_tree.pkl')

# # 验证解压缩文件是否与原文件相同
# with open("random_text.txt", "r") as file:
#     original_text = file.read()
#
# with open("decompressed.txt", "r") as file:
#     decompressed_text = file.read()
#
# assert original_text == decompressed_text
# print("Huffman compression and decompression successful!")
import random
import string

def generate_random_word(min_length=1, max_length=10):
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

def generate_random_number(max_length=3):
    length = random.randint(1, max_length)
    return ''.join(random.choice(string.digits) for _ in range(length))

def generate_random_sentence(word_count=10, number_probability=0.1):
    sentence = ''
    for _ in range(word_count):
        # if random.random() < number_probability:
        #     sentence += generate_random_number() + ' '
        # else:
            sentence += generate_random_word() + ' '
    sentence = sentence.capitalize().strip()
    sentence += random.choice('.?!#""')
    return sentence

def generate_random_paragraph(sentence_count=20):
    return ' '.join(generate_random_sentence() for _ in range(sentence_count))

def generate_random_text(paragraph_count=100):
    return '\n'.join(generate_random_paragraph() for _ in range(paragraph_count))

# Generate 10 paragraphs of random text.
random_text = generate_random_text(300)

# Save the generated text to a file.
with open('random_text.txt', 'w') as file:
    file.write(random_text)
