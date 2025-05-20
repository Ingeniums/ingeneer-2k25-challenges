#!/usr/bin/env python3
import numpy as np

BLOCK_SIZE = 32
FLAG_LEN = 48

# Your encrypted flag bytes
encrypted_flag = [
    0x22, 0xE1, 0x50, 0xA4, 0x54, 0x8C, 0xDD, 0xA4,
    0x22, 0xFB, 0x9E, 0xFE, 0x03, 0x0B, 0x9B, 0x77,
    0xCE, 0xB5, 0x84, 0x59, 0xCE, 0x45, 0xD4, 0x7F,
    0xA9, 0xB4, 0x8F, 0x36, 0xB1, 0xAE, 0x6E, 0xE3,
    0x0F, 0x9F, 0x3F, 0x83, 0x00, 0xC8, 0xDD, 0xA8,
    0xE3, 0x83, 0xBB, 0x95, 0xEF, 0xC1, 0x15, 0xAD
]

key = [
    0x13, 0x37, 0xBA, 0xAD, 0xC0, 0xDE, 0xFE, 0xED,
    0xBE, 0xEF, 0xFA, 0xCE, 0xCA, 0xFE, 0x42, 0x42,
    0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80,
    0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0x00
]

# Encryption functions (for reference and testing)
def xor_layer(data, key):
    result = bytearray(len(data))
    for i in range(0, len(data), BLOCK_SIZE):
        for j in range(min(BLOCK_SIZE, len(data) - i)):
            result[i + j] = data[i + j] ^ key[j % len(key)]
    return result

def prime_block_shuffle(data):
    block_sizes = [7, 11, 13]
    bs = block_sizes[(data[0] + data[FLAG_LEN-1]) % 3]
    temp = bytearray(FLAG_LEN)
    
    for i in range(FLAG_LEN):
        new_pos = (i * bs) % FLAG_LEN
        temp[new_pos] = data[i]
    
    return temp

def feistel_shuffle(data, rounds):
    result = bytearray(data)
    for r in range(rounds):
        for i in range(FLAG_LEN // 2):
            left = result[i]
            right = result[i + FLAG_LEN // 2]
            result[i] = right
            result[i + FLAG_LEN // 2] = left ^ (right % 256)
    return result

def matrix_shuffle(data):
    rows = 6
    cols = (FLAG_LEN + rows - 1) // rows
    temp = bytearray(FLAG_LEN)
    
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            if idx < FLAG_LEN:
                temp[j * rows + i] = data[idx]
    
    return temp

# Decryption functions (reversing the encryption operations)
def inverse_matrix_shuffle(data):
    rows = 6
    cols = (FLAG_LEN + rows - 1) // rows
    temp = bytearray(FLAG_LEN)
    
    for i in range(rows):
        for j in range(cols):
            idx = j * rows + i
            if idx < FLAG_LEN:
                temp[i * cols + j] = data[idx]
    
    return temp

def inverse_feistel_shuffle(data, rounds):
    result = bytearray(data)
    for r in range(rounds):
        # Run the Feistel network in reverse
        for i in range(FLAG_LEN // 2 - 1, -1, -1):
            right = result[i]
            left_xor_f = result[i + FLAG_LEN // 2]
            left = left_xor_f ^ (right % 256)
            result[i] = left
            result[i + FLAG_LEN // 2] = right
    return result

def inverse_prime_block_shuffle(data):
    # We need to find the block size first, which depends on the original data
    # We'll have to try all possibilities
    block_sizes = [7, 11, 13]
    
    # We'll try all three possible block sizes
    for bs in block_sizes:
        temp = bytearray(FLAG_LEN)
        # Calculate the modular multiplicative inverse of bs mod FLAG_LEN
        # This allows us to reverse the operation (i * bs) % FLAG_LEN
        bs_inverse = pow(bs, -1, FLAG_LEN)
        
        # Apply the inverse shuffle
        for i in range(FLAG_LEN):
            orig_pos = (i * bs_inverse) % FLAG_LEN
            temp[orig_pos] = data[i]
        
        # Check if this is potentially the right block size by seeing if it matches
        # the expected criteria when re-encrypted
        if (temp[0] + temp[FLAG_LEN-1]) % 3 == block_sizes.index(bs):
            return temp
    
    # If we can't determine the right block size, return the most likely option
    # Default to the first block size if we can't determine
    bs = block_sizes[0]
    bs_inverse = pow(bs, -1, FLAG_LEN)
    temp = bytearray(FLAG_LEN)
    for i in range(FLAG_LEN):
        orig_pos = (i * bs_inverse) % FLAG_LEN
        temp[orig_pos] = data[i]
    
    return temp

# Solve the challenge by reversing all the operations
def solve_challenge():
    # Start with the encrypted flag
    data = bytearray(encrypted_flag)
    
    # Reverse the matrix shuffle
    data = inverse_matrix_shuffle(data)
    print("After inverse matrix shuffle:", bytes(data))
    
    # Reverse the Feistel network (3 rounds)
    data = inverse_feistel_shuffle(data, 3)
    print("After inverse feistel shuffle:", bytes(data))
    
    # Try all possible options for inverse prime block shuffle
    data = inverse_prime_block_shuffle(data)
    print("After inverse prime block shuffle:", bytes(data))
    
    # Finally, reverse the XOR operation
    data = xor_layer(data, key)  # XOR is its own inverse
    print("Decrypted flag:", bytes(data))
    
    # Convert to string, stopping at null bytes
    flag_str = ""
    for b in data:
        if b == 0:
            break
        flag_str += chr(b)
    
    return flag_str

# Try to solve the challenge using the brute force approach
def brute_force_solve():
    # We know the decryption process is:
    # 1. Inverse Matrix Shuffle
    # 2. Inverse Feistel Shuffle (3 rounds)
    # 3. Inverse Prime Block Shuffle (try all 3 possibilities)
    # 4. XOR with key
    
    data = bytearray(encrypted_flag)
    data = inverse_matrix_shuffle(data)
    data = inverse_feistel_shuffle(data, 3)
    
    # Try all three possible block sizes
    for bs_index, bs in enumerate([7, 11, 13]):
        temp = bytearray(FLAG_LEN)
        bs_inverse = pow(bs, -1, FLAG_LEN)
        
        # Apply the inverse shuffle
        for i in range(FLAG_LEN):
            new_pos = (i * bs) % FLAG_LEN
            temp[i] = data[new_pos]
        
        # XOR with key
        candidate = xor_layer(temp, key)
        
        # Check if the result looks like a valid flag
        candidate_str = "".join(chr(b) for b in candidate if 32 <= b <= 126)
        print(f"Block size {bs} candidate: {candidate_str}")
        
        # Alternative approach - reverse mapping
        temp2 = bytearray(FLAG_LEN)
        for i in range(FLAG_LEN):
            orig_pos = (i * bs_inverse) % FLAG_LEN
            temp2[orig_pos] = data[i]
        
        # XOR with key
        candidate2 = xor_layer(temp2, key)
        candidate_str2 = "".join(chr(b) for b in candidate2 if 32 <= b <= 126)
        print(f"Block size {bs} candidate (method 2): {candidate_str2}")

if __name__ == "__main__":
    print("Attempting to solve the challenge...")
    # Try the analytical solution first
    flag = solve_challenge()
    print("Possible flag:", flag)
    
    # If the analytical solution doesn't give a clear result, try brute force
    print("\nTrying brute force approach for all possible block sizes:")
    brute_force_solve()

