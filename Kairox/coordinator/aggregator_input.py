import os
import json

def prepare_aggregation(base_dir):
    # 1. Collect and sort chunk directories
    chunk_dirs = sorted([
        d for d in os.listdir(base_dir) 
        if d.startswith("chunk_") and os.path.isdir(os.path.join(base_dir, d))
    ], key=lambda x: int(x.split('_')[1]))

    if not chunk_dirs:
        print("Error: No chunk directories found.")
        return

    chunk_roots = []
    proof_objects = []
    global_root = None

    # 2. Process each chunk
    for chunk_name in chunk_dirs:
        chunk_path = os.path.join(base_dir, chunk_name)
        
        # Load meta.json for roots
        meta_path = os.path.join(chunk_path, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                meta = json.load(f)
                # Store as int internally for now
                chunk_roots.append(int(meta["chunk_root"]))
                if global_root is None:
                    global_root = int(meta["full_root"])
        
        # Load proof.json
        proof_file = os.path.join(chunk_path, "proofs", "proof.json")
        if os.path.exists(proof_file):
            with open(proof_file, 'r') as f:
                raw_proof = json.load(f)
                proof_objects.append({
                    "proof_data": raw_proof.get("proof_data", []), 
                    "public_inputs": [int(meta["chunk_root"])] 
                })
        else:
            print(f"Warning: Proof missing for {chunk_name}")

    if global_root is None:
        print("Error: Could not find full_root in any meta.json")
        return

    # 3. Construct the flat input list for Cairo's Serde
    # Every value MUST be a string starting with "0x"
    aggregator_input = [hex(global_root)]
    
    # Add chunk_roots Span: [len, e1, e2...]
    aggregator_input.append(hex(len(chunk_roots)))
    for root in chunk_roots:
        aggregator_input.append(hex(root))
    
    # Add chunk_proofs Span: [len, p1, p2...]
    aggregator_input.append(hex(len(proof_objects)))
    for p in proof_objects:
        # Flattening StwoProof: [data_len, *data, inputs_len, *inputs]
        
        # proof_data Span
        aggregator_input.append(hex(len(p["proof_data"])))
        for d in p["proof_data"]:
            # Handle potential hex or int in proof_data
            val = int(d, 16) if isinstance(d, str) and d.startswith('0x') else int(d)
            aggregator_input.append(hex(val))

        # public_inputs Span
        aggregator_input.append(hex(len(p["public_inputs"])))
        for pi in p["public_inputs"]:
            val = int(pi, 16) if isinstance(pi, str) and pi.startswith('0x') else int(pi)
            aggregator_input.append(hex(val))

    # 4. Save
    output_path = os.path.join(base_dir, "aggregator_input.json")
    with open(output_path, 'w') as f:
        # This will produce a list of quoted hex strings: ["0x123", "0xabc"]
        json.dump(aggregator_input, f)

    print(f"Found Global Root: {hex(global_root)}")
    print(f"Prepared aggregation input for {len(chunk_roots)} chunks at {output_path}")

def main():
    path = input("Enter the log folder path: ").strip()
    prepare_aggregation(path)

if __name__ == "__main__":
    main()