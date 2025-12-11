import sys

def generate(charset, index):
    tIndex = index
    csLen = len(charset)
    result = []
    while tIndex > -1:
        s = charset[tIndex % csLen]
        result.append(s)
        tIndex = tIndex // csLen
        tIndex -= 1
    return result

if __name__ == "__main__":
    charset = sys.argv[1]
    index = int(sys.argv[2])
    r = print(generate(charset, index))
