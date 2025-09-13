# Practical Work 2 — Advanced Cryptography (Elliptic Curves & ECDSA)

Advanced Cryptography — **Elliptic Curves and Digital Signatures**  <br>
Vinicius MOREIRA NASCIMENTO — ENSICAEN, 3A Informatique (CyIA), 2025

## Overview
This project implements elliptic curve primitives over prime fields and demonstrates their cryptographic use on the standardized curve **P-256**:
- Group law for elliptic curves over **ℤp** (P-256 parameters).
- **Point verification** on the curve.
- **Diffie–Hellman** key exchange over elliptic curves.
- **ECDSA** (Elliptic Curve Digital Signature Algorithm): signing and verification.
- Integration with **OpenSSL**: extracting public keys from certificates, generating keys, signing and verifying real files.

All tests follow the parts described in the assignment PDF and run from a single script.

## Project Structure
. <br>
├── README.md <br>
├── src/ <br>
│   ├── classes.py <br>
│   └── lab1_utils.py <br>
├── test.py <br>
├── docs/ <br>
│   ├── google.pem / google.der <br>
│   ├── ecdhkeyAlice.der <br>
│   ├── AlicePub.pem / AlicePub.der <br>
│   ├── Lab2.pdf <br>
│   └── Lab2.sig <br>
└── lab2.pdf <br>

- `src/classes.py`: defines `Group` and `SubGroup` with elliptic curve support (`ECConZp`), point addition/doubling, exponentiation (Montgomery Ladder), Diffie–Hellman checks, and ECDSA sign/verify.
- `src/lab1_utils.py`: utility file from Lab01, reused here.
- `test.py`: runs the checks in order:
  - **Part 1**: verifies Google’s public key lies on P-256 and runs Diffie–Hellman.  
  - **Part 2**: reproduces the NIST ECDSA test vector for P-256 (sign & verify).  
  - (Optional) can use Alice’s key to sign `Lab2.pdf` and verify the signature.
- `docs/`: supplementary files (Google certificate, Alice’s keys, PDF and signature).
- `lab2.pdf`: assignment description.

## Execution
Open a terminal in the repository folder and run:
```bash
python3 test.py
```
The script executes the verifications in order (Lab2 parts 1 and 2).  
Files in `docs/` are used for certificate parsing and OpenSSL interoperability.

## Components

**1) Group Law on P-256 (`classes.py`)**  
- Implements the algorithm from the slides:
  - Identity, opposite points, point doubling, and point addition.
- Inversion is done with `pow(..., -1, p)`.

**2) Diffie–Hellman**  
- `testDiffieHellman()` checks `A^b == B^a` over the elliptic curve.

**3) ECDSA**  
- `ecdsa_sign(m, sk, debug)` — computes `(t, s)` given message hash `m` and private key `sk`.  
- `ecdsa_verif(m, (t,s), pk, debug)` — verifies signatures, printing intermediate values (`t1`, `t2`, `Q1.x`, `Q2.x`) in debug mode.  
- Tested against the official **NIST P-256/SHA-256 vector**.

**4) OpenSSL Integration**  
- `docs/google.pem/der`: used to extract Google’s public key and check it lies on P-256.  
- `docs/ecdhkeyAlice.der`: private key generated for Alice.  
- `docs/AlicePub.pem/der`: Alice’s public key, extracted from DER.  
- `docs/Lab2.pdf`: assignment document.  
- `docs/Lab2.sig`: signature of `Lab2.pdf` created with Alice’s private key.

## Features

- Full support for elliptic curve arithmetic on **P-256**.  
- Implementation of **ECDSA** with optional debug for NIST test vectors.  
- Reuse of Lab01 structure (`Group`, `SubGroup`, `lab1_utils`).  
- Supplementary OpenSSL workflow for certificate parsing and real file signatures.

## Example Output
```bash
message m is:  Example of ECDSA with P-256
Hash of m is:  <sha256 as int>
t is correct?  True
s is correct?  True
Public key Q is on curve?  True
t1 ok?    True
t2 ok?    True
Q1.x ok?  True
Q2.x ok?  True
ECDSA verif -> True
ECDSA verify OK?  True
```

## Notes

- Python implementation demonstrates the mathematics of elliptic curves and ECDSA.
- OpenSSL commands are used to generate keys and sign `Lab2.pdf` for interoperability.
- Supplementary files (`.pem`, `.der`, `.sig`, `.pdf`) are kept under docs/.