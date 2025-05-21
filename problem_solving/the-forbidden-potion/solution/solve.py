# solve script for four numbers add to fixed sum & product
#!/usr/bin/env python3

from math import sqrt

sm = 981
product = 981 * 1_000_000

i = 25
while i <= (sm // 2):
    j = 4
    while j <= (sm - i) // 2:
        qt = product / (i * j)
        if qt.is_integer():
            rm = sm - (i + j)
            ds = (rm ** 2) - 4 * qt
            if ds >= 0:
                k = (rm + sqrt(ds)) / 2
                l = (rm - sqrt(ds)) / 2
                if k * l == qt:
                    ireal = i / 100
                    jreal = j / 100
                    kreal = k / 100
                    lreal = l / 100
                    # print(f'The real <i> = {ireal}')
                    # print(f'The real <j> = {jreal}')
                    # print(f'The real <k> = {kreal}')
                    # print(f'The real <l> = {lreal}')
                    # print(f'Their sum = {ireal + jreal + kreal + lreal}')
                    # print(f'Their product = {ireal * jreal * kreal * lreal}')
                    results = [str(ireal), str(jreal), str(kreal), str(lreal)]
                    print(f'- "1ng3neer2k25{{{'_'.join(results)}}}"')
        j += 4
    i += 25
