#include <immintrin.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>

#define BLOCK_SIZE 32
#define FLAG_LEN 48

// Your encrypted flag bytes
const uint8_t encrypted_flag[FLAG_LEN] = {
    0x22, 0xE1, 0x50, 0xA4, 0x54, 0x8C, 0xDD, 0xA4, 
    0x22, 0xFB, 0x9E, 0xFE, 0x03, 0x0B, 0x9B, 0x77,
    0xCE, 0xB5, 0x84, 0x59, 0xCE, 0x45, 0xD4, 0x7F, 
    0xA9, 0xB4, 0x8F, 0x36, 0xB1, 0xAE, 0x6E, 0xE3,
    0x0F, 0x9F, 0x3F, 0x83, 0x00, 0xC8, 0xDD, 0xA8, 
    0xE3, 0x83, 0xBB, 0x95, 0xEF, 0xC1, 0x15, 0xAD
};

void xor_layer(uint8_t *data, const uint8_t *key) {
    for (size_t i = 0; i < FLAG_LEN; i += BLOCK_SIZE) {
        __m256i block = _mm256_loadu_si256((__m256i *)(data + i));
        __m256i key_vec = _mm256_loadu_si256((const __m256i *)(key + (i % BLOCK_SIZE)));
        __m256i result = _mm256_xor_si256(block, key_vec);
        _mm256_storeu_si256((__m256i *)(data + i), result);
    }
}

void prime_block_shuffle(uint8_t *data) {
    uint8_t temp[FLAG_LEN];
    const int block_sizes[] = {7, 11, 13};
    int bs = block_sizes[(data[0] + data[FLAG_LEN-1]) % 3];
    
    for (int i = 0; i < FLAG_LEN; i++) {
        int new_pos = (i * bs) % FLAG_LEN;
        temp[new_pos] = data[i];
    }
    memcpy(data, temp, FLAG_LEN);
}

void feistel_shuffle(uint8_t *data, int rounds) {
    for (int r = 0; r < rounds; r++) {
        for (int i = 0; i < FLAG_LEN/2; i++) {
            uint8_t left = data[i];
            uint8_t right = data[i + FLAG_LEN/2];
            data[i] = right;
            data[i + FLAG_LEN/2] = left ^ (right % 256);
        }
    }
}

void matrix_shuffle(uint8_t *data) {
    uint8_t temp[FLAG_LEN];
    const int rows = 6;
    const int cols = (FLAG_LEN + rows - 1) / rows;
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            int idx = i * cols + j;
            if (idx < FLAG_LEN) {
                temp[j * rows + i] = data[idx];
            }
        }
    }
    memcpy(data, temp, FLAG_LEN);
}

bool check_wish(const char *wish) {
    if (strlen(wish) > FLAG_LEN) return false;
    
    uint8_t padded_wish[FLAG_LEN] = {0};
    memcpy(padded_wish, wish, strlen(wish));
    
    // Apply the same transformations
    xor_layer(padded_wish, (uint8_t[]){
        0x13, 0x37, 0xBA, 0xAD, 0xC0, 0xDE, 0xFE, 0xED,
        0xBE, 0xEF, 0xFA, 0xCE, 0xCA, 0xFE, 0x42, 0x42,
        0x10, 0x20, 0x30, 0x40, 0x50, 0x60, 0x70, 0x80,
        0x90, 0xA0, 0xB0, 0xC0, 0xD0, 0xE0, 0xF0, 0x00
    });
    
    prime_block_shuffle(padded_wish);
    feistel_shuffle(padded_wish, 3);
    matrix_shuffle(padded_wish);
    
    return memcmp(padded_wish, encrypted_flag, FLAG_LEN) == 0;
}

int main() {
    char wish[FLAG_LEN + 1];
    printf("Make your wish (max %d chars): ", FLAG_LEN);
    fgets(wish, sizeof(wish), stdin);
    
    // Remove newline if present
    wish[strcspn(wish, "\n")] = '\0';
    
    if (check_wish(wish)) {
        printf("✨ Your wish is granted! (true)\n");
    } else {
        printf("❌ Not the right wish... (false)\n");
    }
    
    return 0;
}