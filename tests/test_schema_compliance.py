import unittest
import json
import os
import sys

# Dynamic Module Resolution: Force Python to see your root 'src' directory
current_test_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(current_test_dir)
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Safe imports after path routing is established
from src.core.cryptography import SentinelSecurityCore
from src.utils.time_helpers import obfuscate_timestamp
from jsonschema import validate

class TestSchemaCompliance(unittest.TestCase):
    def setUp(self):
        # Target the exact schema physical file path
        schema_path = os.path.join(repo_root, "schemas", "v1", "biometric_telemetry.schema.json")
        
        with open(schema_path, "r") as f:
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
