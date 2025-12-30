use core::array::Span;

#[derive(Copy, Drop)]
struct Counts {
    severity_total: felt252,
    facility_total: felt252,
}

fn process_chunk(
    chunk_root: felt252,
    num_lines: felt252,
    line_hashes: Span<felt252>,
    severity_counts: Span<felt252>,
    facility_counts: Span<felt252>,
) -> Counts {
    // -----------------------------
    // 1️⃣ Recompute chunk Merkle root
    // -----------------------------
    assert(line_hashes.len() > 0, 'Empty chunk');

    let mut computed_root = *line_hashes.at(0);
    let mut i: usize = 1;

    while i < line_hashes.len() {
        computed_root = computed_root + *line_hashes.at(i);
        i += 1;
    }

    assert(computed_root == chunk_root, 'Merkle root mismatch');

    // -----------------------------
    // 2️⃣ Verify severity counts
    // -----------------------------
    let mut total_severity: felt252 = 0;
    let mut s: usize = 0;

    while s < severity_counts.len() {
        total_severity += *severity_counts.at(s);
        s += 1;
    }

    assert(total_severity == num_lines, 'Severity count mismatch');

    // -----------------------------
    // 3️⃣ Verify facility counts
    // -----------------------------
    let mut total_facility: felt252 = 0;
    let mut f: usize = 0;

    while f < facility_counts.len() {
        total_facility += *facility_counts.at(f);
        f += 1;
    }

    assert(total_facility == num_lines, 'Facility count mismatch');

    Counts {
        severity_total: total_severity,
        facility_total: total_facility,
    }
}
