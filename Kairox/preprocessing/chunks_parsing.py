import os
import json
from multiprocessing import Pool, cpu_count

# -----------------------------
# RFC 5424 parsing helpers
# -----------------------------
def parse_rfc5424_line(line: str) -> dict:
    """
    Parse a single RFC 5424 log line into components.
    Returns a dict with timestamp, host, app, pid, msgid, severity, facility, message
    """
    try:
        # Example line: <34>1 2025-03-24T11:00:00.000Z node01 sshd 1234 ID45 [meta seq="0"] Accepted password for user
        pri_end = line.find(">")
        pri = int(line[1:pri_end])
        severity = pri & 0b111  # lowest 3 bits
        facility = pri >> 3

        # split remaining line
        rest = line[pri_end+1:].strip()
        parts = rest.split(" ", 6)  # split first 7 fields

        if len(parts) < 7:
            # malformed line
            return {"raw": line}

        timestamp, host, app, pid, msgid, structured, message = parts
        return {
            "timestamp": timestamp,
            "host": host,
            "app": app,
            "pid": pid,
            "msgid": msgid,
            "structured": structured,
            "severity": severity,
            "facility": facility,
            "message": message
        }
    except Exception as e:
        return {"raw": line, "error": str(e)}

# -----------------------------
# Process a single chunk folder
# -----------------------------
def process_chunk(chunk_dir):
    data_log_path = os.path.join(chunk_dir, "data.log")
    parsed_json_path = os.path.join(chunk_dir, "parsed.json")

    if not os.path.exists(data_log_path):
        print(f"Skipping {chunk_dir}, no data.log found")
        return

    with open(data_log_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    parsed_lines = [parse_rfc5424_line(line) for line in lines]

    with open(parsed_json_path, "w", encoding="utf-8") as f:
        json.dump(parsed_lines, f, indent=2)

    print(f"Parsed {len(parsed_lines)} lines in {chunk_dir}")

# -----------------------------
# Main pipeline
# -----------------------------
def main():
    log_folder = input("Enter log folder name under 'chunks/' (e.g., linux_rfc5424): ").strip()
    base_dir = os.path.join("chunks", log_folder)

    if not os.path.exists(base_dir):
        print(f"Folder {base_dir} does not exist")
        return

    # Find all chunk directories
    chunk_dirs = [os.path.join(base_dir, d) for d in os.listdir(base_dir)
                  if os.path.isdir(os.path.join(base_dir, d)) and d.startswith("chunk_")]

    print(f"Found {len(chunk_dirs)} chunks to parse")

    # Process chunks in parallel
    with Pool(cpu_count()) as pool:
        pool.map(process_chunk, chunk_dirs)

    print("All chunks parsed successfully")

if __name__ == "__main__":
    main()
