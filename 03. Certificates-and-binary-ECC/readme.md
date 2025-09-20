# Advanced Cryptography — Lab 3 (Certificates & ECC over F2^n)

**Author:** Vinicius MOREIRA NASCIMENTO — ENSICAEN, 3A Informatique (CyIA), 2025  
**Course:** Advanced Cryptography  
**Topics:** X.509 certificate parsing & ECDSA (P-384), elliptic curves over \( \mathbb{F}_{2^{163}} \) (B-163), EC Diffie–Hellman, ECDSA over binary fields.

## Project structure

- `src/classes.py`  
  Implements `Group` and `SubGroup` with:
  - Prime-field EC (`ECConZp`) including group law, scalar multiplication, point verify, DH, ECDSA.
  - **Binary-field EC (`ECC_F2^n`)**: group law on curves of the form \( y^2 + x y = x^3 + a x^2 + b \)  
    (B-163: \(a=1\), irreducible poly \(x^{163}+x^7+x^6+x^3+1\)), scalar multiplication, point verify, DH, ECDSA.

- `src/lab1_utils.py`  
  Helpers for finite-field operations (provided by the course).

- `tests.py`  
  - `testLab3_part1()`:  
    *Certificate & ECDSA (P-384)* — extracts Wikipedia’s certificate, parses DER, isolates “to-be-signed” bytes, hashes with SHA-384, parses ECDSA `(t,s)` and verifies the signature using the CA’s public key (P-384).
  - `testLab3_part2()`:  
    *B-163 over \( \mathbb{F}_{2^{163}} \)* — completes the binary-field group law; runs `verify([Gx,Gy])`, EC Diffie–Hellman, and ECDSA sign/verify on the message `"Example of ECDSA with B-163"` (SHA-1).

- `docs/` (inputs/outputs used by the scripts)
  - `wikipedia-org.pem`, `wikipedia.der` — Wikipedia certificate (PEM/DER).
  - `E6.der`, `e6-wikipedia.pem` — CA certificate used to verify Wikipedia’s signature.
  - `google.pem`, `google.der` — extra certificate set kept from Lab 2.
  - `ecdhkeyAlice.der`, `AlicePub.pem` — Alice’s EC keypair (from previous lab, for OpenSSL demos).
  - `b163key.der` — B-163 private key generated via OpenSSL (for inspection).
  - `Lab2.sig` — signature example (from previous lab, kept for reference).

> **Note:** *Part 3. X25519 curve and RSA key generation with backdoor (alternative to parts 2 and 3) — **not implemented** in this submission.*

## How to run

From the project root (Python 3.x):
```bash
python3 test.py
```

The script executes:
1) `testLab3_part1()` — Certificate parsing and ECDSA verification on **P-384** (Wikipedia’s certificate, signed by CA E6).  
2) `testLab3_part2()` — Binary-field elliptic curve **B-163**: verifies the base point G, runs EC Diffie–Hellman, and performs ECDSA sign/verify on `"Example of ECDSA with B-163"`.

## OpenSSL usage (what was used in Part 1 & Part 2)

### Part 1 — Certificate parsing & DER/SHA-384
```bash
# Display certificate info (PEM)
openssl x509 -in docs/wikipedia-org.pem -text -noout

# Convert to DER
openssl x509 -in docs/wikipedia-org.pem -outform DER -out docs/wikipedia.der

# (Optional) Hex-dump the DER (Linux/macOS)
xxd docs/wikipedia.der | more -1
# On Windows, use:
#   certutil -encodehex docs/wikipedia.der stdout
```

### Part 2 — B-163 key (just for inspection) and curve checks
```bash
# Generate a B-163 key (sect163r2) in DER
openssl ecparam -outform DER -out docs/b163key.der -name sect163r2 -genkey

# Inspect the key (text dump)
openssl ec -inform DER -in docs/b163key.der -text -noout
```
---