import spacy
import pronouncing
from collections import Counter
from spacy.lang.en import English
from spacy.tokens import Span
import string
nlp = spacy.load('en_core_web_sm')
ga = nlp("hello heather heath like a feather")
for token in ga:
    print(token.lemma_.lower())
onoma = ["bam", "bang", "clang", "clank", "clap", "clatter", "click", "clink", \
         "ding", "jingle", "screech", "slap", "thud", "thump", "bloop", "dribble",\
         "drip", "gurgle", "mumble", "murmur", "bawl", "belch", "chatter", "blurt",\
         "thud", "thump", "flutter", "fsst", "fwoosh", "swish", "swoosh", \
         "waft", "whoosh", "whizz", "arf", "baa", "bark", "bray", "buzz", \
         "chirp", "chortle", "cluck", "cock-a-doodle-doo", "cuckoo", "hiss", "meow",\
         "neigh", "oink", "purr", "quack", "ribbit", "tweet", "warble", \
         "chug", "puff", "ding-dong", "plop", "fizz", "sputter", "splat", \
         "clunk", "crash", "ring", "twang", "toot", "pop", "snort", "snuck",\
         "jingle", "rattle", "squeal", "boing", "honk", "caw", "grr" ]
         
sle = "chirpy"
z = nlp(u"he went to the bathroom when death death death, Bathroom")
num_lit_devices = 0

phrase = "She ate the pizza like a hungry bull. Then she smiled as an otter would. As the otter swam towards heaven. John is as high as the Eiffel Tower. Dan's love was fiery."
#doc = nlp("She ate the pizza like a hungry bull. Then she smiled as an otter would.")
doc = nlp(phrase)
##for token in doc:
##    print(token.text, token.pos_)
phrase = input("Enter phrase: ")
#Fix this
doc1 = nlp(phrase)
##TESTING FOR PALINDROME
chars = []
for line in phrase:
    for c in line:
        chars.append(c.lower())

for item in chars:
    if (item.isspace() == True):
        chars.remove(item)
for item in chars:
    if item in string.punctuation:
        chars.remove(item)
if chars == chars[::-1]:
    print("Your input contains a palindrome in " + '-'.join(chars))
    num_lit_devices += 1

## TESTING FOR ASSONANCE
print(pronouncing.phones_for_word(str(phrase)))
pronouncez = ["AE1", "EY1", "IY1", "AY1", "OW1", "UW1", "EH1", "IH1", "AO1", "AH1"\
              "UH1", "OY1", "AW1"]
lol = []
for token in doc1:
    b = pronouncing.phones_for_word(token.text)
    s = str(pronouncing.phones_for_word(token.text)).split()
    slice1 = s[1::]
    lol.append(slice1)
lo1 = nlp(str(lol))
lo2 = [token.text for token in lo1 if token.is_punct != True and (str(token).find("1") != -1 \
       or "0" in token.text)]
lo2_count = Counter(lo2)
for lo2, count in lo2_count.items():
    if count > 2:
        print("Literary device of assonance in " + lo2)
        num_lit_devices += 1
## TESTING FOR REPETITION
words = [token.lemma_.lower() for token in doc1 if token.is_stop != True and token.is_punct != True]
print(words)
reps = []
xy=[]
word_count = Counter(words)
print(word_count)
for c in words:
    reps_num = Counter(words[words.index(c)-6:words.index(c)+6])
    for reps,num in reps_num.items():
        if num > 1:
            print(reps_num)
            print("Repitition of " + reps + ".")
for word, count in word_count.items():
    if(count > 1):
        print("Repetition of " + word)
        num_lit_devices += 1
l = []
##TESTING FOR ALLITERATION
for token in doc1:  
    var = pronouncing.phones_for_word(token.text)
    spit = str(pronouncing.phones_for_word(token.text)).split()
    l.append(spit[0])
lo = nlp(str(l))
pronds = [token.text for token in lo if token.is_punct != True\
          and token.is_quote != True and "1" not in token.text]
prond_count = Counter(pronds)
zet = []

for d in pronds:
    slappy_zez = Counter(pronds[pronds.index(d)-4:pronds.index(d)+4])
    for slappy,zez in slappy_zez.items():
        if zez > 1:
            zet.append(slappy)
for prond, count in prond_count.items():
    if count > 1 and (prond == "'S" or prond == "SH" or prond == "CH" or \
       prond == "TH" or prond == "Z"):
        print("Literary device of sibilance in " + prond)
        num_lit_devices += 1
    elif count > 2:
        print("Literary device of alliteration in " + prond)
        num_lit_devices += 1
##TESTING FOR ONOMATOPEIA
for token in doc1:
    if str(token.lemma_) in onoma:
        print("Literary device of onomatopeia in '" + str(token.lemma_) + "'.")
        num_lit_devices += 1
tester = 0
for token in doc1:
##    span = Span[doc, 0]
##    span.remove(token)
##    print(span))
#    print(token)
    cases = str(doc1[token.i-5:token.i+5])
    if "as" in cases:
        tester = 1
        print(cases)
    if (token.pos_ == "ADP") and (token.i != [0]) \
       and token.text == "like" or (token.text == "as" and tester == 1 and token.pos_ == "ADP") \
       or (token.i != -1 and token.text == "similar") :
        print("Your phrase has a simile using", token.text)
        num_lit_devices += 1
    #else:
        #print(antonym(str(token)))


##    #elif any(str(antonym1(doc1)) == str(token)):
##        #print("This is an antithesis")


if num_lit_devices == 1:
    cond = "literary device"
elif num_lit_devices != 1:
    cond = "literary devices"
rty = "Your phrase has " + str(num_lit_devices) + " " + cond
print("Your phrase has " + str(num_lit_devices) + " " + cond)


