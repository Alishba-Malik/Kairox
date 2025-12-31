// use core::array::Span;

// #[derive(Copy, Drop)]
// struct Counts {
//     severity_total: felt252,
//     facility_total: felt252,
// }

// fn process_chunk(
//     chunk_root: felt252,
//     num_lines: felt252,
//     line_hashes: Span<felt252>,
//     severity_counts: Span<felt252>,
//     facility_counts: Span<felt252>,
// ) -> Counts {
//     // -----------------------------
//     // 1️⃣ Recompute chunk Merkle root
//     // -----------------------------
//     assert(line_hashes.len() > 0, 'Empty chunk');

//     let mut computed_root = *line_hashes.at(0);
//     let mut i: usize = 1;

//     while i < line_hashes.len() {
//         computed_root = computed_root + *line_hashes.at(i);
//         i += 1;
//     }

//     assert(computed_root == chunk_root, 'Merkle root mismatch');

//     // -----------------------------
//     // 2️⃣ Verify severity counts
//     // -----------------------------
//     let mut total_severity: felt252 = 0;
//     let mut s: usize = 0;

//     while s < severity_counts.len() {
//         total_severity += *severity_counts.at(s);
//         s += 1;
//     }

//     assert(total_severity == num_lines, 'Severity count mismatch');

//     // -----------------------------
//     // 3️⃣ Verify facility counts
//     // -----------------------------
//     let mut total_facility: felt252 = 0;
//     let mut f: usize = 0;

//     while f < facility_counts.len() {
//         total_facility += *facility_counts.at(f);
//         f += 1;
//     }

//     assert(total_facility == num_lines, 'Facility count mismatch');

//     Counts {
//         severity_total: total_severity,
//         facility_total: total_facility,
//     }
// }

//use core::array::{ArrayTrait, SpanTrait}; // Required for .at() and .len()
// use core::poseidon::poseidon_hash_span;

#[derive(Copy, Drop, Serde)]
struct Output {
}

#[executable]
fn main(
    chunk_root: felt252,
    num_lines: felt252,
    severity_counts: Span<felt252>,
    facility_counts: Span<felt252>,
    
) -> Output {
    // -----------------------------
    // 1. Verify severity totals
    // -----------------------------
    let mut sev_sum: felt252 = 0;
    let mut i: usize = 0;
    while i < severity_counts.len() {
        sev_sum += *severity_counts.at(i);
        i += 1;
    };
    assert(sev_sum == num_lines, 'Severity sum mismatch');

    // -----------------------------
    // 2. Verify facility totals
    // -----------------------------
    let mut fac_sum: felt252 = 0;
    let mut j: usize = 0;
    while j < facility_counts.len() {
        fac_sum += *facility_counts.at(j);
        j += 1;
    };
    assert(fac_sum == num_lines, 'Facility sum mismatch');
    let _ = chunk_root;

    Output {}
}

//     // -----------------------------
//     // 3. Verify stats commitment
//     // -----------------------------
//     let mut combined: Array<felt252> = ArrayTrait::new();
    
//     // Manually move elements into the Array to be hashed
//     let mut k: usize = 0;
//     while k < severity_counts.len() {
//         combined.append(*severity_counts.at(k));
//         k += 1;
//     };
//     let mut l: usize = 0;
//     while l < facility_counts.len() {
//         combined.append(*facility_counts.at(l));
//         l += 1;
//     };

//     let computed_commitment = poseidon_hash_span(combined.span());
    
//     // This will check if your Python-calculated hash matches the Cairo one
//     assert(
//         computed_commitment == stats_commitment,
//         'Stats commitment mismatch'
//     );

//     Output { stats_commitment: computed_commitment }
// }
