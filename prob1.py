import re

file = open("mycipher1.txt")
str1 = file.read()
file.close()


def offset(c):
    return ord(c) - 65


def get_diff(base, perm):
    return (offset(perm) - offset(base)) % 26


base_perm = [0 for i in range(26)]
base_perm[offset('A')] = get_diff('T', 'A')
base_perm[offset('C')] = get_diff('H', 'C')
base_perm[offset('X')] = get_diff('E', 'X')

base_perm[offset('W')] = get_diff('A', 'W')
base_perm[offset('R')] = get_diff('O', 'R')  # try for two most common unused letters

base_perm[offset('P')] = get_diff('D', 'P')  # because xh xp frequent and er ed frequent
base_perm[offset('H')] = get_diff('R', 'H')  # because xh xp frequent and er ed frequent

base_perm[offset('L')] = get_diff('W', 'L')  # with word 'was' from LaK
base_perm[offset('K')] = get_diff('S', 'K')  # with word 'was' from LaK
base_perm[offset('N')] = get_diff('F', 'N')  # with word 'first' from Nirst
base_perm[offset('D')] = get_diff('I', 'D')  # with word 'first' from NDrst

# from what day of the month
base_perm[offset('I')] = get_diff('N', 'I')
base_perm[offset('B')] = get_diff('M', 'B')
base_perm[offset('Q')] = get_diff('Y', 'Q')

base_perm[offset('Y')] = get_diff('C', 'Y')
base_perm[offset('J')] = get_diff('B', 'J')
base_perm[offset('E')] = get_diff('K', 'E')
base_perm[offset('U')] = get_diff('L', 'U')
base_perm[offset('V')] = get_diff('U', 'V')
base_perm[offset('G')] = get_diff('G', 'G')
base_perm[offset('Z')] = get_diff('P', 'Z')
base_perm[offset('S')] = get_diff('V', 'S')


def test_perm(perm):
    res = ""
    for j in range(len(str1)):
        off = offset(str1[j])
        shift = perm[off]
        if shift == 0:
            if str1[j] == 'G':
                res += chr(((off - shift) % 26) + 97)
            else:
                res += chr(((off - shift) % 26) + 65)
        else:
            res += chr(((off - shift) % 26) + 97)
    return res


def rep_patterns(substring):
    occ = [m.start() for m in re.finditer(substring, str1)]
    rep_distances = [occ[i + 1] - occ[i] for i in range(len(occ) - 1)]
    print(substring + " repetition patterns :")
    print(rep_distances)


def count_substrings(s, length):
    dic = {}
    morethanonce = {}
    for i in range(len(s) - 2):
        slice = s[i:i + length]
        if slice in dic:
            dic[slice] += 1
        else:
            dic[slice] = 1
    for entry in dic:
        if dic[entry] > 1:
            morethanonce[entry] = dic[entry]
    sortedval = sorted(morethanonce.values())[::-1]
    sorteddic = {}
    for v in sortedval:
        for k in morethanonce.keys():
            if morethanonce[k] == v:
                sorteddic[k] = v
    print(sorteddic)


# Press the green button in the gutter to run the script.

if __name__ == '__main__':
    res = test_perm(base_perm)
    print(res)
    count_substrings(str1, 1)
    count_substrings(str1, 2)
    count_substrings(str1, 3)
