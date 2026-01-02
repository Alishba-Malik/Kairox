// // use core::poseidon::poseidon_hash_span;

// // // Added Copy to the derive list
// // #[derive(Copy, Drop, Serde)]
// // struct StwoProof {
// //     proof_data: Span<felt252>,
// //     public_inputs: Span<felt252>, 
// // }

// // #[executable]
// // fn main(
// //     global_root: felt252,
// //     chunk_roots: Span<felt252>,
// //     chunk_proofs: Span<StwoProof>,
// // ) -> bool {
// //     // 1. Verify Merkle Integrity
// //     let computed_root = poseidon_hash_span(chunk_roots); 
// //     assert(computed_root == global_root, 'Merkle Root Mismatch');

// //     // 2. Recursive Verification Loop
// //     let mut i: usize = 0;
// //     while i < chunk_proofs.len() {
// //         // Now this * works because the struct is Copy
// //         let current_proof = *chunk_proofs.at(i);
// //         let expected_chunk_root = *chunk_roots.at(i);

// //         // 3. Link the Proof to the Chunk Root
// //         // Accessing the first element of public_inputs (the chunk root)
// //         let proof_claimed_root = *current_proof.public_inputs.at(0);
// //         assert(proof_claimed_root == expected_chunk_root, 'Proof not for this chunk');

// //         i += 1;
// //     };

// //     true 
// // }

// use core::array::ArrayTrait;

// #[derive(Copy, Drop, Serde)]
// struct StwoProof {
//     proof_data: Span<felt252>,
//     public_inputs: Span<felt252>, 
// }

// // Internal helper to compute the Binary Merkle Root
// fn compute_binary_root(mut nodes: Span<felt252>) -> felt252 {
//     // Base cases
//     if nodes.len() == 0 { return 0; }
//     if nodes.len() == 1 { return *nodes.at(0); }

//     let mut next_level = array![];
//     let mut i = 0;

//     while i < nodes.len() {
//         let left = *nodes.at(i);
        
//         if i + 1 < nodes.len() {
//             // Case: We have a pair
//             let right = *nodes.at(i + 1);
//             next_level.append(left + right);
//         } else {
//             // Case: Odd node at the end of the level
//             // MUST match Python: next_level.append(hash_node(left, left))
//             next_level.append(left + left);
//         }
//         i += 2;
//     };

//     // Recursively calculate the next level
//     compute_binary_root(next_level.span())
// }

// #[executable]
// fn main(
//     global_root: felt252,
//     chunk_roots: Span<felt252>,
//     chunk_proofs: Span<StwoProof>,
// ) -> bool {
//     // 1. Verify Merkle Integrity using Binary Logic
//     let computed_root = compute_binary_root(chunk_roots); 
    
//     assert(computed_root == global_root, 'Merkle Root Mismatch');

//     // 2. Recursive Verification Loop
//     let mut i: usize = 0;
//     while i < chunk_proofs.len() {
//         let current_proof = *chunk_proofs.at(i);
//         let expected_chunk_root = *chunk_roots.at(i);

//         // 3. Link the Proof to the Chunk Root
//         let proof_claimed_root = *current_proof.public_inputs.at(0);
//         assert(proof_claimed_root == expected_chunk_root, 'Proof not for this chunk');

//         i += 1;
//     };

//     true 
// }


use core::array::ArrayTrait;


#[derive(Copy, Drop, Serde)]
struct StwoProof {
    proof_data: Span<felt252>,
    public_inputs: Span<felt252>, 
}

// Internal helper to compute the Binary Merkle Root
fn compute_binary_root(mut nodes: Span<felt252>) -> felt252 {
    // Base cases
    if nodes.len() == 0 { return 0; }
    if nodes.len() == 1 { return *nodes.at(0); }

    let mut next_level = array![];
    let mut i = 0;

    while i < nodes.len() {
        let left = *nodes.at(i);
        
        if i + 1 < nodes.len() {
            // Case: We have a pair
            let right = *nodes.at(i + 1);
            next_level.append(left + right);
        } else {
            // Case: Odd node at the end of the level
            // MUST match Python: next_level.append(hash_node(left, left))
            next_level.append(left + left);
        }
        i += 2;
    };

    // Recursively calculate the next level
    compute_binary_root(next_level.span())
}

#[executable]
fn main(
    global_root: felt252,
    chunk_roots: Span<felt252>,
    chunk_proofs: Span<StwoProof>,
) -> bool {
    // 1. Verify Merkle Integrity using Binary Logic
    let computed_root = compute_binary_root(chunk_roots); 
    
    // --- DEBUG SECTION ---
    // This will print the values to your console during 'scarb execute'
// Using the PrintTrait which works on almost all Cairo versions
    println!("Expected Root: {:?}", global_root);
    println!("Computed Root: {:?}", computed_root);
    // -----------------------------
    // ---------------------

    assert(computed_root == global_root, 'Merkle Root Mismatch');

    // 2. Recursive Verification Loop
    let mut i: usize = 0;
    while i < chunk_proofs.len() {
        let current_proof = *chunk_proofs.at(i);
        let expected_chunk_root = *chunk_roots.at(i);

        // 3. Link the Proof to the Chunk Root
        let proof_claimed_root = *current_proof.public_inputs.at(0);
        assert(proof_claimed_root == expected_chunk_root, 'Proof not for this chunk');

        i += 1;
    };

    true 
}