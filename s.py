import random
words = {}
tokens = []
temp = ''
remove = ['!',',','.','\"','\'',':',':','&','(',')']
corpus = open("c.txt",'r')
i = 0
for line in corpus.read().splitlines():
    line.rstrip()
    for word in line.split(" "):
        final = word
        for char in remove:
            if char in final:
                temp = char
                final.strip(char)
        if not temp == '':
            tokens.append(temp)
            temp = ''
        tokens.append(final)
        i += 1
        words[word] = "word"



print(tokens)
print("read in " + str(i) + " tokens and " + str(len(words)) + " words")


def find_bigrams(tokens,words):
    bigram = [{key for key in workds.keys() : }]
    for i in range(len(tokens)[1:]):
