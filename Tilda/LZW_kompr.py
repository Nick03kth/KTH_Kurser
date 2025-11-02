def lzw_compress(data):
    dictionary = {chr(i): i for i in range(256)}
    next_code = 256
    string = ""
    compressed_data = []
    
    for symbol in data:
        string_plus_symbol = string + symbol
        if string_plus_symbol in dictionary:
            string = string_plus_symbol
        else:
            compressed_data.append(dictionary[string])
            if next_code < 4096:  # Begränsa till 12-bitars koder
                dictionary[string_plus_symbol] = next_code
                next_code += 1
            string = symbol

    if string:
        compressed_data.append(dictionary[string])
    
    return compressed_data

def lzw_decompress(compressed_data):
    dictionary = {i: chr(i) for i in range(256)}
    next_code = 256

    string = chr(compressed_data.pop(0))
    decompressed_data = [string]

    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = string + string[0]
        else:
            raise ValueError("Felaktig LZW-kod")
        
        decompressed_data.append(entry)

        if next_code < 4096:  # Begränsa till 12-bitars koder
            dictionary[next_code] = string + entry[0]
            next_code += 1
        
        string = entry

    return ''.join(decompressed_data)
