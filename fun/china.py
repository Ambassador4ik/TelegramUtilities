from deep_translator import GoogleTranslator
from math import cos, trunc
import random


def gen_numbers(seed):
    nums = []
    count = 0
    for i in range(32):
        if count > 1001:
            break
        for j in range(32):
            if count > 1001:
                break
            for k in range(32):
                num = str(seed[i]) + str(seed[j]) + str(seed[k])
                num = cos(trunc(int(num)**k))
                n = str(num)
                n = n[3:8]
                if n != '' and (13500 <= int(n.rstrip()) <= 40880):
                    nums.append(int(n))
                if count > 1001:
                    break
    return nums


def gen_seed():
    seed = ''
    for i in range(32):
        seed += str(random.randint(0, 9))
    return seed


def update(line):
    for i in range(25):
        st = line[random.randint(1, len(line) - 1)]
        line = line.replace(st, '', 1)
    for i in range(20):
        st = line[random.randint(1, len(line) - 1)]
        line = line.replace(st, ' ', 1)
    return line


def gen_china():
    line = ""
    j = gen_numbers(gen_seed())
    for i in range(1000):
        line += chr(j[i])
    return update(line.encode('utf-8', 'replace').decode()).rstrip()


def translate(st):
    translated = GoogleTranslator(source='auto', target='ru').translate(st)

    result = ''
    allowed = ' ,?!.'
    for char in translated:
        if 1040 <= ord(char) <= 1106 or char in allowed:
            result += char

    return ' '.join(result.split())


def wise_thing():
    return translate(gen_china())
