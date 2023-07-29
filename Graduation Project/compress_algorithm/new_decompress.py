def count_unique_chars(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    return sorted(list(set(content)))
def lzw_decompression(input_file_path, output_file_path, original_file_path):
    # Initialize the dictionary with all unique characters from original file
    unique_chars = count_unique_chars(original_file_path)
    print(f"Unique Characters: {unique_chars}")
    dictionary = {i: char for i, char in enumerate(unique_chars)}

    # Initialize variables
    result = []
    string = ""
    code = ""
    length = len(bin(len(unique_chars))) - 2  # Initial length depends on the unique characters in original file

    with open(input_file_path, 'rb') as f:
        data = f.read()
    binary_string = [format(b, '08b') for b in data]

    for binary in binary_string:
        # Update the code
        code += binary

        while len(code) >= length:
            # Extract the next length bits from code
            next_code = code[:length]
            code = code[length:]

            # If the next_code is in the dictionary, decode it
            if int(next_code, 2) in dictionary:
                entry = dictionary[int(next_code, 2)]
                result.append(entry)

                # If string exists, add string + entry[0] to dictionary
                if string:
                    dictionary[len(dictionary)] = string + entry[0]

                # Update string to be the entry
                string = entry

            # If the next_code is not in the dictionary, add string + string[0] to the dictionary
            else:
                dictionary[len(dictionary)] = string + string[0]
                string = string + string[0]
            print(f"Current code: {code}, Its corresponding string: {entry}")
            # If the length of the next index is more than length, then increment length
            if len(bin(len(dictionary))) - 2 > length:
                length += 1

    # Save the decompressed data
    with open(output_file_path, 'w') as f:
        f.write(''.join(result))


# 使用解压缩函数的例子
input_file_path = '../outcomes/Trie_compressed.bin'
output_file_path = '../outcomes/Trie_decompressd.txt'
original_file_path = '../dataset/test.txt'
lzw_decompression(input_file_path, output_file_path, original_file_path)
