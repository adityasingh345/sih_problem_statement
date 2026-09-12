from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
def find_duplicate(candidate, reports):
    comparable=[r for r in reports if r["location"]==candidate["location"] and r["event_type"]==candidate["event_type"]]
    if not comparable: return None, 0
    matrix=TfidfVectorizer(stop_words="english").fit_transform([candidate["text"]]+[r["text"] for r in comparable])
    scores=cosine_similarity(matrix[0:1],matrix[1:]).ravel(); best=int(scores.argmax())
    return comparable[best], float(scores[best])
