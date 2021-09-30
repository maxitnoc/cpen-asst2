import re
from math import log, exp
from random import shuffle, randint, sample, random
import numpy as np

file = open("mycipher2.txt")
mystr = file.read()
file.close()
quads_dic = {}


def offset(c):
    off = ord(c) - 65
    return off  # if off < 10 else off - 1


def ciphertwo():  # to find occurrences (or no occurrence in this case) of 'J'
    print(mystr.index('J'))


def decompose_snd():  # to decompose the digrams in order to check for Playfair
    f = open("mycipher2.txt", "a")
    f.write("\n")
    for i in range(0, len(mystr), 2):
        f.write(mystr[i:i + 2] + " ")
    f.close()


def check_digrams():  # checking all digrams to see if double letter occur
    for i in range(0, len(mystr), 2):
        if mystr[i] == mystr[i + 1]:
            print("Double-letter digram !")
            return
    print("Good to go !")


def decipher_digram(char1, char2, key):
    addr1 = np.where(key == offset(char1))
    addr2 = np.where(key == offset(char2))
    if addr1[0] == addr2[0]:  # letters on same row are just shifted back left by one
        orig1 = key[addr1[0], (addr1[1] - 1) % 5]
        orig2 = key[addr2[0], (addr2[1] - 1) % 5]
    elif addr1[1] == addr2[1]:  # letters in same column are just shifted back up by one
        orig1 = key[(addr1[0] - 1) % 5, addr1[1]]
        orig2 = key[(addr2[0] - 1) % 5, addr2[1]]
    else:  # letters form rectangle
        orig1 = key[addr1[0], addr2[1]]  # recover letter on same row but in column of other letter
        orig2 = key[addr2[0], addr1[1]]
    return chr(orig1[0] + 65), chr(orig2[0] + 65)


def decipher_text(text, key):
    res = ""
    for i in range(0, len(text), 2):  # goes through all digrams and decipher them one by one
        dec1, dec2 = decipher_digram(text[i], text[i + 1], key)
        res += dec1
        res += dec2
    return res


def get_quadgrams_stats():
    file = open("english_quadgrams.txt")
    sum = 0
    for line in file:
        arr = line.split(' ')
        quads_dic[arr[0]] = int(arr[1])
        sum += int(arr[1])
    file.close()
    for k in quads_dic.keys():
        quads_dic[k] = log(quads_dic[k] / sum, 10)  # computes the log fitness of a quadgram
    quads_dic["QQQK"] = log(0.01 / sum, 10)  # default value to avoid log(0)


def compute_fitness(text):
    fitness = 0
    for i in range(len(text) - 3):
        sub = text[i:i + 4]
        if sub in quads_dic:
            fitness += quads_dic[sub]
        else:
            fitness += quads_dic["QQQK"]  # if 0 occurrence of quadgram -> default value (to avoid exceptions)
    return fitness


def random_change(key):  # changes the key randomly, added different variations than just swapping two letters
    # in order to "shuffle" more the key and not get stuck with a text
    rand = randint(0, 4)
    newkey = np.copy(key)
    if rand == 0:  # swaps 2 random cells
        for i in range(5):
            temp = np.copy(newkey[:, i])
            newkey[:, i] = temp[::-1]
    elif rand == 1:  # swaps two rows
        randarr = sample(range(5), 2)
        temp = np.copy(newkey[randarr[0]])
        newkey[randarr[0]] = newkey[randarr[1]]
        newkey[randarr[1]] = temp
    elif rand == 2:  # swaps two columns
        randarr = sample(range(5), 2)
        temp = np.copy(newkey[:, randarr[0]])
        newkey[:, randarr[0]] = newkey[:, randarr[1]]
        newkey[:, randarr[1]] = temp
    elif rand == 3:  # reverses all rows
        for i in range(5):
            temp = np.copy(newkey[i, :])
            newkey[i, :] = temp[::-1]
    else: # just switch two letters
        randarr = sample(range(25), 2)
        temp = np.copy(newkey[randarr[0] // 5, randarr[0] % 5])
        newkey[randarr[0] // 5, randarr[0] % 5] = newkey[randarr[1] // 5, randarr[1] % 5]
        newkey[randarr[1] // 5, randarr[1] % 5] = temp

    return newkey


def sim_annealing(key, text): # simulates the whole algorithm as explained in the cited source
    parent_key = key
    deciphered = decipher_text(text, parent_key)
    curr_fit = compute_fitness(deciphered)
    max_temp = 100
    max_count = 10000
    best_key = parent_key
    best_fit = curr_fit
    # print("first best fit of this iteration is " + str(curr_fit))
    # print("first best key of this iteration is " + str(best_key))
    for t in range(max_temp)[::-1]:
        temp = t / 5
        print("temperature is : " + str(temp))

        if temp in range(20):  # to see improvement while the program is running
            print("best fit is : " + str(best_fit))
            print("current fit is : " + str(curr_fit))
            print("current deciphered text is :")
            print(decipher_text(text, best_key))

        for count in range(max_count):
            child_key = random_change(parent_key)
            temp_dec = decipher_text(text, child_key)
            temp_fit = compute_fitness(temp_dec)
            df = temp_fit - curr_fit
            if df >= 0:
                # print("improvement ! prev : " + str(curr_fit) + ", new curr : " + str(temp_fit))
                parent_key = child_key
                curr_fit = temp_fit
            else:
                if temp != 0:
                    prob = exp(df / temp)
                else:
                    prob = 0
                rand = random()
                if rand <= prob:
                    # print("improbable ! prob was : " + str(prob) + " and random number " + str(rand) + "occured.")
                    parent_key = child_key
                    curr_fit = temp_fit
            if curr_fit > best_fit:
                best_fit = curr_fit
                best_key = parent_key

    res = decipher_text(text, best_key)
    return res, best_key


if __name__ == '__main__':
    get_quadgrams_stats()
    rand = [i for i in (0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25)]
    shuffle(rand)  # first random key generation
    key = [[rand[i * 5 + j] for i in range(5)] for j in range(5)]
    first_key = np.array(key)
    text = mystr[:300]
    for i in range(1, 5):
        print("iteration " + str(i) + " :")
        t, f = sim_annealing(first_key, text)
        first_key = f
        print("current deciphered text is : " + t)
        print("current fitness is : " + str(compute_fitness(t)))
        print("current parent key is : ")
        print(first_key)
