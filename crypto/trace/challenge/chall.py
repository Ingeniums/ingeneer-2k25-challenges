import os
from Crypto.Util.number import bytes_to_long
from sage.all import *

m = bytes_to_long(flag)
p = 82880337306360052550952380657384418102169134986290141696988204552000561657747
a = 26413685284385555604181540288021678971301314378522544469879270355650843743231
b = 10017655579196313780863100027113686719855502076415017585743221280232958057095

E = EllipticCurve(GF(p), [a, b])
trace_1 = p + 1 - E.cardinality()
trace_cache = {0: 2, 1: trace_1}

def complicated_trace(n):
    def inner(k):
        if k in trace_cache:
            return trace_cache[k]
        val = inner(k - 1) * inner(1) - p * inner(k - 2)
        trace_cache[k] = val
        return val

    t = inner(n)
    return p**n + 1 - t

x = bytes_to_long(os.urandom(16))
n = complicated_trace(x)
e = 0x10001
c = pow(m, e, n)

with open('output.txt', 'w') as f:
    f.write(str(c))

