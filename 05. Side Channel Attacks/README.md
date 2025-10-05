# Advanced Cryptography — Lab 2 (Side-Channel Attacks: SPA & CPA)

**Author:** Vinicius MOREIRA NASCIMENTO — ENSICAEN, 3A Informatique (CyIA), 2025  
**Course:** Advanced Cryptography  
**Topics:** Side-Channel Attacks on cryptographic implementations — SPA on scalar multiplication (double-and-add) and CPA on AES first round (SubBytes).

## Files Structure

- `attack_notebook.ipynb`  
  Contains both parts of the lab:
  - **Part 1 — SPA Attack (Simple Power Analysis)**  
    - Based on the *Double and Add* challenge from CryptoHack (Elliptic Curves → Side Channel).  
    - Processes a collected trace of scalar multiplications on secp256k1.  
    - Extracts operation patterns, reconstructs the bitstring, adjusts bit order and padding, and recovers the secret scalar / flag.
  - **Part 2 — CPA Attack (Correlation Power Analysis)**  
    - Loads `traces.npy` and `plaintext.npy` (AES power traces and plaintexts).  
    - Implements a **Hamming-weight leakage model** on S-box outputs after the first SubBytes.  
    - Computes Pearson-like correlation for each key-byte hypothesis (0–255).  
    - Recovers the 16-byte AES key and compares it with the expected value from the exercise.

- `traces.npy` — AES power traces (N=50, N₀=9996 samples each).  
- `plaintext.npy` — plaintexts used for the AES encryptions (16 bytes each).  
- *(optional)* `collected_data.txt` — raw scalar-multiplication dump used for the SPA challenge.

## How to run

From the notebook environment (Python 3.x):

```bash
jupyter notebook attack_notebook.ipynb
```

Then:

1. Run all cells.  
2. **Part 1 (SPA):** prints the extracted bitstring and recovered flag.  
3. **Part 2 (CPA):** prints  

```bash
Recovered key (hex): 98a90ac6a2bc26493c3be04b113555d4
Expected key (hex): 98a90ac6a2bc26493c3be04b113555d4
Match: True 
```


## Requirements

- Python ≥ 3.8  
- numpy  

Install if needed:
```bash
pip install numpy
```

## Notes

- The sbox is kept as a Python list (no conversion needed).
- Only core computations are included — no plots or extra outputs.
- The notebook is minimal and follows exactly the specifications of the lab statement.