# Solution for The Unseen Curse in python
#!/usr/bin/env python3
def main():
    with open('../files/the-unseen-curse.txt', 'r') as f:
        A, B = map(int, f.readline().split())
        X, Y = map(int, f.readline().split())

    # Now you can use these variables in your solution
    print(f"Alice sees {A} marked trees")
    print(f"Bob sees {B} marked trees")
    print(f"Possible totals: {X} or {Y}")


if __name__ == "__main__":
    main()
