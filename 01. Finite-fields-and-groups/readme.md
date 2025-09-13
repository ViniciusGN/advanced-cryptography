# Practical Work 1 — Advanced Cryptography (Finite Fields & Groups)

Advanced Cryptography — **Group Operations and DLP**  <br>
Vinicius MOREIRA NASCIMENTO — ENSICAEN, 3A Informatique (CyIA), 2025

## Overview
This project implements core algebraic primitives used in cryptography:
- Groups over **ℤp** (additive and multiplicative).
- Binary fields **𝔽₂ⁿ** with polynomial reduction (e.g., 𝔽₂⁸ with `x⁸+x⁴+x³+x+1`).
- **Montgomery Ladder** exponentiation (generic via group law).
- **Diffie–Hellman** key agreement checks.
- **Discrete Logarithm** via **trial multiplication** and **Baby-Step Giant-Step (BSGS)**.

All tests follow the five parts described in the assignment PDF and run in order from a single script.

## Project Structure
. <br>
├── README.md <br>
├── classes.py <br>
├── tests.py <br>
├── lab1_utils.py  <br>
└── lab1.pdf <br>

- `classes.py`: defines `Group` and `SubGroup`, the group laws for `"ZpAdditive"`, `"ZpMultiplicative"`, and `"F2^n"`, the generic `exp` (Montgomery Ladder), Diffie–Hellman checks, DLP (trial + BSGS), and the `ComputeDL` dispatcher.
- `tests.py`: prints the verifications **in the same order as the five parts** of the assignment; run this file to execute everything.
- `lab1_utils.py`: provided by the exercise (helpers for binary fields); **no changes required**.

## Execution
Open a terminal in the repository folder and run:
```bash
python3 tests.py
```

The script will execute all checks in order (Parts 1 to 5) without additional setup. Optionally, set a seed for reproducible runs (add at the top of `tests.py`):
```bash
import random
random.seed(42)
```

## Components

**1) Group & SubGroup (`classes.py`)**  
Generic group abstraction with a single `law`:
- **ℤp (additive)**: `(a + b) mod p`, identity `0`.
- **(ℤp)× (multiplicative)**: `(a * b) mod p`, identity `1`.
- **𝔽₂ⁿ (multiplicative)**: Russian-style multiply with reduction by the irreducible polynomial (`poly`), identity `1`.

**2) Exponentiation (Montgomery Ladder)**  
Constant-shape algorithm using only `law`, works across all supported groups. Handles negative exponents via `k %= N`.

**3) Diffie–Hellman**  
- `testDiffieHellman()` (random a,b) checks whether `A^b == B^a`.
- `DiffieHellman(a,b,A,B,K)` (deterministic) verifies `A=g^a`, `B=g^b`, and `K=A^b=B^a`.

**4) Discrete Logarithm (DLP)**  
- `DLbyTrialMultiplication(h)` — O(N) scan using the group law.
- `DLbyBabyStepGiantStep(h)` — O(√N) giant-table variant aligned with the course slides.
- `ComputeDL(h, τ)` — dispatcher: uses trial if `N ≤ τ`, otherwise BSGS.

## Features

- Unified group interface for **ℤp** (add/mul) and **𝔽₂ⁿ**.
- Clean separation of **law** and **exp** for portability and reuse.
- **BSGS** implemented exactly as specified in the slides (precompute `g^(i·w)`).
- Single command test runner (`python3 tests.py`) that follows the assignment’s 5 parts in order.

## Example Output
```bash
First Verification:
testDiffieHellman: True
True

Second Verification:
198
In F256 : 45 * 72 == 198 ? True
h value computed by exp() : 193
DL Function value : 178
i value : 178

Third Verification:
testDiffieHellman: True

Fourth Verification:
ComputeDL (tau=100) value : 222
i value : 222
```

## Notes

- `lab1_utils.py` is instructor-provided; keep it alongside `classes.py` and `tests.py`.
- All class implementations are in `classes.py`.
- Running `tests.py` is sufficient to validate all five parts in sequence.