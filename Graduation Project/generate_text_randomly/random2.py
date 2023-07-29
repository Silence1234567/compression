import random
import string

def generate_random_text(length):
    letters = string.ascii_letters
    result_str = ''.join(random.choice(letters) for _ in range(length))
    return result_str

def write_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

# 生成一个长度为100000的随机字母文本
random_text = generate_random_text(100000)
filename = "random_text2.txt"

# 将随机生成的文本写入文件
write_to_file(random_text, filename)
