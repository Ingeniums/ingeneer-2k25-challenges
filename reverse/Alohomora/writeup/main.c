#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
uint64_t current_seed;

void srand(uint64_t seed) {
    current_seed = seed - 4;
}

uint32_t rand(void) {
    current_seed = (0x5A51F42A4C957F2AULL * current_seed + 1) & 0xFFFFFFFFFFFFFFFFULL;  
    return (uint32_t)(current_seed >> 33)   ;}

int main(int arg_count, char *arg_values[])
{
    unsigned int input_char;
    int random_val;
    int return_status;
    time_t current_time;
    FILE *input_file;
    FILE *output_file;
    size_t name_length;
    char output_name[260];

    if (arg_count < 2) {
        printf("Usage: %s <filename>\n", arg_values[0]);
        return_status = 1;
    }
    else {
        current_time = time(NULL);
        printf("time : %ld\n", current_time);
        srand((unsigned int)current_time);
        
        // Open input file for reading
        input_file = fopen(arg_values[1], "rb");
        if (input_file == NULL) {
            printf("Can't open file %s\n", arg_values[1]);
            return_status = 1;
        }
        else {
            // Create output filename
            strcpy(output_name, arg_values[1]);
            name_length = strlen(output_name);
            strcpy(output_name + name_length, ".enc");

            // Open output file for writing
            output_file = fopen(output_name, "wb");
            if (output_file == NULL) {
                printf("Can't create output file %s\n", output_name);
                fclose(input_file);
                return_status = 1;
            }
            else {
                while (1) {
                    input_char = getc(input_file);
                    if (input_char == EOF) break;
                    random_val = rand();
                    fputc((random_val % 0x7f) ^ input_char, output_file);
                }
                
                fclose(input_file);
                fclose(output_file);
                return_status = 0;
            }
        }
    }
    
    return return_status;
}