def checksum(l: list) -> int:
    '''
computes checksum for mrz code\n
list items *must* be of str type
    '''
    dictionary = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}
    weight = [7, 3, 1]
    sum = 0
    for i in range(len(l)):
        item = int(l[i]) if ord(l[i]) >= 48 and ord(l[i]) <= 57 else dictionary[l[i]]
        if item == '<':
            item = 0
        sum += item * weight[i % 3]
    return sum % 10

if __name__ == '__main__':
    input = list(input())
    print(checksum(input))