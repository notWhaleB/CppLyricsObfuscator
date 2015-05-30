# Python 3.4

import sys

def bit_at_pos(val, pos):
    return val & (1 << pos)


def word_bit_mask(word, mask):
    res = word[:]
    for i in range(len(word)):
        if bit_at_pos(mask, i):
            res = res[:i] + res[i].upper() + res[i + 1:]

    return res

argv = []
if __name__ == "__main__":
    argv = sys.argv
if len(argv) == 1:
    argv.append(input().strip())
    argv.append(input().strip())


code_before = ""
obfuscated_code = ""
code_after = ""
lyrics = []
reserved_words = "and asm auto goto if inline int long mutable " \
                 "bool break case catch char class const continue " \
                 "default delete do double else enum explicit export " \
                 "extern false final float for friend namespace new noexcept " \
                 "not operator or private protected public register return " \
                 "short signed static struct switch template this throw " \
                 "true try union unsigned using virtual void volatile while"

with open(argv[1]) as file:
    state = 1
    for line in file.readlines():
        if state == 1:
            if line.strip() != "//LOBEGIN//":
                code_before += line
            else:
                state += 1
        elif state == 2:
            if line.strip() != "//LOEND//":
                obfuscated_code += line.strip() + " "
            else:
                state += 1
        elif state == 3:
            code_after += line

full_code = code_before + " " + obfuscated_code + " " + code_after

with open(argv[2]) as file:
    for line in file.readlines():
        for word in line.strip().split():
            if word.isalpha():
                lyrics.append(word.lower())
            else:
                for i in range(len(word)):
                    if word[0:-i].isalpha():
                        lyrics.append(word[0:-i].lower())
                        break
        lyrics.append("\n")

d = dict()
definable_words = []
disabled_words = set()
for idx, word in enumerate(lyrics):
    if word != "\n":
        if word not in d:
            d[word] = 0
        elif d[word] < (2 ** len(word) - 1):
            d[word] += 1
        lyrics[idx] = word_bit_mask(word, d[word])
        if lyrics[idx] in full_code or lyrics[idx] in reserved_words:
            lyrics[idx] += "_"
            if d[word] < (2 ** len(word) - 1):
                definable_words.append(lyrics[idx])
            else:
                disabled_words.add(lyrics[idx])
        elif d[word] < (2 ** len(word) - 1):
            definable_words.append(lyrics[idx])
        else:
            disabled_words.add(lyrics[idx])

definable_code = []
stack = []
temp = ""
for idx, sym in enumerate(obfuscated_code):
    if sym == '"' or sym == "'":
        if not stack:
            stack.append(sym)
        elif stack[-1] == sym:
            stack.pop()

    if not stack and sym == " ":
        if idx + 1 == len(obfuscated_code) or obfuscated_code[idx + 1] != " ":
            definable_code.append(temp)
            temp = ""
    else:
        temp += sym

defines = []
definable_code.reverse()

for i in range((len(definable_words) - len(definable_code) % len(definable_words)) % len(definable_words)):
        definable_code.append(" ")

words_per_define = len(definable_code) // len(definable_words)

for word in definable_words:
    code_seq = "#define " + word + " "

    for i in range(words_per_define):
        code_seq += definable_code[-1] + " "
        definable_code.pop()

    defines.append(code_seq)

for word in disabled_words:
    defines.append("#define " + word + " ")

defines.sort()

with open(argv[1] + ".lo", 'w') as file:
    print(code_before, file=file)

    print("// Have fun with LyricsObfuscator :) notWhaleB (2015)", file=file)

    for define in defines:
        print(define, file=file)
    print(file=file)

    for word in lyrics:
        if word != "\n":
            print(word, end=" ", file=file)
        else:
            print(file=file)
    print(file=file)

    print(code_after, file=file)

print("Done.")