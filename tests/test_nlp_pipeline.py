import unittest
from src.core.nlp_middleware import extract_insights_and_destroy_raw_text

class TestNLPMiddleware(unittest.TestCase):
    def test_data_minimization_processing(self):
        raw_input = "I feel anxious about my school final exam grades."
        result = extract_insights_and_destroy_raw_text(raw_input)
        
        self.assertEqual(result["primary_sentiment_token"], "SENT_ANXIOUS")
        self.assertIn("academic", result["extracted_stress_vectors"])
        self.assertNotIn("raw_input", result)
