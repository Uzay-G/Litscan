import spacy
import pronouncing
from collections import Counter
from spacy.lang.en import English
from spacy.tokens import Span

def process_query(query):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(query)
    doc = [token for token in doc if not token.is_punct and not token.is_space]
    techniques = {}
    techniques["assonance"] = {"desc": "Assonance is a literary technique that takes place when two or more words, close to one another repeat the same vowel sound, but start with different consonant sounds.", "items": process_assonance(doc)}

    techniques["repetition"] = {"desc": "Repetition is a literary device that repeats the same words or phrases a few times to make an idea clearer and more memorable", "items": process_repetition(doc)}

    starting_vocals = process_alliteration(doc)
    techniques["alliteration"] = {"desc": "Technique where consonant sounds are repeated at the beginning of words.", "items": starting_vocals[1]}
    techniques["sibilance"] = {"desc": "Literary technique where hissing sounds are repeated through the use of consonants like 's', 'sh', 'ch' and 'tch'.", "items": starting_vocals[0]}

    techniques["onomatopeia"] = {"desc":  "Onomatopeia is the use of words that phonetically imitate the sound that they describe.", "items": process_onomatopeia(doc)}

    techniques["simile"] = {"desc": "Figure of speech where two different things are explicitly compared.", "items": process_simile(doc)}

    print(techniques)
    num_lit_devices = sum([len(technique["items"]) for technique in techniques.values()])
    return (num_lit_devices, techniques)

def process_assonance(doc):
    assonances = []
    assonance_phones = ["AE1", "EY1", "IY1", "AY1", "OW1", "UW1", "EH1", "IH1", "AO1", "AH1"\
                  "UH1", "OY1", "AW1"]
    parsed_phones = []
    for token in doc:
        token_phones = str(pronouncing.phones_for_word(token.text)).split()
        parsed_phones.append(token_phones[1:])
    
    # check if word has vowels
    vowels = []
    for pronunciation in parsed_phones:
        for sound in pronunciation:
            if sound.find("1") != -1 or sound.find("0") != -1:
                vowels.append(sound)

    vowel_count = Counter(vowels)
    for vowel, count in vowel_count.items():
        if count > 3:
            assonances.append("Assonance in " + vowel)
    return assonances

def process_repetition(doc):
   ## TESTING FOR REPETITION
    words = [token.lemma_.lower() for token in doc]
    repetitions = []
    word_count = Counter(words)
    for word, count in word_count.items():
        if(count > 1):
            repetitions.append("Repetition in " + word)
    return repetitions

def process_alliteration(doc):
    # gather starting phones
    starting_phones = []
    sibilances = []
    alliterations = []
    for token in doc:
        spit = str(pronouncing.phones_for_word(token.text)).split()
        # check it isn't a vowel
        if spit[0].find("1") == -1 and spit[0].find("0") == -1:
            starting_phones.append(spit[0])

    phones_count = Counter(starting_phones)
    
    for phones, count in phones_count.items():
        if count > 1 and (phones == "'S" or phones == "SH" or phones == "CH" or \
           phones == "TH" or phones == "Z"):
            sibilances.append("Sibilance in " + phones)
        elif count > 2:
            alliterations.append("Literary device of alliteration in " + phones)
    
    return (sibilances, alliterations)

def process_onomatopeia(doc):
    onoma = open('onomas.txt', 'r').read().split()
    onomatopeia = []
    for token in doc:
        if str(token.lemma_) in onoma:
            onomatopeia.append("Onomatopeia in '" + str(token.lemma_) + "'.")
    return onomatopeia

def process_simile(doc):
    for token in doc:
        if "as" in str(doc) and (token.pos_ == "ADP") and (token.i) \
            and token.text == "like" \
            or (token.i != -1 and token.text == "similar"):

            return ["Your phrase has a simile using " + token.text]
    return []
