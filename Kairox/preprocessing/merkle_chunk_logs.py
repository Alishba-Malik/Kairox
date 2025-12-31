# # import hashlib
# # import math
# # import os
# # from multiprocessing import Pool, cpu_count

# # # -----------------------------
# # # Hash utilities
# # # -----------------------------
# # def sha256(data: bytes) -> bytes:
# #     return hashlib.sha256(data).digest()

# # def hash_leaf(line: str, index: int) -> bytes:
# #     payload = f"{index}:{line}".encode()
# #     return sha256(payload)

# # def hash_node(left: bytes, right: bytes) -> bytes:
# #     return sha256(left + right)

# # # -----------------------------
# # # Merkle tree construction
# # # -----------------------------
# # def build_merkle_tree(leaves: list[bytes]):
# #     """Return the root and the full tree levels (for Merkle paths)"""
# #     if not leaves:
# #         raise ValueError("No leaves to build Merkle tree")

# #     tree_levels = [leaves[:]]  # bottom level first

# #     level = leaves[:]
# #     while len(level) > 1:
# #         next_level = []
# #         for i in range(0, len(level), 2):
# #             left = level[i]
# #             right = level[i + 1] if i + 1 < len(level) else left
# #             next_level.append(hash_node(left, right))
# #         tree_levels.append(next_level)
# #         level = next_level

# #     return tree_levels[-1][0], tree_levels  # root, levels

# # def get_merkle_path(index: int, tree_levels: list[list[bytes]]) -> list[str]:
# #     """Return hex Merkle path for a leaf at given index"""
# #     path = []
# #     idx = index
# #     for level in tree_levels[:-1]:  # exclude root
# #         sibling_idx = idx - 1 if idx % 2 else idx + 1
# #         if sibling_idx >= len(level):
# #             sibling_hash = level[idx]
# #         else:
# #             sibling_hash = level[sibling_idx]
# #         path.append(sibling_hash.hex())
# #         idx = idx // 2
# #     return path

# # # -----------------------------
# # # Chunking logic
# # # -----------------------------
# # def split_into_chunks(lines: list[str], num_chunks: int):
# #     chunk_size = math.ceil(len(lines) / num_chunks)
# #     chunks = []

# #     for i in range(num_chunks):
# #         start = i * chunk_size
# #         end = min(start + chunk_size, len(lines))
# #         if start >= len(lines):
# #             break
# #         chunks.append((i, lines[start:end], start))
# #     return chunks

# # # -----------------------------
# # # Multiprocessing helper
# # # -----------------------------
# # def hash_leaf_worker(args):
# #     idx, line = args
# #     return hash_leaf(line, idx)

# # # -----------------------------
# # # Main pipeline
# # # -----------------------------
# # def main():
# #     log_file = input("Enter path to RFC-5424 log file: ").strip()

# #     if not os.path.exists(log_file):
# #         print("Log file does not exist")
# #         return

# #     with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
# #         lines = [line.rstrip("\n") for line in f]

# #     print(f"Loaded {len(lines)} log lines")

# #     # ---- Build full Merkle tree using multiprocessing ----
# #     print("Computing full-file Merkle root with multiprocessing...")
# #     with Pool(cpu_count()) as pool:
# #         full_leaves = pool.map(hash_leaf_worker, [(i, line) for i, line in enumerate(lines)])

# #     full_root, full_tree_levels = build_merkle_tree(full_leaves)
# #     print(f"FULL MERKLE ROOT: {full_root.hex()}")

# #     # ---- Chunking ----
# #     num_chunks = int(input("Enter number of chunks: ").strip())
# #     chunks = split_into_chunks(lines, num_chunks)

# #     os.makedirs("chunks", exist_ok=True)

# #     print("\nCreating chunks, computing chunk Merkle roots and paths...\n")

# #     for chunk_id, chunk_lines, start_idx in chunks:
# #         chunk_dir = f"chunks/chunk_{chunk_id}"
# #         os.makedirs(chunk_dir, exist_ok=True)

# #         # Compute chunk leaves
# #         chunk_leaves = [
# #             full_leaves[start_idx + i]
# #             for i in range(len(chunk_lines))
# #         ]
# #         chunk_root, _ = build_merkle_tree(chunk_leaves)  # updated

# #         # Save chunk lines
# #         chunk_path = f"{chunk_dir}/data.log"
# #         with open(chunk_path, "w", encoding="utf-8") as cf:
# #             for line in chunk_lines:
# #                 cf.write(line + "\n")

# #         # Save metadata with Merkle paths
# #         with open(f"{chunk_dir}/meta.txt", "w") as mf:
# #             mf.write(f"chunk_id: {chunk_id}\n")
# #             mf.write(f"start_line: {start_idx}\n")
# #             mf.write(f"end_line: {start_idx + len(chunk_lines) - 1}\n")
# #             mf.write(f"chunk_merkle_root: {chunk_root.hex()}\n")
# #             mf.write(f"full_merkle_root: {full_root.hex()}\n")
# #             mf.write("merkle_paths_per_line:\n")
# #             for i in range(len(chunk_lines)):
# #                 path = get_merkle_path(start_idx + i, full_tree_levels)
# #                 mf.write(f"{i}:{','.join(path)}\n")

# #         print(f"Chunk {chunk_id}")
# #         print(f"  Lines: {start_idx} → {start_idx + len(chunk_lines) - 1}")
# #         print(f"  Chunk Merkle Root: {chunk_root.hex()}\n")

# #     print("Done.")

# # if __name__ == "__main__":
# #     main()

# import hashlib
# import math
# import os
# from multiprocessing import Pool, cpu_count

# # -----------------------------
# # Hash utilities
# # -----------------------------
# def sha256(data: bytes) -> bytes:
#     return hashlib.sha256(data).digest()

# def hash_leaf(line: str, index: int) -> bytes:
#     payload = f"{index}:{line}".encode()
#     return sha256(payload)

# def hash_node(left: bytes, right: bytes) -> bytes:
#     return sha256(left + right)

# # -----------------------------
# # Merkle tree construction
# # -----------------------------
# def build_merkle_tree(leaves: list[bytes]):
#     if not leaves:
#         raise ValueError("No leaves to build Merkle tree")

#     tree_levels = [leaves[:]]
#     level = leaves[:]
#     while len(level) > 1:
#         next_level = []
#         for i in range(0, len(level), 2):
#             left = level[i]
#             right = level[i + 1] if i + 1 < len(level) else left
#             next_level.append(hash_node(left, right))
#         tree_levels.append(next_level)
#         level = next_level
#     return tree_levels[-1][0], tree_levels

# def get_merkle_path(index: int, tree_levels: list[list[bytes]]) -> list[str]:
#     path = []
#     idx = index
#     for level in tree_levels[:-1]:
#         sibling_idx = idx - 1 if idx % 2 else idx + 1
#         if sibling_idx >= len(level):
#             sibling_hash = level[idx]
#         else:
#             sibling_hash = level[sibling_idx]
#         path.append(sibling_hash.hex())
#         idx = idx // 2
#     return path

# # -----------------------------
# # Chunking logic
# # -----------------------------
# def split_into_chunks(lines: list[str], num_chunks: int):
#     chunk_size = math.ceil(len(lines) / num_chunks)
#     chunks = []
#     for i in range(num_chunks):
#         start = i * chunk_size
#         end = min(start + chunk_size, len(lines))
#         if start >= len(lines):
#             break
#         chunks.append((i, lines[start:end], start))
#     return chunks

# # -----------------------------
# # Multiprocessing helper
# # -----------------------------
# def hash_leaf_worker(args):
#     idx, line = args
#     return hash_leaf(line, idx)

# # -----------------------------
# # Main pipeline
# # -----------------------------
# def main():
#     log_file = input("Enter path to RFC-5424 log file: ").strip()

#     if not os.path.exists(log_file):
#         print("Log file does not exist")
#         return

#     # Extract log file name without extension
#     log_name = os.path.splitext(os.path.basename(log_file))[0]

#     # Master chunks folder
#     master_chunks_dir = "chunks"
#     os.makedirs(master_chunks_dir, exist_ok=True)

#     # Folder for this specific log file
#     log_chunks_dir = os.path.join(master_chunks_dir, log_name)
#     os.makedirs(log_chunks_dir, exist_ok=True)

#     # Load log lines
#     with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
#         lines = [line.rstrip("\n") for line in f]
#     print(f"Loaded {len(lines)} log lines")

#     # ---- Build full Merkle tree using multiprocessing ----
#     print("Computing full-file Merkle root with multiprocessing...")
#     with Pool(cpu_count()) as pool:
#         full_leaves = pool.map(hash_leaf_worker, [(i, line) for i, line in enumerate(lines)])

#     full_root, full_tree_levels = build_merkle_tree(full_leaves)
#     print(f"FULL MERKLE ROOT: {full_root.hex()}")

#     # ---- Chunking ----
#     num_chunks = int(input("Enter number of chunks: ").strip())
#     chunks = split_into_chunks(lines, num_chunks)

#     print("\nCreating chunks, computing chunk Merkle roots and paths...\n")

#     for chunk_id, chunk_lines, start_idx in chunks:
#         chunk_dir = os.path.join(log_chunks_dir, f"chunk_{chunk_id}")
#         os.makedirs(chunk_dir, exist_ok=True)

#         # Compute chunk leaves
#         chunk_leaves = [full_leaves[start_idx + i] for i in range(len(chunk_lines))]
#         chunk_root, _ = build_merkle_tree(chunk_leaves)

#         # Save chunk lines
#         chunk_path = os.path.join(chunk_dir, "data.log")
#         with open(chunk_path, "w", encoding="utf-8") as cf:
#             for line in chunk_lines:
#                 cf.write(line + "\n")

#         # Save metadata with Merkle paths
#         with open(os.path.join(chunk_dir, "meta.txt"), "w") as mf:
#             mf.write(f"chunk_id: {chunk_id}\n")
#             mf.write(f"start_line: {start_idx}\n")
#             mf.write(f"end_line: {start_idx + len(chunk_lines) - 1}\n")
#             mf.write(f"chunk_merkle_root: {chunk_root.hex()}\n")
#             mf.write(f"full_merkle_root: {full_root.hex()}\n")
#             mf.write("merkle_paths_per_line:\n")
#             for i in range(len(chunk_lines)):
#                 path = get_merkle_path(start_idx + i, full_tree_levels)
#                 mf.write(f"{i}:{','.join(path)}\n")

#         print(f"Chunk {chunk_id}")
#         print(f"  Lines: {start_idx} → {start_idx + len(chunk_lines) - 1}")
#         print(f"  Chunk Merkle Root: {chunk_root.hex()}\n")

#     print("Done.")

# if __name__ == "__main__":
#     main()


import os
import math
from multiprocessing import Pool, cpu_count

# -----------------------------
# Cairo parameters
# -----------------------------
FELT_MOD = 2**251 + 17  # Cairo prime

# -----------------------------
# Hash utilities
# -----------------------------
def pedersen_like_hash(a: int, b: int) -> int:
    """Simple additive hash modulo Cairo prime (placeholder for Pedersen)"""
    return (a + b) % FELT_MOD

def hash_leaf_cairo(line: str, index: int) -> int:
    """Convert line + index into Cairo-friendly felt"""
    val = int.from_bytes(line.encode("utf-8", errors="ignore"), "big") % FELT_MOD
    return pedersen_like_hash(val, index)

# -----------------------------
# Merkle tree construction (linear fold)
# -----------------------------
def compute_merkle_root_cairo(leaf_hashes: list[int]) -> int:
    """Linear left-to-right fold to compute Merkle root (matches Cairo worker)"""
    if not leaf_hashes:
        return 0
    root = leaf_hashes[0]
    for h in leaf_hashes[1:]:
        root = pedersen_like_hash(root, h)
    return root

# -----------------------------
# Chunking logic
# -----------------------------
def split_into_chunks(lines: list[str], num_chunks: int):
    chunk_size = math.ceil(len(lines) / num_chunks)
    chunks = []
    for i in range(num_chunks):
        start = i * chunk_size
        end = min(start + chunk_size, len(lines))
        if start >= len(lines):
            break
        chunks.append((i, lines[start:end], start))
    return chunks

# -----------------------------
# Multiprocessing helper
# -----------------------------
def hash_leaf_worker(args):
    idx, line = args
    return hash_leaf_cairo(line, idx)

# -----------------------------
# Main pipeline
# -----------------------------
def main():
    log_file = input("Enter path to RFC-5424 log file: ").strip()
    if not os.path.exists(log_file):
        print("Log file does not exist")
        return

    # Extract log file name without extension
    log_name = os.path.splitext(os.path.basename(log_file))[0]

    # Master chunks folder
    master_chunks_dir = "chunks"
    os.makedirs(master_chunks_dir, exist_ok=True)

    # Folder for this specific log file
    log_chunks_dir = os.path.join(master_chunks_dir, log_name)
    os.makedirs(log_chunks_dir, exist_ok=True)

    # Load log lines
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        lines = [line.rstrip("\n") for line in f]
    print(f"Loaded {len(lines)} log lines")

    # ---- Compute line hashes (Cairo-compatible) ----
    print("Computing Cairo-compatible line hashes using multiprocessing...")
    with Pool(cpu_count()) as pool:
        line_hashes = pool.map(hash_leaf_worker, [(i, line) for i, line in enumerate(lines)])

    # ---- Compute full Merkle root (linear fold) ----
    full_root = compute_merkle_root_cairo(line_hashes)
    print(f"FULL MERKLE ROOT (Cairo-compatible): {full_root}")

    # ---- Chunking ----
    num_chunks = int(input("Enter number of chunks: ").strip())
    chunks = split_into_chunks(lines, num_chunks)

    print("\nCreating chunks and computing chunk Merkle roots...\n")

    for chunk_id, chunk_lines, start_idx in chunks:
        chunk_dir = os.path.join(log_chunks_dir, f"chunk_{chunk_id}")
        os.makedirs(chunk_dir, exist_ok=True)

        # Compute chunk line hashes and root
        chunk_line_hashes = line_hashes[start_idx:start_idx + len(chunk_lines)]
        chunk_root = compute_merkle_root_cairo(chunk_line_hashes)

        # Write chunk lines
        with open(os.path.join(chunk_dir, "data.log"), "w", encoding="utf-8") as cf:
            for line in chunk_lines:
                cf.write(line + "\n")

        # Write metadata (chunk root, full root, line hashes)
        # with open(os.path.join(chunk_dir, "meta.txt"), "w") as mf:
        #     mf.write(f"chunk_id: {chunk_id}\n")
        #     mf.write(f"start_line: {start_idx}\n")
        #     mf.write(f"end_line: {start_idx + len(chunk_lines) - 1}\n")
        #     mf.write(f"chunk_merkle_root: {chunk_root}\n")
        #     mf.write(f"full_merkle_root: {full_root}\n")
        with open(os.path.join(chunk_dir, "meta.json"), "w") as f:
            f.write(
                f"""{{
  "chunk_id": {chunk_id},
  "start_line": {start_idx},
  "end_line": {start_idx + len(chunk_lines) - 1},
  "chunk_root": "{chunk_root}",
  "full_root": "{full_root}"
}}"""
            )

        print(f"Chunk {chunk_id} created:")
        print(f"  Lines: {start_idx} → {start_idx + len(chunk_lines) - 1}")
        print(f"  Chunk Merkle Root: {chunk_root}\n")

    print("All chunks created and ready for Cairo workers!")

if __name__ == "__main__":
    main()
