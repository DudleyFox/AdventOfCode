
lastIsEven = False
last = 0
for x in range(1000001):
    m = x*2024
    if len(str(x)) % 2 == 1:
        currentIsEven = len(str(m)) % 2 == 0
        if currentIsEven != lastIsEven:
            print(f"{last}-{x-1} {last*2024}-{(x-1)*2024} isEven={lastIsEven}")
            last = x
        lastIsEven = currentIsEven

