def binary_search(the_list, key):
    low = 0
    high = len(the_list) - 1
    
    while low <= high:
        mid = (low + high) // 2
        if the_list[mid] == key:
            return key  # Found, return the key itself
        elif the_list[mid] < key:
            low = mid + 1
        else:
            high = mid - 1
    
    return None  # Not found

def main():
    # Read the list
    indata = input().strip()
    the_list = indata.split()

    # Read the keys to search for
    key = input().strip()
    while key != "#":
        result = binary_search(the_list, key)
        print(result)
        key = input().strip()

main()