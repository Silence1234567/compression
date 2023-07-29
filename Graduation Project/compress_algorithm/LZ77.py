import os
def compress_lz77(input_file_path, output_file_path, max_length=256):
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        input_data = input_file.read()
        i = 0
        recent_positions = {}

        while i < len(input_data):
            chunk = input_data[i:i + max_length]
            pos = recent_positions.get(chunk, -1)

            if pos != -1 and i - pos <= 65536:
                output_file.write(bytes([(i - pos) // 256, (i - pos) % 256, len(chunk)]))
                i += len(chunk)
            else:
                if len(chunk) > 1:
                    recent_positions[input_data[i:i + 1]] = i
                output_file.write(bytes([0, 0, 1, input_data[i]]))
                i += 1

    original_size = os.path.getsize(input_file_path)
    compressed_size = os.path.getsize(output_file_path)

    print(f'Current compress file: {input_file_path}')
    print(f'Original file size: {original_size} bytes')
    print(f'Compressed file size: {compressed_size} bytes')
    print(f'Compression ratio: {compressed_size / original_size:.2f}')

def decompress_lz77(input_file_path, output_file_path, max_length=256):
    with open(input_file_path, 'rb') as input_file, open(output_file_path, 'wb') as output_file:
        input_data = bytearray(input_file.read())
        output_data = bytearray()
        i = 0

        while i < len(input_data):
            dist = input_data[i] * 256 + input_data[i + 1]
            length = input_data[i + 2]
            if dist == 0:
                output_data.append(input_data[i + 3])
                i += 4
            else:
                for j in range(length):
                    output_data.append(output_data[-dist])
                i += 3

        output_file.write(output_data)

print('-----------------This is LZ77 compress algorithm-----------------')
compress_lz77('../dataset/text1.txt', 'LZ77_compressed.bin')
decompress_lz77('LZ77_compressed.bin', 'LZ77_decompressed.txt')
