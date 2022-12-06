import hashlib


prefix = 'bgvyzdsv'
i = 0

hexdigest = ''

while not hexdigest.startswith('000000'):
    i += 1
    hexdigest = hashlib.md5(f'{prefix}{i}'.encode()).hexdigest()
    

print(i)