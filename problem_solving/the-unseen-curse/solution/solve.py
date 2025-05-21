#!/usr/bin/env python3

def new_reasoning_solver(A=12, B=8, X=18, Y=20):
    if X == Y:
        return "1"

    nights = 1
    atleast = 0
    utmost = Y
    delta = Y - X

    while nights <= 30:
        # A tries to answer
        if utmost - delta + 1 <= A <= utmost:
            return str(nights)  # A can deduce
        else:
            utmost -= delta  # A fails, B learns something

        # B tries to answer
        if atleast <= B <= atleast + delta - 1:
            return str(nights)  # B can deduce
        else:
            atleast += delta  # B fails, A learns something

        nights += 1

    return "-1"  # Contradiction or unresolved after 30 nights


if __name__ == "__main__":
    with open("../files/the-unseen-curse.txt") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) % 2 == 0, "Each scenario must have two lines: (A,B) and (X,Y)."

    results = []

    for i in range(0, len(lines), 2):
        A, B = map(int, lines[i].split())
        X, Y = map(int, lines[i + 1].split())

        if X > Y:
            X, Y = Y, X

        result = new_reasoning_solver(A, B, X, Y)
        results.append(result)

    print("Flag:", f"1ng3neer2k25{{{''.join(results)}}}")

