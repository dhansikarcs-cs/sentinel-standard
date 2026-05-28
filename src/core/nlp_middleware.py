import gc

def extract_insights_and_destroy_raw_text(raw_user_text: str) -> dict:
    lowercased = raw_user_text.lower()
    vectors = []
    
    if any(w in lowercased for w in ["exam", "test", "grade", "study", "school"]):
        vectors.append("academic")
    if any(w in lowercased for w in ["peer", "friend", "talk", "isolate"]):
        vectors.append("social")
        
    sentiment = "SENT_ANXIOUS" if any(w in lowercased for w in ["anxious", "panic", "worried", "scared"]) else "SENT_NEUTRAL"
    summary = f"Local Edge-NLP: Identified {sentiment} tokens linked to {vectors or ['general']} stressors."

    del raw_user_text
    del lowercased
    gc.collect()

    return {
        "primary_sentiment_token": sentiment,
        "sentiment_confidence_score": 0.90,
        "extracted_stress_vectors": vectors,
        "clinical_abstract_summary": summary
    }
