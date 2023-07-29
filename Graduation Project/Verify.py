from compress_algorithm.Huffman_coding import compress_with_huffman, decompress_huffman


def verify(input_file_path, compressed_file_path, decompressed_file_path):
    # 调用你在huffman.py文件中定义的压缩和解压函数
    compress_with_huffman(input_file_path, compressed_file_path)
    decompress_huffman(compressed_file_path, decompressed_file_path)

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


# 使用示例
verify("input.txt", "compressed.bin", "decompressed.txt")
