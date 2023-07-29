import os
import pickle

def BWT(s):
    """实现Burrows-Wheeler变换"""
    s = s + '\x00'
    table = sorted(s[i:] + s[:i] for i in range(len(s)))
    last_column = [row[-1:] for row in table]
    return "".join(last_column)

def I_BWT(r):
    """实现逆Burrows-Wheeler变换"""
    table = [""] * len(r)
    for _ in range(len(r)):
        table = sorted(r[i] + table[i] for i in range(len(r)))
    s = [row for row in table if row.endswith('\x00')][0]
    return s.rstrip('\x00')

def RLE(s):
    """实现游程编码"""
    r = []
    l = len(s)
    i = 0
    while i < l:
        count = 1
        while i + 1 < l and s[i] == s[i+1]:
            i += 1
            count += 1
        r.append((s[i], count))
        i += 1
    return r

def I_RLE(r):
    """实现逆游程编码"""
    s = ''
    for (ch, count) in r:
        s += ch * count
    return s

def compress_file(input_file_path, output_file_path):
    """压缩文件"""
    CHUNK_SIZE = 1024
    with open(input_file_path, 'r') as f_in, open(output_file_path, 'wb') as f_out:
        while True:
            chunk = f_in.read(CHUNK_SIZE)
            if not chunk:
                break
            transformed_chunk = BWT(chunk)
            compressed_chunk = RLE(transformed_chunk)
            pickle.dump(compressed_chunk, f_out)

    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(output_file_path)

    print(f'Current compress file: {input_file_path}')
    print(f'Original file size: {original_size} bytes')
    print(f'Compressed file size: {compressed_size} bytes')
    print(f'Compression ratio: {compressed_size / original_size:.2f}')

def decompress_file(input_file_path, output_file_path):
    """解压缩文件"""
    with open(input_file_path, 'rb') as f_in, open(output_file_path, 'w') as f_out:
        while True:
            try:
                compressed_chunk = pickle.load(f_in)
            except EOFError:
                break
            transformed_chunk = I_RLE(compressed_chunk)
            chunk = I_BWT(transformed_chunk)
            f_out.write(chunk)

print('-----------------This is BWT compress algorithm-----------------')
compress_file('dataset/text1.txt', 'BWT_compressed.bin')
decompress_file('BWT_compressed.bin', 'BWT_decompressed.txt')