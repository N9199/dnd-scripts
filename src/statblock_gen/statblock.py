from ..stats.stats import stats


class statblock(stats):

    def __init__(self, cr: float):
        super().__init__(cr)
        self.cr = cr
        self.info = ""  # Define what's this
        self.__gen()

    def __gen(self):
        # raise NotImplementedError
        # Check Martial or Magic, or both
        max_mar = max(self.str, self.dex, self.con)
        max_mag = max(self.int, self.wis, self.cha)
        if max_mar > max_mag:
            self.info += "Martial\n"
            # More Stuff
        elif max_mar < max_mag:
            self.info += "Magic\n"
            # More Stuff
        else:
            self.info += "Mixed\n"
        print(self.info)

    def __str__(self):
        # Finish out
        out = (
            "Statblock:\n"
            ""
        )
        stat = (
            "Stats:\n"
            "Strength:     {:8}\n"
            "Dexterity:    {:8}\n"
            "Constitution: {:8}\n"
            "Intelligence: {:8}\n"
            "Wisdom:       {:8}\n"
            "Charisma:     {:8}"
        ).format(
            *list(map(
                stats.stat,
                [e for e in vars(self).values()][:6]
            ))
        )
        return out+self.info+stat

    def __repr__(self):
        # Finish this
        out = "Statblock:\n"
        return out+self.info+super().__repr__()


if __name__ == "__main__":
    print(statblock(5))
    print(statblock(10))
    print(statblock(20))
