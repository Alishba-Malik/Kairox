import os
import json


def prepare_chunk(chunk_dir):
    parsed_path = os.path.join(chunk_dir, "parsed.json")
    meta_path = os.path.join(chunk_dir, "meta.json")

    if not os.path.exists(parsed_path) or not os.path.exists(meta_path):
        print(f"Skipping {chunk_dir}")
        return

    with open(parsed_path) as f:
        logs = json.load(f)

    severity = [0] * 8
    facility = [0] * 24

    for e in logs:
        if "severity" in e:
            severity[e["severity"]] += 1
        if "facility" in e:
            facility[e["facility"]] += 1

    with open(meta_path) as f:
        meta = json.load(f)

    # stats_commitment = poseidon_hash_many(combined_stats)

    cairo_input = [
        int(meta["chunk_root"]),
        len(logs),
        8,            # severity span length
        *severity,
        24,           # facility span length
        *facility,
        
    ]
    cairo_input_hexified = [hex(int(x)) for x in cairo_input]
    out_path = os.path.join(chunk_dir, "input.json")
    with open(out_path, "w") as f:
        json.dump(cairo_input_hexified, f)

    print(f"Prepared Cairo input for {chunk_dir}")


def main():
    log_folder = input("Enter log folder under chunks/: ").strip()
    base = os.path.join("chunks", log_folder)

    chunk_dirs = [
        os.path.join(base, d)
        for d in os.listdir(base)
        if d.startswith("chunk_")
    ]

    for c in chunk_dirs:
        prepare_chunk(c)

    print("All worker inputs prepared.")


if __name__ == "__main__":
    main()

   main()