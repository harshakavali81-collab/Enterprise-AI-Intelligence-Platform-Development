"""Deterministic TF-IDF retrieval with explicit abstention; not an LLM."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def retrieve(question: str, documents: list[dict], threshold: float = .13):
    if not question.strip() or not documents:
        return {"answer":"No supported answer available.","citations":[],"abstained":True}
    content = [d["title"] + " " + d["text"] for d in documents]
    vectorizer = TfidfVectorizer(ngram_range=(1,2),strip_accents="unicode")
    matrix = vectorizer.fit_transform(content + [question])
    scores = cosine_similarity(matrix[-1],matrix[:-1]).ravel()
    picks = sorted(range(len(documents)),key=lambda x:float(scores[x]),reverse=True)[:2]
    picks = [i for i in picks if float(scores[i])>=threshold]
    if not picks:
        return {"answer":"Insufficient supporting information in the approved demo documents.","citations":[],"abstained":True}
    cites = [{"id":documents[i]["id"],"title":documents[i]["title"],"url":documents[i].get("url"),"status":documents[i]["status"],"similarity":round(float(scores[i]),3)} for i in picks]
    return {"answer":" ".join(documents[i]["text"] for i in picks),"citations":cites,"abstained":False}
