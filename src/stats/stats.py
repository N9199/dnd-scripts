from random import randint, shuffle
from math import log2, sqrt
from ..stats.challenge import challenge
import pandas as pd
import os


class stats:

    def __init__(self, diff: int):
        self.str = None
        self.dex = None
        self.con = None
        self.int = None
        self.wis = None
        self.cha = None
        self.cr = challenge(diff)

        self.__gen(diff)

    @staticmethod
    def stat(num: int) -> str:
        out = "{0:2} ({1})"
        num = int(num)
        if num < 10:
            mod = (num-10)//2
        elif num > 11:
            mod = "+{}".format((num-10)//2)
        else:
            mod = 0
        return out.format(num, mod)

    @staticmethod
    def __check(l: int, diff: int, other: list):
        temp = sum([(e-10)//2 for e in other])
        if temp >= (log2(diff)+2)*4 and len(other) == 6:
            return True
        if l < 2:
            return False
        if l*l/diff < 22:
            return False
        return True

    def __gen(self, diff: int):
        temp_stats = None
        if diff < 1:
            # Gen Stats for low cr creatures
            if diff == 0:
                diff = 1/32
            temp_stats = []
            for i in range(6):
                l = 0
                while not self.__check(l, diff, temp_stats):
                    l += int(log2(diff)+randint(1, log2(diff)+14))
                temp_stats.append(l)

        elif diff < 2:
            # Gen Stats for normal people
            # print(os.path.abspath(os.path.curdir))
            # Change path in case of refactor
            path = os.path.abspath(os.path.curdir)+"/src/csv_files/"
            l = pd.read_csv(
                path+"pointbuy.csv",
                keep_default_na=False
            )
            temp_stats = l.iloc[randint(0, len(l)-1)]
            temp_stats = temp_stats.tolist()
            shuffle(temp_stats)
        else:
            # Gen Stats for Heroes or high cr creatures
            temp_stats = []
            for i in range(6):
                l = 0
                c = 0
                while not self.__check(l, diff, temp_stats) and 2*c < log2(diff):
                    l += int(sqrt(diff)) + \
                        randint(1, int(sqrt(diff))+8)
                    c += 1
                temp_stats.append(l)

        self.str = temp_stats.pop()
        self.dex = temp_stats.pop()
        self.con = temp_stats.pop()
        self.int = temp_stats.pop()
        self.wis = temp_stats.pop()
        self.cha = temp_stats.pop()

    def __repr__(self):
        out = (
            "Stat:\n"
            "str: {str:2}\n"
            "dex: {dex:2}\n"
            "con: {con:2}\n"
            "int: {int:2}\n"
            "wis: {wis:2}\n"
            "cha: {cha:2}"
        )
        return out.format(**vars(self))


if __name__ == "__main__":
    print(stats(5))
    print(stats(10))
    print(stats(20))
