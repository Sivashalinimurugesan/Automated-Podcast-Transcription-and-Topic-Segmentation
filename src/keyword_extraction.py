from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(text, top_n=6):
    if not text or len(text.strip()) < 10:
        return []

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=50
    )

    tfidf = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf.toarray()[0]

    ranked = sorted(
        zip(feature_names, scores),
        key=lambda x: x[1],
        reverse=True
    )

    keywords = []
    for word, score in ranked:
        word = word.lower().strip()

        # remove plural duplicates and substrings
        if any(word in k or k in word for k in keywords):
            continue

        keywords.append(word)

        if len(keywords) >= top_n:
            break

    return keywords
