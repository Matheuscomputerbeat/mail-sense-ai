from __future__ import annotations

import re
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer


_whithespace_re = re.compile(r"\s+")
_non_word_re = re.compile(r"[^\wÀ-ÿ]+", re.UNICODE)


def preprocess_pt(text: str) -> str:
    """
    Pré-processamento clássico (pedido no desafio):
    - lower
    - remove pontuação “pesada”
    - remove stopwords
    - stemming (radicalização)
    """
    text =  (text or "").lower()
    text = _non_word_re.sub(" ", text)
    text = _whithespace_re.sub(" ", text).strip()
    
    words =  text.split(" ")
    sw = set(stopwords.words("portuguese"))
    stemmer = SnowballStemmer("portuguese")

    cleaned = [stemmer.stem(w) for w in words if w and w not in sw and len(w) > 2]
    return " ".join(cleaned)