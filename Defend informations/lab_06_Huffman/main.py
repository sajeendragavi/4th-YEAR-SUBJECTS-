from huffman import HuffmanCoding
import sys

if __name__ == "__main__":
    path = sys.argv[1]  #arg[1] = file name
    h = HuffmanCoding(path)  # path ,code, heap and reverse mapping creating
    print("Compressing...")
    output_path = h.compress()
    print(f"Compressed file:  {output_path}\n")
    print("Decompressing...")
    #print('otput_com',output_path)
    output_path = h.decompress(output_path)  #pass as argument output compressed file
    print(f"Decompressed file:  {output_path}")
