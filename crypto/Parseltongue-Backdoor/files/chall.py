from flag import FLAG
def snake_encrypt(message: str, cols: int) -> str:
    message = message.replace(" ", "").upper()
    
    rows = (len(message) + cols - 1) // cols  
    

    matrix = [['' for _ in range(cols)] for _ in range(rows)]
    index = 0
    for r in range(rows):
        for c in (range(cols) if r % 2 == 0 else reversed(range(cols))):
            if index < len(message):
                matrix[r][c] = message[index]
                index += 1
            else:
                matrix[r][c] = 'X'  

    encrypted = ''
    for c in range(cols):
        for r in range(rows):
            encrypted += matrix[r][c]
    return encrypted


print(snake_encrypt(FLAG,5))

# 1K2NQRS_CXN25OUAEEOXGR{CEPLUIX3EY_R_TGLXNEOUEDONS}
