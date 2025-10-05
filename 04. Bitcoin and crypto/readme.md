# Advanced Cryptography — Lab 4 (Bitcoin Blocks, ECDSA, and secP256k1)

**Author:** Vinicius MOREIRA NASCIMENTO — ENSICAEN, 3A Informatique (CyIA), 2025  
**Course:** Advanced Cryptography  
**Topics:** Bitcoin block header (80 bytes), endianness, Merkle root, TXID (SHA-256d), scriptSig/scriptPubKey (P2PKH), SIGHASH_ALL preimage, ECDSA verification on secp256k1.

## Project structure

- `src/classes.py`  
  Reused from previous labs. Implements `Group` / `SubGroup` with:
  - EC over prime fields (`ECConZp`): group law, scalar multiplication, point verify, Diffie–Hellman, **ECDSA (sign/verify)**.
  - (Binary-field EC kept from earlier labs; not central here.)

- `src/lab1_utils.py`  
  Helpers for finite-field operations used by `classes.py` (provided by the course).

- `main.py`  
  Implements the Lab 4 flow:
  - **Block 57043 parsing and verification**  
    - `recoverData()` reads JSON (Blockchair), extracts **block id**, **header (80 bytes)** and **raw block**.  
    - `recoverDataFromHeader()` prints **version, prev_id, merkle_root, timestamp, bits, nonce** (with endianness fixes).  
    - `checkIdBlock()` validates **block id** = SHA-256d(header).  
    - `CheckMerkleTree_57043()` reconstructs the **Merkle root** from the two txids (pizza + coinbase).  
    - `checkIdTransaction()` checks **TXID** = SHA-256d(raw_tx).
  - **Block 57044 transaction verification (1 input)**  
    - `load_raw_block_from_json()` + `split_block_transactions()` extract the **two transactions**.  
    - `parse_sigscript_bytes()` extracts **(r, s)** and the **public key Q = (Qx, Qy)** (uncompressed 65 bytes).  
    - `make_p2pkh_from_pubkey()` builds **scriptPubKey P2PKH** from `Q` using **HASH160** (SHA-256 → RIPEMD-160).  
    - `build_sighash_all_preimage()` replaces the first input’s scriptSig by `pkscript`, appends `01000000` (**SIGHASH_ALL**), and computes **SHA-256d** of the preimage.  
    - Verifies that the preimage hash is  
      `c2d48f45d7fbeff644ddb72b0f60df6c275f0943444d7df8cc851b3d55782669`  
      and checks the **ECDSA signature** with `SubGroup.ecdsa_verif`.

- `docs/tp4/`  
  - `block_57043.json` — raw block #57043.  
  - `block_57044.json` — raw block #57044 (the 1-input transaction).

## How to run

From the project root (Python 3.x):

```bash
python3 main.py
```

The script prints verification steps for blocks 57043 and 57044, including block id, Merkle root, TXIDs, pubkey check on secp256k1, preimage hash, and ECDSA verification.