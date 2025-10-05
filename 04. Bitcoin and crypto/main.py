import json
import hashlib
import binascii
import src.classes as classes

def reverseBytes(data):
    data = bytearray(data)
    data.reverse()
    return data

def sha256d(data):
    hash = hashlib.sha256(data).digest()
    hash2 = reverseBytes(hashlib.sha256(hash).digest())
    return hash2

def read_varint(b: bytes, off: int):
    fb = b[off]; off += 1
    if fb < 0xfd:
        return fb, off
    elif fb == 0xfd:
        val = int.from_bytes(b[off:off+2], 'little'); off += 2
        return val, off
    elif fb == 0xfe:
        val = int.from_bytes(b[off:off+4], 'little'); off += 4
        return val, off
    else:
        val = int.from_bytes(b[off:off+8], 'little'); off += 8
        return val, off
    
def hash160(b: bytes) -> bytes:
    h = hashlib.sha256(b).digest()
    return hashlib.new('ripemd160', h).digest()

def make_p2pkh_from_pubkey(pubkey_bytes: bytes):
    if not pubkey_bytes or len(pubkey_bytes) != 65 or pubkey_bytes[0] != 0x04:
        # Return empty script if the input is not a 65-byte uncompressed pubkey
        return b"", b""
    H = hash160(pubkey_bytes)  # 20 bytes
    # 0x76=OP_DUP, 0xa9=OP_HASH160, 0x14=PUSH(20), 0x88=OP_EQUALVERIFY, 0xac=OP_CHECKSIG
    script = bytes.fromhex('76a914') + H + bytes.fromhex('88ac')
    return script, H

def build_sighash_all_preimage(raw_tx: bytes, pkscript: bytes) -> bytes:
    off = 0
    version = raw_tx[off:off+4]; off += 4
    n_in, off = read_varint(raw_tx, off)

    out = bytearray()
    out += version

    def write_varint(x: int) -> bytes:
        if x < 0xfd: return bytes([x])
        elif x <= 0xffff: return b'\xfd' + x.to_bytes(2, 'little')
        elif x <= 0xffffffff: return b'\xfe' + x.to_bytes(4, 'little')
        else: return b'\xff' + x.to_bytes(8, 'little')

    out += write_varint(n_in)

    # prevout
    prev_txid_le = raw_tx[off:off+32]; off += 32
    prev_vout    = raw_tx[off:off+4];  off += 4

    old_len, off2 = read_varint(raw_tx, off)
    old_scriptSig = raw_tx[off2:off2+old_len]
    off = off2 + old_len
    sequence = raw_tx[off:off+4]; off += 4

    out += prev_txid_le + prev_vout
    assert len(pkscript) == 25
    out += write_varint(25) + pkscript + sequence

    for _ in range(n_in - 1):
        out += raw_tx[off:off+32+4]      # prevout
        off += 32+4
        l, off2 = read_varint(raw_tx, off)
        out += write_varint(l) + raw_tx[off2:off2+l]
        off = off2 + l
        out += raw_tx[off:off+4]         # sequence
        off += 4

    # Outputs + locktime 
    out += raw_tx[off:]  # included n_out, outs and locktime

    # Anex SIGHASH_ALL (LE)
    out += bytes.fromhex('01000000')
    return bytes(out)

def load_raw_block_from_json(path_json: str) -> bytes:
    with open(path_json, 'r') as f:
        data = json.load(f)
    block_id = list(data['data'].keys())[0]
    return bytes.fromhex(data['data'][block_id]['raw_block'])

def split_block_transactions(raw_block: bytes):
    header = raw_block[:80]
    off = 80
    n_tx, off = read_varint(raw_block, off)
    txs = []
    for _ in range(n_tx):
        start = off
        off += 4
        n_in, off = read_varint(raw_block, off)
        for _i in range(n_in):
            off += 32
            off += 4
            slen, off = read_varint(raw_block, off)
            off += slen    # scriptSig
            off += 4 
        # outputs
        n_out, off = read_varint(raw_block, off)
        for _o in range(n_out):
            off += 8       # value
            pklen, off = read_varint(raw_block, off)
            off += pklen   # scriptPubKey
        off += 4           # locktime
        txs.append(raw_block[start:off])
    return txs

# To parser properly the sigscript bytes I used ChatGPT to help me, the other solutions was hardcoded that by the positions informed in the lab
def parse_sigscript_bytes(sigscript: bytes):
    # Expect: 0x48 | DER(0x30 ... len=0x45) | 0x01 | 0x41 | 0x04 || Qx || Qy
    # 0x48 = push de 72 bytes (DER signature + 1 byte SIGHASH)
    assert sigscript[0] == 0x48, "Sig push len expected 0x48"
    sig_len = sigscript[0]
    der = sigscript[1:1+sig_len]
    # DER
    assert der[0] == 0x30, "DER seq expected"
    der_len = der[1]
    der_body = der[2:2+der_len]    
    hash_type = der[2+der_len]       # 1 byte (0x01 = SIGHASH_ALL)

    idx = 0
    assert der_body[idx] == 0x02; idx += 1
    r_len = der_body[idx]; idx += 1
    r = int.from_bytes(der_body[idx:idx+r_len], 'big'); idx += r_len

    assert der_body[idx] == 0x02; idx += 1
    s_len = der_body[idx]; idx += 1
    s = int.from_bytes(der_body[idx:idx+s_len], 'big'); idx += s_len

    # pubkey
    off = 1 + sig_len
    assert sigscript[off] == 0x41, "PubKey push len expected 0x41"
    off += 1
    pub = sigscript[off:off+0x41]    # 65 bytes
    assert pub[0] == 0x04, "Uncompressed pubkey expected"
    Qx = int.from_bytes(pub[1:33], 'big')
    Qy = int.from_bytes(pub[33:65], 'big')
    pubkey_bytes = pub               # 0x04 || Qx || Qy

    return r, s, hash_type, Qx, Qy, pubkey_bytes

# To parser properly the sigscript bytes I used ChatGPT to help me, the other solutions was hardcoded that by the positions informed in the lab
def parse_der_signature(sigscript_hex: str):
    sig_bytes = bytes.fromhex(sigscript_hex)
    assert sig_bytes[0] == 0x48 or sig_bytes[0] == 0x30, "Invalid DER sequence tag"
    total_len = sig_bytes[1]
    idx = 2
    assert sig_bytes[idx] == 0x02, "Invalid integer tag for r"
    idx += 1
    r_len = sig_bytes[idx]
    idx += 1
    r_bytes = sig_bytes[idx:idx+r_len]
    idx += r_len
    assert sig_bytes[idx] == 0x02, "Invalid integer tag for s"
    idx += 1
    s_len = sig_bytes[idx]
    idx += 1
    s_bytes = sig_bytes[idx:idx+s_len]
    idx += s_len
    r = int.from_bytes(r_bytes, byteorder='big')
    s = int.from_bytes(s_bytes, byteorder='big')
    return r, s

def recoverData(filename):
    try:
        with open(filename, 'r') as file:
            block_data = json.load(file)
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None, None
    
    block_id = list(block_data['data'].keys())[0]
    block_raw = bytes.fromhex(block_data['data'][block_id]['raw_block'])
    block_header = block_raw[0:80]
    transactions = block_raw[80+1:]

    return block_id, block_header, transactions

def checkIdBlock(block_id, block_header):
    hash_header = sha256d(block_header)
    return (hash_header.hex() == block_id)
    
def CheckMerkleTree_57043(ids, merkle_root):
    id0_bytes = reverseBytes(ids[0].to_bytes(32, byteorder='big'))
    id1_bytes = reverseBytes(ids[1].to_bytes(32, byteorder='big'))
    concatenated = id0_bytes + id1_bytes
    calculated_root = sha256d(concatenated)
    return calculated_root.hex() == merkle_root

def checkIdTransaction(id, transaction):
    hash_transaction = sha256d(transaction).hex()
    id_bytes = id.to_bytes(32, byteorder='big')
    return (id_bytes.hex() == hash_transaction)

def recoverDataFromHeader(block_header):
    block_reader_data = []
    print("=========== BLOCK HEADER ==========")
    print(f"blockVersion    : {reverseBytes(block_header[:4]).hex()}")
    block_reader_data.append(reverseBytes(block_header[:4]).hex())
    print(f"idPreviousBlock : {reverseBytes(block_header[4:32+4]).hex()}")
    block_reader_data.append(reverseBytes(block_header[4:32+4]).hex())
    print(f"MerkleRoot      : {reverseBytes(block_header[32+4:64+4]).hex()}")
    block_reader_data.append(reverseBytes(block_header[32+4:64+4]).hex())
    print(f"timestamp       : {reverseBytes(block_header[64+4:64+8]).hex()}")
    block_reader_data.append(reverseBytes(block_header[64+4:64+8]).hex())
    print(f"bits            : {reverseBytes(block_header[72:72+4]).hex()}")
    block_reader_data.append(reverseBytes(block_header[72:72+4]).hex())
    print(f"nonce           : {reverseBytes(block_header[72+4:72+8]).hex()}")
    block_reader_data.append(reverseBytes(block_header[72+4:72+8]).hex())

    return block_reader_data

def checkTransactions():
    # secp256k1
    p_ecp256k1 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    a_ecp256k1 = 0
    b_ecp256k1 = 7
    Px = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
    Py = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
    N_ecp256k1 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

    ecp256k1 = classes.SubGroup(
        l="ECConZp", e=0, N=N_ecp256k1, p=p_ecp256k1, g=[Px, Py], A=a_ecp256k1, B=b_ecp256k1
    )

    raw_block_57044 = load_raw_block_from_json('./docs/tp4/block_57044.json')
    txs_57044 = split_block_transactions(raw_block_57044)
    if len(txs_57044) != 2:
        print("Unexpected number of transactions in block 57044.")
        return False

    target_tx = txs_57044[1]  # tx with one input

    txid_target_be = "cca7507897abc89628f450e8b1e0c6fca4ec3f7b34cccf55f3f531c659ff4d79"
    ok_txid = checkIdTransaction(int(txid_target_be, 16), target_tx) 
    print(f"TXID target ok?            {ok_txid}")

    # scriptSig
    off = 0
    off += 4  # version
    n_in, off = read_varint(target_tx, off)
    if n_in is None or n_in < 1:
        print("Invalid n_in in target transaction.")
        return False

    off += 32  # prev txid
    off += 4   # vout
    siglen, p = read_varint(target_tx, off)
    if siglen is None:
        print("Could not read scriptSig length.")
        return False
    if p + siglen > len(target_tx):
        print("scriptSig length exceeds transaction size.")
        return False

    sigscript = target_tx[p:p+siglen]
    off = p + siglen
    off += 4   # sequence

    r, s, hash_type, Qx, Qy, pubkey_bytes = parse_sigscript_bytes(sigscript)
    if r is None:
        print("Failed to parse scriptSig.")
        return False
    print("hash_type (sighash):     0x%02x" % hash_type)

    on_curve = ecp256k1.verify([Qx, Qy])
    print(f"Q is in secp256k1?     {on_curve}")

    pkscript, H = make_p2pkh_from_pubkey(pubkey_bytes)
    if not pkscript:
        print("Could not build P2PKH script from pubkey.")
        return False
    print("H (hash160(pubkey))      :", H.hex())

    preimage = build_sighash_all_preimage(target_tx, pkscript)
    if not preimage:
        print("Failed to build SIGHASH_ALL preimage.")
        return False

    digest_be = hashlib.sha256(hashlib.sha256(preimage).digest()).digest()
    got = digest_be.hex()
    print("Hash preimage (BE)       :", got)
    print("Hash expected (BE)       : c2d48f45d7fbeff644ddb72b0f60df6c275f0943444d7df8cc851b3d55782669")

    m = int.from_bytes(digest_be, 'big') % N_ecp256k1
    ok_sig = ecp256k1.ecdsa_verif(m=m, signature=(r, s), pb_key=[Qx, Qy], debug=False)
    print(f"ECDSA Verify        : {ok_sig}")
    return ok_sig

def checkHeader():
    block_id, block_header, transactions = recoverData('./docs/tp4/block_57043.json')
    first_transaction = transactions[:134]
    second_transaction = transactions[134:]
    ids = [0xbd9075d78e65a98fb054cb33cf0ecf14e3e7f8b3150231df8680919a79ac8fe5,
           0xa1075db55d416d3ca199f55b6084e2115b9345e16c5cf302fc80e9d5fbf5d48d]
    
    if block_id and block_header:
        print("========= BLOCK DATA INFO =========")
        print(f"Block ID     : {block_id}")
        print(f"Block Header : {block_header.hex()}")

    block_reader_data = recoverDataFromHeader(block_header)
    print("========= CHECK BLOCK INFO ========")
    print(f"CheckIdBlock            : {checkIdBlock(block_id, block_header)}")
    print(f"CheckMerkleRoot         : {CheckMerkleTree_57043(ids, block_reader_data[2])}")
    print(f"checkIdTransaction 1    : {checkIdTransaction(ids[0], first_transaction)}")
    print(f"checkIdTransaction 2    : {checkIdTransaction(ids[1], second_transaction)}")
    checkTransactions()

if __name__ == "__main__":   
    checkHeader()