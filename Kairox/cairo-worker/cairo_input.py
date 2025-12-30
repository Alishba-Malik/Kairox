import os
import json
import sys

def prepare_cairo_input(parsed_json_path, meta_txt_path):
    if not os.path.exists(parsed_json_path):
        raise FileNotFoundError(f"{parsed_json_path} does not exist")
    if not os.path.exists(meta_txt_path):
        raise FileNotFoundError(f"{meta_txt_path} does not exist")

    # -----------------------------
    # Load parsed logs
    # -----------------------------
    with open(parsed_json_path, "r") as f:
        logs = json.load(f)

    num_lines = len(logs)

    # Initialize counts
    severity_counts = [0] * 8
    facility_counts = [0] * 24

    for entry in logs:
        severity_counts[entry["severity"]] += 1
        facility_counts[entry["facility"]] += 1

    # -----------------------------
    # Read meta.txt for chunk_root and line_hashes
    # -----------------------------
    chunk_root = None
    line_hashes = []

    with open(meta_txt_path, "r") as f:
        reading_hashes = False
        for line in f:
            line = line.strip()
            if line.startswith("chunk_merkle_root"):
                chunk_root = int(line.split(":")[1].strip())
            elif line.startswith("line_hashes"):
                reading_hashes = True
            elif reading_hashes and ":" in line:
                _, h = line.split(":")
                line_hashes.append(int(h))

    if chunk_root is None or not line_hashes:
        raise ValueError(f"Invalid meta.txt: missing chunk_root or line_hashes")

    # -----------------------------
    # Prepare Cairo input JSON
    # -----------------------------
    input_data = {
        "chunk_root": chunk_root,
        "num_lines": num_lines,
        "line_hashes": line_hashes,
        "severity_counts": severity_counts,
        "facility_counts": facility_counts
    }

    # Save input.json in the same directory as parsed.json
    input_json_path = os.path.join(os.path.dirname(parsed_json_path), "input.json")
    with open(input_json_path, "w") as f:
        json.dump(input_data, f, indent=2)

    print(f"Generated Cairo input JSON: {input_json_path}")
    return input_json_path

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 prepare_input.py /path/to/parsed.json /path/to/meta.txt")
        sys.exit(1)

    parsed_json_path = sys.argv[1]
    meta_txt_path = sys.argv[2]
    prepare_cairo_input(parsed_json_path, meta_txt_path)
