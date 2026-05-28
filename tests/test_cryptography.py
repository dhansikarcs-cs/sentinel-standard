import unittest
from src.core.cryptography import SentinelSecurityCore

class TestCryptographicEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SentinelSecurityCore("test_passphrase_123!")
        self.payload = {"heart_rate_bpm": 72, "hrv_rmssd_ms": 45.0}

    def test_encryption_decryption_pipeline(self):
        envelope = self.engine.encrypt_payload(self.payload)
        decrypted = self.engine.decrypt_payload(envelope)
        self.assertEqual(decrypted["heart_rate_bpm"], 72)

    def test_tamper_detection(self):
        envelope = self.engine.encrypt_payload(self.payload)
        corrupted_b64 = list(envelope["ciphertext_b64"])
        corrupted_b64 = 'A' if corrupted_b64 != 'A' else 'B'
        envelope["ciphertext_b64"] = "".join(corrupted_b64)
        
        with self.assertRaises(Exception):
            self.engine.decrypt_payload(envelope)
