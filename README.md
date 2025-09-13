# Advanced Cryptography Practical Projects
Vinicius Nascimento <br>

This repository will host a series of practical labs for **Advanced Cryptography** (ENSICAEN — 3A Informatique, CyIA, 2025). Each lab focuses on a specific cryptographic building block or algorithm.  

## Table of Contents

1. [Finite Fields & Groups (Lab 1)](#1-finite-fields--groups-lab-1)  
2. [Elliptic Curves & ECDSA (Lab 2)](#2-elliptic-curves--ecdsa-lab-2)

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
cd 01. Finite-fields-and-groups
python3 tests.py
```

The script runs all verifications in the assignment’s order (Parts 1 to 5).

---

### 2. Elliptic Curves & ECDSA (Lab 2)

**Folder name:** `02. Elliptic-curves-and-ecdsa`

**Objective:**  
Work with elliptic curves over prime fields (P-256) to implement the group law, Diffie–Hellman key exchange, and ECDSA (sign/verify), including validation with NIST test vectors and OpenSSL interoperability.

**How to Run:**  
Inside the lab folder:
```bash
cd 02. Elliptic-curves-and-ecdsa
python3 test.py
```

The script executes the verifications in order (Lab2 parts 1 and 2).

To generate Alice’s key pair and sign the PDF:
```bash
openssl ecparam -name prime256v1 -genkey -outform DER -out docs/ecdhkeyAlice.der
openssl dgst -sha256 -sign docs/ecdhkeyAlice.der -out docs/Lab2.pdf.sig docs/Lab2.pdf
openssl dgst -sha256 -verify <(openssl ec -inform DER -in docs/ecdhkeyAlice.der -pubout) \
    -signature docs/Lab2.pdf.sig docs/Lab2.pdf
```
---

Summary

This project covers foundational and advanced cryptography topics:
- Lab 1: Algebraic structures, Montgomery Ladder, Diffie–Hellman, DLP.
- Lab 2: Elliptic curves (P-256), certificate verification, ECDH, and ECDSA.
Each lab includes its own README, source files in src/, and test scripts to reproduce the results.