# # import os
# # import json
# # import subprocess
# # from multiprocessing import Pool, cpu_count

# # def run_worker_on_chunk(args):
# #     log_folder, chunk_dir = args

# #     parsed_json = os.path.join(chunk_dir, "parsed.json")
# #     meta_txt = os.path.join(chunk_dir, "meta.txt")

# #     if not os.path.exists(parsed_json) or not os.path.exists(meta_txt):
# #         print(f"Skipping {chunk_dir}, missing parsed.json or meta.txt")
# #         return

# #     # -----------------------------
# #     # Load parsed logs
# #     # -----------------------------
# #     with open(parsed_json, "r") as f:
# #         logs = json.load(f)

# #     num_lines = len(logs)

# #     severity_counts = [0] * 8
# #     facility_counts = [0] * 24

# #     for entry in logs:
# #         if "severity" in entry:
# #             severity_counts[entry["severity"]] += 1
# #         if "facility" in entry:
# #             facility_counts[entry["facility"]] += 1

# #     # -----------------------------
# #     # Read chunk merkle root
# #     # -----------------------------
# #     with open(meta_txt, "r") as f:
# #         for line in f:
# #             if line.startswith("chunk_merkle_root"):
# #                 chunk_root = int(line.split(":")[1].strip())

# #     # -----------------------------
# #     # Prepare Cairo input
# #     # -----------------------------
# #     proof_dir = os.path.join("proofs", log_folder, os.path.basename(chunk_dir))
# #     os.makedirs(proof_dir, exist_ok=True)

# #     input_path = os.path.join(proof_dir, "input.json")

# #     with open(input_path, "w") as f:
# #         json.dump({
# #             "chunk_root": chunk_root,
# #             "num_lines": num_lines,
# #             "severity_counts": severity_counts,
# #             "facility_counts": facility_counts
# #         }, f, indent=2)

# #     # -----------------------------
# #     # Run Cairo worker
# #     # -----------------------------
# #     subprocess.run([
# #         "cairo-run",
# #         "--program", "worker.cairo",
# #         "--program_input", input_path,
# #         "--layout", "all_cairo"
# #     ], check=True)

# #     print(f"Proof generated for {chunk_dir}")

# # def main():
# #     log_folder = input("Enter log folder name under 'chunks/': ").strip()
# #     base_dir = os.path.join("chunks", log_folder)

# #     chunk_dirs = [
# #         os.path.join(base_dir, d)
# #         for d in os.listdir(base_dir)
# #         if d.startswith("chunk_")
# #     ]

# #     with Pool(cpu_count()) as pool:
# #         pool.map(run_worker_on_chunk, [(log_folder, c) for c in chunk_dirs])

# #     print("All chunk worker proofs completed")

# # if __name__ == "__main__":
# #     main()
# import os
# import json
# import subprocess
# from multiprocessing import Pool, cpu_count

# def run_worker_on_chunk(args):
#     log_folder, chunk_dir = args

#     parsed_json = os.path.join(chunk_dir, "parsed.json")
#     meta_txt = os.path.join(chunk_dir, "meta.txt")

#     if not os.path.exists(parsed_json) or not os.path.exists(meta_txt):
#         print(f"Skipping {chunk_dir}, missing parsed.json or meta.txt")
#         return

#     # -----------------------------
#     # Load parsed logs
#     # -----------------------------
#     with open(parsed_json, "r") as f:
#         logs = json.load(f)

#     num_lines = len(logs)

#     severity_counts = [0] * 8
#     facility_counts = [0] * 24

#     for entry in logs:
#         severity_counts[entry["severity"]] += 1
#         facility_counts[entry["facility"]] += 1

#     # -----------------------------
#     # Read meta.txt
#     # -----------------------------
#     chunk_root = None
#     line_hashes = []

#     with open(meta_txt, "r") as f:
#         reading_hashes = False
#         for line in f:
#             line = line.strip()

#             if line.startswith("chunk_merkle_root"):
#                 chunk_root = int(line.split(":")[1].strip())

#             elif line.startswith("line_hashes"):
#                 reading_hashes = True

#             elif reading_hashes and ":" in line:
#                 _, h = line.split(":")
#                 line_hashes.append(int(h))

#     if chunk_root is None or not line_hashes:
#         print(f"Invalid meta.txt in {chunk_dir}")
#         return

#     # -----------------------------
#     # Prepare Cairo input
#     # -----------------------------
#     proof_dir = os.path.join("proofs", log_folder, os.path.basename(chunk_dir))
#     os.makedirs(proof_dir, exist_ok=True)

#     input_path = os.path.join(proof_dir, "input.json")

#     with open(input_path, "w") as f:
#         json.dump({
#             "chunk_root": chunk_root,
#             "num_lines": num_lines,
#             "line_hashes": line_hashes,
#             "severity_counts": severity_counts,
#             "facility_counts": facility_counts
#         }, f, indent=2)

#     # -----------------------------
#     # Run Cairo worker via Scarb
#     # -----------------------------
#     subprocess.run(
#         [
#             "scarb", "cairo-run",
#             "--bin", "worker",
#             "--",
#             "--program_input", input_path
#         ],
#         cwd="cairo_worker",   # IMPORTANT: run inside Scarb project
#         check=True
#     )

#     print(f"Proof generated for {chunk_dir}")

# def main():
#     log_folder = input("Enter log folder name under 'chunks/': ").strip()
#     base_dir = os.path.join("chunks", log_folder)

#     chunk_dirs = [
#         os.path.join(base_dir, d)
#         for d in os.listdir(base_dir)
#         if d.startswith("chunk_")
#     ]

#     with Pool(cpu_count()) as pool:
#         pool.map(run_worker_on_chunk, [(log_folder, c) for c in chunk_dirs])

#     print("All chunk worker proofs completed")

# if __name__ == "__main__":
#     main()

import os
import json
import subprocess
from multiprocessing import Pool, cpu_count

def run_worker_on_chunk(args):
    log_folder, chunk_dir = args

    parsed_json = os.path.join(chunk_dir, "parsed.json")
    meta_txt = os.path.join(chunk_dir, "meta.txt")

    if not os.path.exists(parsed_json) or not os.path.exists(meta_txt):
        print(f"Skipping {chunk_dir}, missing parsed.json or meta.txt")
        return

    # 1. Load parsed logs
    with open(parsed_json, "r") as f:
        logs = json.load(f)

    num_lines = len(logs)
    severity_counts = [0] * 8
    facility_counts = [0] * 24

    for entry in logs:
        severity_counts[entry["severity"]] += 1
        facility_counts[entry["facility"]] += 1

    # 2. Read meta.txt for chunk root and hashes
    chunk_root = None
    line_hashes = []
    with open(meta_txt, "r") as f:
        reading_hashes = False
        for line in f:
            line = line.strip()
            if line.startswith("chunk_merkle_root"):
                chunk_root = line.split(":")[1].strip()
            elif line.startswith("line_hashes"):
                reading_hashes = True
            elif reading_hashes and ":" in line:
                line_hashes.append(line.split(":")[1].strip())

    # 3. Prepare Cairo input (FLATTENED ARRAY)
    # Order: root, num_lines, hashes_len, hashes..., sev_len, sev..., fac_len, fac...
    cairo_input = [
        str(chunk_root),
        str(num_lines),
        str(len(line_hashes)), *[str(h) for h in line_hashes],
        str(len(severity_counts)), *[str(s) for s in severity_counts],
        str(len(facility_counts)), *[str(f) for f in facility_counts]
    ]

    proof_dir = os.path.join("proofs", log_folder, os.path.basename(chunk_dir))
    os.makedirs(proof_dir, exist_ok=True)
    input_path = os.path.join(proof_dir, "input.json")
    trace_path = os.path.join(proof_dir, "trace.bin")
    memory_path = os.path.join(proof_dir, "memory.bin")

    with open(input_path, "w") as f:
        json.dump(cairo_input, f) # Saves as [ "val1", "val2", ... ]

    # 4. Run Cairo worker using the cairo1-run binary you built
    # Use the absolute path or relative path to where you built cairo1-run
    cairo_run_path = "./cairo-vm/target/release/cairo1-run" 
    
    try:
        subprocess.run([
            cairo_run_path,
            "target/dev/worker.sierra.json", # Path to your compiled Sierra file
            "--layout", "all_cairo",
            "--args_file", input_path,
            "--trace_file", trace_path,
            "--memory_file", memory_path,
            "--proof_mode",
            "--print_output"
        ], check=True)
        print(f"✅ Success: Trace generated for {chunk_dir}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Cairo VM for {chunk_dir}: {e}")

def main():
    log_folder = input("Enter log folder name under 'chunks/': ").strip()
    base_dir = os.path.join("chunks", log_folder)

    chunk_dirs = [
        os.path.join(base_dir, d)
        for d in os.listdir(base_dir)
        if d.startswith("chunk_")
    ]

    with Pool(cpu_count()) as pool:
        pool.map(run_worker_on_chunk, [(log_folder, c) for c in chunk_dirs])

    print("All chunk worker proofs completed")

if __name__ == "__main__":
    main()

# ... (rest of your main() remains the same)