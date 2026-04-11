import hashlib
import json
import time

def hash_block(block):
    block_copy = {k: v for k, v in block.items() if k != 'hash'}
    block_string = json.dumps(block_copy, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def create_block(index, data, prev_hash, nonce=0):
    block = {
        'index': index,
        'timestamp': time.time(),
        'data': data,
        'prev_hash': prev_hash,
        'nonce': nonce
    }
    block['hash'] = hash_block(block)
    return block

def mine_block(index, data, prev_hash, difficulty=3):
    target = '0' * difficulty
    nonce = 0
    while True:
        block = create_block(index, data, prev_hash, nonce)
        if block['hash'].startswith(target):
            print(f"Mined block {index} with nonce {nonce}")
            return block
        nonce += 1

genesis = create_block(0, "Genesis Block", "0")
block1 = mine_block(1, "Alice -> Bob 10", genesis['hash'])
block2 = create_block(2, "Bob -> Carol 5", block1['hash'])

chain = [genesis, block1, block2]

def is_chain_valid(chain):
    for i in range(1, len(chain)):
        if chain[i]['prev_hash'] != chain[i-1]['hash']:
            return False
    return True

print("Blockchain valid:", is_chain_valid(chain))
