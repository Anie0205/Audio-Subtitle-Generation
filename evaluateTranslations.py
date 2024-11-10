from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Levenshtein import distance as levenshtein_distance

def evaluate_translation_metrics(translated_text, reference_text):

    # BLEU Score
    reference = [reference_text.split()]
    candidate = translated_text.split()
    smooth_fn = SmoothingFunction().method1
    bleu_score = sentence_bleu(reference, candidate, smoothing_function=smooth_fn)

    # ROUGE Score
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = scorer.score(reference_text, translated_text)

    #   
    vectorizer = TfidfVectorizer().fit_transform([translated_text, reference_text])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)[0, 1]

    # Levenshtein Distance
    lev_distance = levenshtein_distance(translated_text, reference_text)

    # Return all metrics
    return {
        "BLEU Score": bleu_score,
        "ROUGE Scores": rouge_scores,
        "Cosine Similarity": cosine_sim,
        "Levenshtein Distance": lev_distance
    }

# Example usage
#translated_text = "Bonjour le monde!"
#reference_text = "Bonjour, le monde!"

#metrics = evaluate_translation_metrics(translated_text, reference_text)
#print("Evaluation Metrics:", metrics)
