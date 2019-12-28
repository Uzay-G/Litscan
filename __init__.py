from flask import Flask, render_template, request, redirect, flash, url_for
app = Flask(__name__, static_url_path="", static_folder="static")
from config import Config
import spacy
import pronouncing
from collections import Counter
from spacy.lang.en import English
from spacy.tokens import Span
import string
app.config.from_object(Config)
from forms import LoginForm
@app.route('/')
def renders():
##    form = LoginForm()
##    if form.validate_on_submit():
##        flash('Your phrase was submitted!')
##        return render_template("Results.html")
    return render_template("Litscan2.html")
@app.route('/techniques')
def techniques():
    return render_template("techniques.html")
@app.route('/about')
def about():
    return render_template("About.html")
@app.route('/results', methods=["POST", "GET"])
def results():
    if request.method == 'POST':
        formdata = request.form['phrase']
        nlp = spacy.load('en_core_web_sm')
##        onoma = ["bam", "bang", "clang", "clank", "clap", "clatter", "click", "clink", \
##                 "ding", "jingle", "screech", "slap", "thud", "thump", "bloop", "dribble",\
##                 "drip", "gurgle", "mumble", "murmur", "bawl", "belch", "chatter", "blurt",\
##                 "thud", "thump", "flutter", "fsst", "fwoosh", "swish", "swoosh", \
##                 "waft", "whoosh", "whizz", "arf", "baa", "bark", "bray", "buzz", \
##                 "chirp", "chortle", "cluck", "cock-a-doodle-doo", "cuckoo", "hiss", "meow",\
##                 "neigh", "oink", "purr", "quack", "ribbit", "tweet", "warble", \
##                 "chug", "puff", "ding-dong", "plop", "fizz", "sputter", "splat", \
##                 "clunk", "crash", "ring", "twang", "toot", "pop", "snort", "snuck",\
##                 "jingle", "rattle", "squeal", "boing", "honk", "caw", "grr"]
        onoma1 = open('onomas.txt', 'r')
        onoma = (onoma1.read()).split()
        print(onoma)
        listings = {}
        num_lit_devices = 0
        ##for token in doc:
        ##    print(token.text, token.pos_)
        phrase = formdata
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
            listings.update( {("Your input contains a palindrome in " + '-'.join(chars)) : 'A palindrome is a word, phrase, or other sequence of characters which reads the same backward as forward, such as madam.'})
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
                listings.update({("Literary device of assonance in " + lo2) : "Assonance is a literary technique that takes place when two or more words, close to one another repeat the same vowel sound, but start with different consonant sounds." })
                num_lit_devices += 1
        ## TESTING FOR REPETITION
        words = [token.lemma_.lower() for token in doc1 if token.is_stop != True and token.is_punct != True]
        word_count = Counter(words)
        for word, count in word_count.items():
            if(count > 1):
                listings.update( {("Repetition of " + word) : "Repetition of words at the start of clauses or verses."})
                num_lit_devices += 1
        l = []
        ##TESTING FOR ALLITERATION
        for token in doc1:  
            var = pronouncing.phones_for_word(token.text)
            spit = str(pronouncing.phones_for_word(token.text)).split()
            l.append(spit[0])
        lo = nlp(str(l))
        pronds = [token.text for token in lo if token.is_punct != True\
                  and token.is_quote != True and ("1" or "0") not in token.text]
        prond_count = Counter(pronds)
        zet = []

        for d in pronds:
            slappy_zez = Counter(pronds[pronds.index(d)-4:pronds.index(d)+4])
            print(slappy_zez)
            for slappy,zez in slappy_zez.items():
                if zez > 1:
                    zet.append(d)
        print(zet)
        for prond, count in prond_count.items():
            if count > 1 and (prond == "'S" or prond == "SH" or prond == "CH" or \
               prond == "TH" or prond == "Z"):
                listings.update({("Literary device of sibilance in " + prond) : "Literary technique where hissing sounds are repeated through the use of consonants like 's', 'sh', 'ch' and 'tch'."})
                num_lit_devices += 1
            elif count > 2:
                listings.update({("Literary device of alliteration in " + prond) : "Technique where consonant sounds are repeated at the beginning of words."})
                num_lit_devices += 1
        ##TESTING FOR ONOMATOPEIA
        for token in doc1:
            
            if str(token.lemma_) in onoma:
                listings.update({("Literary device of onomatopeia in '" + str(token.lemma_) + "'.") : "Onomatopeia is the use of words that phonetically imitate the sound that they describe."})
                num_lit_devices += 1
        tester = 0
        for token in doc1:
        ##    span = Span[doc, 0]
        ##    span.remove(token)
        ##    print(span))
        #    print(token)
            if "as" in str(doc1[token.i-4:token.i+4]):
                tester = 1
            if (token.pos_ == "ADP") and (token.i != [0]) \
               and token.text == "like" or (token.text == "as" and tester == 1 and token.pos_ == "ADP") \
               or (token.i != -1 and token.text == "similar") :
                listings.update({("Your phrase has a simile using " + token.text) : "Figure of speech where two different things are explicitly compared."})
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
        if len(listings) == 0:
            listings = {"The phrase you entered contains 0 literary devices": "Try another phrase!"}
        print(listings) 
        return render_template("Results.html", formdata=formdata, rty=rty, listings=listings)
if __name__ == "__main__":
	app.run()
