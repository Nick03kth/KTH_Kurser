from TV import TV
def read_file(filename):
    with open(filename, "r") as tv_info:
        tv_lista=[]
        for line in tv_info:
            new_object = line.strip().split(",")
            for i in range(1,len(new_object)):
                new_object[i] = int(new_object[i])
            tv = TV(*new_object)
            tv_lista.append(tv)
    return tv_lista

print(read_file("C:\\Users\\nick0\\.vscode\\Labb5.py\\Programmering\\allatv.txt"))