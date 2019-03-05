from random import randint, shuffle
import pandas as pd


class stats:

    def __init__(self, diff):
        self.diff = diff
        self.str = None
        self.dex = None
        self.con = None
        self.int = None
        self.wis = None
        self.cha = None
        self.gen()

    def gen(self):
        if self.diff == 0:
            l = pd.read_csv("pointbuy.csv", keep_default_na=False)
            temp = l.iloc[randint(0, len(l)-1)]
            temp = temp.tolist()
            shuffle(temp)
        elif self.diff < -8:
            temp = 6*[2]
        else:
            temp = []
            while not self.acceptable(temp):
                temp = 6*[0]
                for i in range(6):
                    l = 4*[None]
                    for j in range(4):
                        l[j] = randint(1, max(6+self.diff//2, 1))
                    l.remove(min(l))
                    for n in l:
                        temp[i] += n

        self.str = temp.pop()
        self.dex = temp.pop()
        self.con = temp.pop()
        self.int = temp.pop()
        self.wis = temp.pop()
        self.cha = temp.pop()

    def acceptable(self, l):
        if len(l) == 0:
            return False
        if max(l) < self.diff*1.3 + 13:
            return False
        temp = 0
        for n in l:
            temp += (n-10)//2
        if self.diff < 0:
            if temp >= self.diff+2 and min(l) > self.diff//2+10:
                return False
        else:
            if temp <= self.diff*2 or min(l) < self.diff*0.5:
                return False
        return True

    def stat(self, a):
        out = "{0:2} ({1})"
        return out.format(a, (a-10)//2 if a < 10 else "+{}".format((a-10)//2))

    def __str__(self):
        out = (
            "Stats:\n"
            "Strength:      {}\n"
            "Dexterity:     {}\n"
            "Constitution:  {}\n"
            "Intelligence:  {}\n"
            "Wisdom:        {}\n"
            "Charisma:      {}"
        )
        temp = []
        out = out.format(*list(map(self.stat, [self.str,
                                               self.dex,
                                               self.con,
                                               self.int,
                                               self.wis,
                                               self.cha
                                               ]))
                         )
        return out


if __name__ == "__main__":
    diff = None
    while diff is None:
        try:
            diff = int(input("Diff\n"))
        except:
            continue
    print(stats(diff))
