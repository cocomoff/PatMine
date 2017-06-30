# -*- coding: utf-8 -*-

import bitarray as BA
import BitVector as BV


def test_array():
    BA.test()

def sample_array():
    a = BA.bitarray()
    a.append(True)
    a.extend([False, True, True])
    print(a)

    b = BA.bitarray(2**10)
    lst = [True, False, False, True, False, True, True]
    print(b)
    print(BA.bitarray("100101"))
    print(BA.bitarray(lst))

    i1 = BA.bitarray("1001001")
    i2 = BA.bitarray("0011010")

    print(i1 & i2)
    print(i1 | i2)
    print(i1 ^ i2)

    
if __name__ == '__main__':
    sample_array()
