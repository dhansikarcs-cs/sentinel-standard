import unittest
import json
from jsonschema import validate
from src.core.cryptography import SentinelSecurityCore
from src.utils.time_helpers import obfuscate_timestamp

class TestSchemaCompliance(unittest.TestCase):
    def setUp(self):
        with open("schemas/v1/biometric_telemetry.schema.json", "r") as f:
            self.bio_schema = json.load(f)
        self.engine = SentinelSecurityCore("secure_pass_123")

    def test_generated_payload_matches_schema(self):
        biometric_raw = {"heart_rate_bpm": 80, "eda_microsiemens": 2.1}
        envelope = self.engine.encrypt_payload(biometric_raw)
        
        valid_packet = {
          "metadata": {
            "packet_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
            "coarse_timestamp_ms": obfuscate_timestamp(1717141200000),
            "timezone_offset_min": 330
          },
          "crypto_envelope": envelope
        }
        validate(instance=valid_packet, schema=self.bio_schema)
