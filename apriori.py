# -*- coding: utf-8 -*-

import BitVector as BV
from collections import defaultdict

class DB(object):
    def __init__(self, db=None):
        if db is not None:
            self.db = db
        else:
            # sample database
            self.db = [
                [1, 2, 5, 6, 7, 9],
                [2, 3, 4, 5],
                [1, 2, 7, 8, 9],
                [1, 7, 9],
                [2, 3, 7, 9]
            ]
        self.max_item = max([max(v) for v in self.db])

    def get_max_item(self):
        return self.max_item

    def __iter__(self):
        return self.db.__iter__()

    def __len__(self):
        return self.db.__len__()

    def __str__(self):
        return "[Size {}; Max {}]\n{}".format(len(self.db), self.max_item,
                                              self.db.__str__())


class Apriori(object):
    def __init__(self, db, theta=1):
        self.db = db
        self.M = self.db.get_max_item() + 1
        self.T = theta
        self.initialize()


    def initialize(self):
        self.bit_db = []
        for X in self.db:
            bitX = BV.BitVector(size = self.M)
            for item in X:
                bitX[item] = 1
            self.bit_db.append(bitX)

    def cover(self, item):
        ans = BV.BitVector(size = len(self.db))
        for ldx, bitX in enumerate(self.bit_db):
            if bitX[item]:
                ans[ldx] = 1
        return ans
            
    def support(self, item):
        lv = list(item)
        if len(lv) == 1:
            ans = self.cover(lv[0])
            return ans.count_bits()
        else:
            ans = BV.BitVector(size = self.M, intVal = 2 ** self.M - 1)
            for idx, bool_i in enumerate(lv):
                if bool_i:
                    ans &= self.cover(idx)
            return ans.count_bits()

    def bv2set(self, bv):
        ans = set({})
        for idx, elem in enumerate(bv):
            if elem:
                ans.add(idx)
        return frozenset(ans)
            
    def run(self):
        k = 1
        answer = set()
        Fk = defaultdict(list)
        for item in range(self.M):
            F1bit = BV.BitVector(size = self.M)
            F1bit[item] = 1
            count = self.support(set({item}))
            if count >= self.T:
                Fk[k].append(F1bit)
                answer.add(self.bv2set(F1bit))

        while len(Fk[k]) > 0:
            print("k: {}, |Fk|: {}".format(k, len(Fk[k])))
            for f1 in Fk[k]:
                for f2 in Fk[k]:
                    # print(f1, f2, f1 | f2)
                    if f1 != f2:
                        f12 = f1 | f2
                        ff12 = self.bv2set(f12)
                        if ff12 not in answer:
                            count = self.support(f12)
                            if count >= self.T:
                                # print(f1, f2, f12, count)
                                Fk[k+1].append(f12)
                                answer.add(self.bv2set(f12))
            k += 1
        return answer

if __name__ == '__main__':
    db = DB()
    apriori = Apriori(db, 3)
    results = apriori.run()

    for ans in results:
        print(set(ans))
