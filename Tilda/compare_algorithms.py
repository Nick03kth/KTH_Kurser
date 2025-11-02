from time import time
from huffman_kompr import huffman_encode, huffman_decode
from LZW_kompr import lzw_compress, lzw_decompress

# Läs in text från fil
def read_file(filename):
    with open(filename, "r") as file:
        return file.read()

# Mät komprimeringsgrad och tidskomplexitet
def compare_algorithms(text, filename):
    original_size = len(text)  # Original storlek i bytes
    print(f"\n--- Bearbetar fil: {filename} ---")
    print(f"Original storlek: {original_size} bytes")
    
    # LZW
    start = time()
    compressed_lzw = lzw_compress(text)
    lzw_time = time() - start
    lzw_size = len(compressed_lzw) * 2  # LZW lagrar koder som 16-bitars ord
    decompressed_lzw = lzw_decompress(compressed_lzw)
    assert decompressed_lzw == text, "LZW-dekodning misslyckades!"

    lzw_compression_ratio = original_size / lzw_size 

    # Huffmankodning
    start = time()
    encoded_huffman, huffman_tree = huffman_encode(text)
    huffman_time = time() - start
    huffman_size = len(encoded_huffman) // 8  # Omvandlar bitar till bytes
    decoded_huffman = huffman_decode(encoded_huffman, huffman_tree)
    assert decoded_huffman == text, "Huffman-dekodning misslyckades!"

    huffman_compression_ratio = original_size / huffman_size

    

    # Resultat
    print("\n--- Resultat ---")
    print(f"Huffman kodad storlek: {huffman_size} bytes")
    print(f"Huffman komprimeringsgrad: {huffman_compression_ratio:.2%}")
    print(f"Huffman komprimeringstid: {huffman_time:.6f} sekunder")
    print(f"LZW kodad storlek: {lzw_size} bytes")
    print(f"LZW komprimeringsgrad: {lzw_compression_ratio:.2%}")
    print(f"LZW komprimeringstid: {lzw_time:.6f} sekunder")


# Huvudprogram
if __name__ == "__main__":
    files = [
        "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\alice29.txt",
        "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\E.coli.txt",
        "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\random.txt",
        "C:\\Users\\nick0\\.vscode\\.vscode\\pythonfil.py\\aaa.txt"
    ]
      # Upprepa för varje fil 3 gånger
    for filename in files:
        for run in range(3):
            print(f"\n--- Körning {run+1} för filen: {filename} ---")
            text = read_file(filename)
            compare_algorithms(text, filename)
