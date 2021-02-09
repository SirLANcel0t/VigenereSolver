import string
import random
# import time
import operator
import english_quadgrams as quadgram

alphaUpp = list(string.ascii_uppercase)
alphaLow = list(string.ascii_lowercase)

def group_info():
    return [("1003769",   "Mike Jansen",   "INF1D")]

def encrypt_vigenere(plaintext, key):
    counter = 0
    keystring = ''
    key = key.lower()
    # iterate through given text
    for i in plaintext:
        letter = i.lower()
        if letter.isalpha():
            # get index of current iteration in the alphabet
            index = alphaLow.index(letter)
            # get index of current shifter letter in the alphabet
            shifter = alphaLow.index(key[counter])
            # calculate new encrypted letter
            useletter = (index + shifter) % 26
            # check if letter was upper or lowercase, and add the newly encrypted letter to the full new string.
            if i.isupper():
                keystring = keystring + alphaUpp[useletter]
            else:
                keystring = keystring + alphaLow[useletter]
            counter = counter + 1
        # if letter is not in the alphabet, add same character to the string.
        else:
            keystring = keystring+i
        if counter == len(key):
            counter = 0
    return keystring

def decrypt_vigenere(plaintext, key):
    counter = 0
    keystring = ''
    key = key.lower()
    for i in plaintext:
        letter = i.lower()
        if letter.isalpha():
            index = alphaLow.index(letter)
            shifter = alphaLow.index(key[counter])
            useletter = (index - shifter) % 26
            if i.isupper():
                keystring = keystring + alphaUpp[useletter]
            else:
                keystring = keystring + alphaLow[useletter]
            counter = counter + 1
        else:
            keystring = keystring+i
        if counter == len(key):
            counter = 0
    return keystring

def quadgram_fitness(text):
    number = 0
    txtLst = []
    letters = ""
    for i in text:
        if i.lower() in alphaLow:
            letters += i.lower()

    max = len(letters)-4
    n = 0
    while n <= max:
        txtLst.append(letters[(0+n):(4+n)])
        n += 1

    for w in txtLst:
        if w in quadgram.quadgram_score.keys():
            value = quadgram.quadgram_score[w]
            number = number + value
        else:
            number = number + 23
    return number

def solve_vigenere(ciphertext, keylen):
    # start_time = time.time()
    keypvalue = {}
    count = 0
    # create random key
    key = ( ''.join(random.choice(alphaLow) for i in range(keylen)))
    # create initial key fitness
    keyvalue = quadgram_fitness(decrypt_vigenere(ciphertext, key))
    keypvalue[key] = keyvalue
    # while loop that goes on for at least 1000 times the key length to the power of 2
    while count <= (1000 * (keylen ** 2)):
        # pick random character from alphabet
        char1=random.choice(alphaLow)
        # pick random position for key
        ran_pos1 = random.randint(0,len(key)-1)
        # turn key into list
        key_list = list(key)
        # change random position to randomly selected new character
        key_list[ran_pos1]=char1
        mod = ''.join(key_list)
        # new fitness value with newly created key
        modvalue = quadgram_fitness(decrypt_vigenere(ciphertext, mod))
        # check if new fitness is lower than current lowest fitness
        if modvalue < keyvalue:
            key = mod
            keyvalue = quadgram_fitness(decrypt_vigenere(ciphertext, key))
            # add new lowest value to total dict
            keypvalue[key] = keyvalue
        else:
            # if new fitness is not lower, check survival rate. If survived, go on with bad mutation.
            if random.uniform(0, 1) < 0.001:
                key = mod
                keyvalue = quadgram_fitness(decrypt_vigenere(ciphertext, key))
                keypvalue[key] = keyvalue
        # + 1 to go through the loop
        count += 1
    # print("My program took", time.time() - start_time, "to run")
    # get the lowest fitness from dict, take the key from that. This is the best key.
    solvedKey = min(keypvalue.items(), key=operator.itemgetter(1))[0]
    # decrypt using best key, store "decrypted" sentence in a variable
    decrypted = decrypt_vigenere(ciphertext, min(keypvalue.items(), key=operator.itemgetter(1))[0])
    print(keypvalue)
    return (solvedKey, decrypted)

solve_vigenere('V id wueirl lk tb ml vvxk vn pweorndvkkdoaaeg wgirs.',7)
