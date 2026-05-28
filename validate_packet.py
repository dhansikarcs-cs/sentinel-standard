import json
import sys
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def validate_json_packet(packet_path, schema_path):
    """
    Validates a generated telemetry or journal JSON packet against 
    the formal Sentinel open-source specification rules.
    """
    try:
        with open(packet_path, 'r') as p_file:
            packet_data = json.load(p_file)
            
        with open(schema_path, 'r') as s_file:
            schema_data = json.load(s_file)
            
        # Run formal JSON Schema validation rules
        validate(instance=packet_data, schema=schema_data)
        print(f"✅ SUCCESS: Packet '{packet_path}' perfectly matches schema '{schema_path}'.")
        print("🔒 Data structure, cryptographic types, and privacy structures verified.")
        return True
        
    except FileNotFoundError as e:
        print(f"❌ ERROR: File not found. Details: {e}", file=sys.stderr)
        return False
    except ValidationError as e:
        print(f"❌ VALIDATION FAILED: Data packet breaches framework rules!", file=sys.stderr)
        print(f"Field Path: {list(e.path)}", file=sys.stderr)
        print(f"Rule Broken: {e.message}", file=sys.stderr)
        return False
    except json.JSONDecodeError:
        print("❌ ERROR: Invalid JSON file format. Check your syntax/commas.", file=sys.stderr)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python validate_packet.py <path_to_data_packet.json> <path_to_schema.json>")
        sys.exit(1)
        
    success = validate_json_packet(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)
