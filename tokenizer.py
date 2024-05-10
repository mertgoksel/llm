import string
from nltk.corpus import stopwords
from iteration_utilities import deepflatten

ex = "This is 3 tokeni#zer example w?ith shreeny a_mounts of words"


class Tokenizer:  # For english only
    def __init__(self, texts: list[str], vocab_size=100000) -> None:
        self.texts = texts
        self.vocab_size = vocab_size
        self.stopwords = set(stopwords.words("english"))
        self.corpus = {}
        self.operators = ["</w>", "<BOS>", "<EOS>"]

        self.preproc()
        self.mapping()
        self.indexer()

    def preproc(self):

        ## Check if texts is singular or multiple
        if isinstance(self.texts, str) == True:
            raise TypeError("Given string must be encapsulated as a list")

        ## Format text
        processed_texts = []
        for text in self.texts:
            words = text.lower().split()

            filtered = []
            filtered.append("<BOS>")
            for word in words:
                if word not in self.stopwords:

                    for char in word:  # remove symbols from words
                        if char in string.punctuation:
                            word = word.replace(char, "")

                    filtered.append(word)

                    if word not in self.corpus:
                        self.corpus[word] = 1
                    else:
                        self.corpus[word] += 1
            filtered.append("<EOS>")
            processed_texts.append(filtered)

        self.preproced = processed_texts

    def mapping(self):
        ## Tokenize to characters
        tokenized_texts = []
        for text in self.preproced:
            processed_chars = []
            for word in text:
                if word in self.operators:
                    processed_chars.append(word)
                    continue
                processed_chars.append([*word, "</w>"])
            tokenized_texts.append(processed_chars)
        self.tokenized_text = list(deepflatten(tokenized_texts[0], depth=1, types=list))

        # char counts
        chars = {}
        for char in self.tokenized_text:
            if char in self.operators:
                continue
            if char not in chars:
                chars[char] = 1
                continue
            chars[char] += 1

        # mapping
        charmap = {}
        sorted_chars = sorted(chars, key=chars.get, reverse=True)
        for i, char in enumerate(sorted_chars):
            charmap[char] = i
        self.charmap = charmap
        self.inv_charmap = {j: i for i, j in self.charmap.items()}

    def indexer(self):
        self.indexed = [
            self.charmap[i] if i not in self.operators else i
            for i in self.tokenized_text
        ]
        print(self.indexed)


token = Tokenizer([ex])
