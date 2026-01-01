#!/bin/bash

# 1. Ask the user for the folder path
echo "Enter the path to your log folder (e.g., chunks/linux_rfc5424):"
read -r USER_PATH

# 2. Resolve to absolute path
BASE_DIR=$(realpath "$USER_PATH")

if [ ! -d "$BASE_DIR" ]; then
    echo "Error: Directory $BASE_DIR does not exist."
    exit 1
fi

# IMPORTANT: Clear old executions so we start at 1
echo "Cleaning up old execution traces..."
rm -rf target/execute/worker/execution*

echo "Starting batch proving for: $BASE_DIR"

# Initialize execution counter
i=1

# 3. Loop through every chunk folder
for chunk in "$BASE_DIR"/chunk_*; do
    [ -d "$chunk" ] || continue
    
    echo "-----------------------------------"
    echo "Processing $(basename "$chunk") (Execution ID: $i)..."
    
    # 4. Execute
    scarb execute --arguments-file "$chunk/input.json"
    
    if [ $? -ne 0 ]; then
        echo "Execution failed for $chunk. Skipping proof."
        ((i++))
        continue
    fi

    # 5. Prove
    # We pass the current value of i to the execution-id
    scarb prove --execution-id "$i"
    
    # 6. Verify where the proof was saved and move it
    EXEC_PATH="target/execute/worker/execution$i"
    
    if [ -f "${EXEC_PATH}/proof/proof.json" ]; then
        mkdir -p "$chunk/proofs"
        cp "${EXEC_PATH}/proof/proof.json" "$chunk/proofs/proof.json"
        echo "Success: Proof saved to $chunk/proofs/proof.json"
    else
        echo "Error: Proof file not found in ${EXEC_PATH}/proof/"
    fi

    # Increment counter for the next chunk
    ((i++))
done

echo "-----------------------------------"
echo "All available chunks processed."