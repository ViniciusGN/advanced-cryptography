# Advanced Cryptography Practical Projects
Vinicius Nascimento <br>

This repository will host a series of practical labs for **Advanced Cryptography** (ENSICAEN — 3A Informatique, CyIA, 2025). Each lab focuses on a specific cryptographic building block or algorithm.  

## Table of Contents

1. [Finite Fields & Groups (Lab 1)](#1-finite-fields--groups-lab-1)

---

### 1. Finite Fields & Groups (Lab 1)

**Folder name:** `01. Finite-fields-and-groups`

**Objective:**  
Implement core algebraic primitives used in cryptography: group operations over **ℤp** (additive/multiplicative) and **𝔽₂ⁿ**, a generic **Montgomery Ladder** exponentiation, **Diffie–Hellman** checks, and **Discrete Logarithm** solvers (trial multiplication and **Baby-Step Giant-Step**).

**Key Features:**
- Unified group interface (`Group`, `SubGroup`) with a single `law`:
  - ℤp (additive): `(a + b) mod p`, identity `0`
  - (ℤp)× (multiplicative): `(a * b) mod p`, identity `1`
  - 𝔽₂ⁿ (multiplicative): Russian-style multiply with reduction by the irreducible polynomial (`poly`), identity `1`
- Generic **exp** via Montgomery Ladder (works across all supported groups; handles negative exponents mod N)
- **Diffie–Hellman**: randomized check and deterministic validator
- **DLP**: `DLbyTrialMultiplication`, `DLbyBabyStepGiantStep`, and `ComputeDL(τ)` dispatcher

**How to Run:**  
Inside the lab folder:
```bash
cd lab1-finite-fields-and-groups
python3 tests.py
```

The script runs all verifications in the assignment’s order (Parts 1 to 5).

**Files:**
- `classes.py` — class implementations
- `tests.py` — ordered checks and prints
- `lab1_utils.py` — provided helper (no changes required)

## Summary

This project covers foundational cryptography topics:

- **Algebraic Structures:** groups over ℤp and fields 𝔽₂ⁿ  
- **Exponentiation:** Montgomery Ladder (constant-shape)  
- **Key Exchange:** Diffie–Hellman property validation  
- **Hard Problems:** Discrete Logarithm in practice (trial vs. BSGS)

More labs will be added over time, each lab includes its own README and runnable tests.
