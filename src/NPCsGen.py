from random import randint, choice
from os import listdir, rename
from subprocess import call
from NPCsStats import stats
import pandas as pd


class NPC:

    def __init__(
        self, diff,
        limits_race=[], limits_class=[], limits_align=[],
        NPC=True, Test=False
    ):
        self.NPC = NPC
        self.diff = diff
        self.stats = stats(diff)
        self.char = pd.Series()
        self.test = Test
        self.gen(limits_race, limits_class, limits_align)

    def gen(self, limits_race, limits_class, align):
        # Read corresponding .csv files
        races = pd.read_csv("races.csv", keep_default_na=False)
        if self.diff >= 0:
            classes = pd.read_csv(
                "classes.csv", keep_default_na=False)
        else:
            classes = pd.read_csv(
                "classes*.csv", keep_default_na=False)

        # Base Setup
        for i in range(len(races['prof'])):
            races['prof'][i] = races['prof'][i].split(',')

        for i in range(len(races['special'])):
            races['special'][i] = races['special'][i].split(',')

        for i in range(len(races['lang'])):
            races['lang'][i] = races['lang'][i].split(',')

        for i in range(len(races['female_names'])):
            races['female_names'][i] = races['female_names'][i].split(
                ',')

        for i in range(len(races['male_names'])):
            races['male_names'][i] = races['male_names'][i].split(',')

        for i in range(len(races['last_names'])):
            races['last_names'][i] = races['last_names'][i].split(',')

        for i in range(len(classes['prof'])):
            classes['prof'][i] = classes['prof'][i].split(',')

        for i in range(len(classes['saving_throws'])):
            classes['saving_throws'][i] = classes['saving_throws'][i].split(
                ',')

        for i in range(len(classes['special'])):
            classes['special'][i] = classes['special'][i].split(',')

        for i in range(len(classes['items'])):
            classes['items'][i] = classes['items'][i].split(',')

        for i in range(len(classes['primary_ability'])):
            temp = classes['primary_ability'][i].split(',')
            classes['primary_ability'][i] = temp

        align = set(align)

        # Filters, and class & race selection
        filter_race = True
        if len(limits_race) != 0:
            for item in limits_race:
                flag = '~' in item
                if flag:
                    item = item[1:]
                item = item.split('=')
                flag2 = ',' in item[1]
                if flag2:
                    temp = False
                    asdf = item[1].split(',')
                    for a in asdf:
                        temp = temp | (races[item[0]] == a)
                    if flag:
                        filter_race = filter_race & ~temp
                    else:
                        filter_race = filter_race & temp
                else:
                    if flag:
                        filter_race = filter_race & (
                            races[item[0]] != item[1])
                    else:
                        filter_race = filter_race & (
                            races[item[0]] == item[1])
            r = races[filter_race].iloc[randint(
                0, len(races[filter_race])-1)]
        else:
            r = races.iloc[randint(0, len(races)-1)]

        filter_class = True
        if len(limits_class) != 0:
            for item in limits_class:
                flag = '~' in item
                if flag:
                    item = item[1:]
                item = item.split('=')
                flag2 = ',' in item[1]
                if flag2:
                    temp = False
                    asdf = item[1].split(',')
                    for a in asdf:
                        temp = temp | (classes[item[0]] == a)
                    if flag:
                        filter_class = filter_class & ~temp
                    else:
                        filter_class = filter_class & temp
                else:
                    if flag:
                        filter_class = filter_class & (
                            classes[item[0]] != item[1])
                    else:
                        filter_class = filter_class & (
                            classes[item[0]] == item[1])
            c = classes[filter_class].iloc[randint(
                0, len(classes[filter_class])-1)]
        else:
            c = classes.iloc[randint(0, len(classes)-1)]

        # Merge selected class and race, to character info
        self.char = c+r
        for index in self.char.index:
            a = pd.isna(self.char[index])
            if type(a) != bool:
                a = a.any()
            if a:
                if r.get(index) is not None:
                    self.char[index] = r[index]
                elif c.get(index) is not None:
                    self.char[index] = c[index]

        # Setup for formatting
        self.char['prof'] = set(self.char['prof'])
        self.char['prof'].discard('')

        self.char['special'] = set(self.char['special'])
        self.char['special'].discard('')

        self.char['items'] = list(self.char['items'])
        print("ASDF")
        for i, item in enumerate(self.char['items']):
            if "choose" in item:
                l = [ls[1:-1].replace(".", ",")
                     for ls in item[7:].split("/")]
                self.char['items'][i] = [
                    "choose", enumerate(l)]
                alph = [chr(i) for i in range(ord('a'), ord('z')+1)]
                self.char['items'][i][1] = list(map(
                    lambda it: ("({})".format(alph[it[0]]), it[1]),
                    self.char['items'][i][1]
                ))

        print(self.char['items'])

        print("ASDF")

        self.char['str'] += self.stats.str
        self.char['dex'] += self.stats.dex
        self.char['con'] += self.stats.con
        self.char['int'] += self.stats.int
        self.char['wis'] += self.stats.wis
        self.char['cha'] += self.stats.cha

        # Gender, pronouns and names for the formatting
        self.char['gender'] = choice(['male', 'female']).title()
        if self.char['gender'].lower() == 'male':
            self.char['name'] = choice(
                self.char['male_names']).title() if self.NPC else "Fill"
            self.char['pronoun1'] = 'he'
            self.char['pronoun2'] = 'his'
            self.char['pronoun3'] = 'him'
        else:
            self.char['name'] = choice(
                self.char['female_names']).title() if self.NPC else "Fill"
            self.char['pronoun1'] = 'she'
            self.char['pronoun2'] = 'her'
            self.char['pronoun3'] = 'her'
        self.char['lastname'] = choice(
            self.char['last_names']
        ).title() if self.NPC else ""

        # Alignment choosing (may do a rework to filter alignments)
        self.char['alignment'] = choice(list(
            {'lawful good', 'neutral good', 'chaotic good',
             'lawful neutral', 'true neutral', 'chaotic neutral',
             'lawful evil', 'neutral evil', 'chaotic evil'}-align
        ))

        self.char['race'] = self.char['race'].title()

        # Almost arbitrary level chooser (mostly for the amount of hit dice)
        self.char['lvl'] = randint(
            1, self.diff*2+1) if self.diff >= 0 else 1

        # Modifier calculation
        if self.diff >= 0 or (self.char['con']-10)//2 > 1:
            self.char['conmod'] = (self.char['con']-10)//2
        else:
            self.char['conmod'] = 1
        self.char['wismod'] = ((self.char['wis']-10)//2)
        self.char['chamod'] = ((self.char['cha']-10)//2)
        self.char['intmod'] = ((self.char['int']-10)//2)
        self.char['perception'] = (self.char['wis']-10)//2
        self.char['bon'] = (self.char['lvl']-1)//4+2

        # Bonus HP from CON
        self.char['hp'] = self.char['conmod']*self.char['lvl']

        if 'tough' in self.char['special']:
            # Logic for tough
            self.char['hp'] += self.char['lvl']

        # Skills, need to do a rework,
        # so that they're formatted with the correct modifiers
        skills = {
            'athletics',
            'acrobatics', 'sleight_of_hand', 'stealth',
            'arcana', 'history', 'investigation', 'nature', 'religion',
            'animal_handling', 'insight', 'medicine', 'perception', 'survival',
            'deception', 'intimidation', 'performance', 'persuasion'
        }
        self.char['skills'] = self.char['prof'] & skills
        self.char['skills'] = self.frmt(self.char['skills'])[:-2]

        senses = {
            'darkvision_normal', 'darkvision_superior',
            'blindsight', 'truesight'
        }
        self.char['senses'] = self.char['prof'] & senses
        for item in self.char['senses']:
            if 'darkvision' in item:
                if 'normal' in item:
                    item = 'Darkvision 60 ft'
                elif 'superior' in item:
                    item = 'Darkvision 120 ft'

        self.char['senses'] = ("passive Perception {}, "+self.frmt(
            self.char['senses'])).format(10+self.char['perception'])[:-2]

        self.char['lang'] = self.frmt(self.char['lang'])[:-2]

        self.char['saving_throws'] = self.frmt(
            self.char['saving_throws'])[:-2]

        # Stuff that needs special logic to deal with
        special = {
            'tough'
        }
        # All the things that need a description in the character summary
        self.char['add'] = ((
            self.char['special'] - skills) - senses) - special
        self.func()
        if not self.test:
            self.add()
        # Check the output
        print(self.out())

    # Format Function
    def frmt(self, s):
        if len(s) == 0:
            return ""
        else:
            out = ""
            for item in s:
                out += "{}, ".format(item).title()
            return out

    # Add the output to NPCs.tex or to StatBlocks
    def add(self):
        file = 'NPCs.tex' if self.NPC else 'StatsBlocks.tex'
        with open(file, encoding='utf8', mode='r') as r:
            with open(file+'.tmp', encoding='utf8', mode='w') as w:
                for line in r:
                    if line == '\\end{document}':
                        w.write("\n")
                        w.write(self.out())
                        w.write(line)
                    else:
                        w.write(line)
        bad_suffix = ".tmp"
        fnames = listdir('.')
        for f in fnames:
            if f.endswith(bad_suffix):
                rename(f, f.replace(bad_suffix, '', 1))
        call(
            ("pdflatex -synctex=1 -interaction=nonstopmode -file-line-error "
             + file).split(' ')
        )
        call(
            ("pdflatex -synctex=1 -interaction=nonstopmode -file-line-error "
             + file).split(' ')
        )
        file = file[:-4]
        call(
            [
                'rm', '-rf',
                file+'.aux', file+'.log', file+'.out'
            ]
        )

    def out(self):
        begin = '\\begin{{monsterboxnobg}}{{{name} {lastname}}}\n'
        end = '\\end{{monsterboxnobg}}\n'
        begin2 = '\\begin{{monsterbox}}{{{name}}}\n'
        end2 = '\\end{{monsterbox}}\n'
        line_break = "\\hline\n"

        first_par = (
            "\\begin{{hangingpar}}\n"
            "        \\textit{{{gender} {race}, {class}, {alignment}}}\n"
            "    \\end{{hangingpar}}\n"
        )

        second_par = (
            "\\basics[\n"
            "       armorclass = {{}},\n"
            "       hitpoints  = {{\\dice{{{lvl}{hit_die}{hp:+}}}}},\n"
            "       speed      = {{{speed}}}\n"
            "    ]\n"
        )

        third_par = (
            "\\stats[\n"
            "       STR = \\stat{{{str}}},\n"
            "       DEX = \\stat{{{dex}}},\n"
            "       CON = \\stat{{{con}}},\n"
            "       INT = \\stat{{{int}}},\n"
            "       WIS = \\stat{{{wis}}},\n"
            "       CHA = \\stat{{{cha}}}\n"
            "    ]\n"
        )

        fourth_par = (
            "\\details[\n"
            "       savingthrows = {{{saving_throws}}},\n"
            "       languages    = {{{lang}}},\n"
            "       skills       = {{{skills}}},\n"
            "       senses       = {{{senses}}}\n"
            "    ]\n"
        )
        special = "{add}\n"
        prof = "{prof}\n"
        items = "{items}\n"

        actions_start = "\\monstersection{{Actions}}\n"

        summary_start = "\\monstersection{{Summary}}\n"

        out = ""
        out += begin if self.NPC else begin2
        out += "    " + first_par
        out += "    " + line_break
        out += "    " + second_par
        out += "    " + line_break
        out += "    " + third_par
        out += "    " + line_break
        out += "    " + fourth_par
        out += "    " + line_break
        out += "\n    %Proficiencies:" + prof
        out += "\n    %Items:" + items
        for item in self.char['add']:
            out += "    \\begin{{monsteraction}}"
            out += "[{skill}]\n".format(**item)
            out += "       {description}\n".format(**item)
            out += "    \\end{{monsteraction}}\n\n"

        out += "    " + actions_start
        out += "    " + (summary_start if self.NPC else "")
        out += end if self.NPC else end2
        return out.format(**self.char.to_dict({}))

    def func(self):
        m = {
            "resilient": {
                'skill': 'Resilience',
                'description': (
                    "{name} has advantage on saving throws against poison,"
                    " and {pronoun1} has resistance against poison damage"
                )
            },
            "stonecunning": {
                'skill': 'Stonecunning',
                'description': (
                    "Whenever {name} makes an Intelligence (History) check"
                    " related to the origin of stonework, {pronoun1} is"
                    " considered proficient in the History skill and adds"
                    " double {pronoun2} proficiency bonus to the check,"
                    " instead of {pronoun2} normal proficiency bonus."
                )
            },
            "trance": {
                'skill': 'Trance',
                'description': (
                    "Elves don’t need to sleep. Instead, they meditate deeply,"
                    " remaining semiconscious, for 4 hours a day. (The Common"
                    " word for such meditation is “trance.”) While meditating,"
                    " {pronoun1} can dream after a fashion; such dreams are"
                    " actually mental exercises that have become reflexive"
                    " through years of practice. After resting in this way,"
                    " {pronoun1} gains the same benefit that a human does from"
                    " 8 hours of sleep."
                )
            },
            "drow_magic": {
                'skill': "Drow Magic",
                'description': (
                    "{name} knows the dancing lights cantrip. When {pronoun1}"
                    " reaches 3rd level, {pronoun1} can cast the faerie fire"
                    " spell once per day. When {pronoun1} reaches 5th level,"
                    " {pronoun1} can also cast the darkness spell once per day"
                    ". Charisma is {pronoun2} spellcasting ability for these"
                    " spells."
                )
            },
            "fey": {
                'skill': "Fey Ancestry",
                'description': (
                    "{name} has advantage on saving throws against being"
                    " charmed, and magic can’t put {pronoun3} to sleep."
                )
            },
            "sunlight_sensitivity": {
                'skill': "Sunlight Sensitivity",
                'description': (
                    "{name} has disadvantage on attack rolls and on Wisdom"
                    " (Perception) checks that rely on sight when {pronoun1},"
                    " the target of {pronoun2} attack, or whatever {pronoun1}"
                    " is trying to perceive is in direct sunlight."
                )
            },
            "mask_wild": {
                'skill': "Mask of the Wild",
                'description': (
                    "{name} can attempt to hide even when {pronoun1} is only"
                    " lightly obscured by foliage, heavy rain, falling snow,"
                    " mist, and other natural phenomena"
                )
            },
            "cantrip": {
                'skill': "Cantrip",
                'description': (
                    "{name} knows one cantrip of {pronoun2} choice from the"
                    " wizard spell list. Intelligence is {pronoun2}"
                    " spellcasting ability for it."
                )
            },
            "brave": {
                'skill': "Brave",
                'description': (
                    "{name} has advantage on saving"
                    " throws against being frightened."
                )
            },
            "lucky": {
                'skill': "Lucky",
                'description': (
                    "When {pronoun1} rolls a 1 on an attack roll, ability"
                    " check, or saving throw, {pronoun1} can reroll the die"
                    " and must use the new roll."
                )
            },
            "nimble": {
                'skill': "Nimbleness",
                'description': (
                    "{name} can move through the space of any creature that"
                    " is of a size larger than {pronoun3}."
                )
            },
            "stealthy": {
                'skill': "Naturally Stealthy",
                'description': (
                    "{name} can attempt to hide even when {pronoun1} is"
                    " obscured only by a creature that is at least one"
                    " size larger than {pronoun3}."
                )
            },
            "draconic_ancestry": dragon(),
            "cunning": {
                'skill': "Cunning",
                'description': (
                    "{name} has advantage on all Intelligence, Wisdom,"
                    " and Charisma saving throws against magic."
                )
            },
            "illusionist": {
                'skill': "Natural Illusionist",
                'description': (
                    "{name} knows the minor illusion cantrip. Intelligence is"
                    " {pronoun2} spellcasting ability for it."
                )
            },
            "speak_with_small_animals": {
                'skill': "Speak with Small Beasts",
                'description': (
                    "Through sounds and gestures, {name} can communicate"
                    " simple ideas with Small or smaller beasts."
                )
            },
            "artificer": {
                'skill': "Artificer’s Lore",
                'description': (
                    "Whenever {name} makes an Intelligence (History) check"
                    " related to magic items, alchemical objects, or"
                    " technological devices, {pronoun1} can add twice"
                    " {pronoun2} proficiency bonus, instead of any proficiency"
                    " bonus {pronoun1} normally applies."
                )
            },
            "tinker": {
                'skill': "Tinker",
                'description': (
                    "{name} has proficiency with artisan’s tools"
                    " (tinker’s tools). Using those tools, {pronoun1} can"
                    " spend 1 hour and 10 gp worth of materials to construct a"
                    " Tiny clockwork device (AC 5, 1 hp). The device ceases to"
                    " function after 24 hours (unless you spend 1 hour"
                    " repairing it to keep the device functioning), or when"
                    " {pronoun1} use {pronoun2} action to dismantle it; at"
                    " that time, {pronoun1} can reclaim the materials used to"
                    " create it. {pronoun1} can have up to three such devices"
                    " active at a time. When you create a device, choose one"
                    " of the following options:\n"
                    "       \\textit{{Clockwork Toy.}} This toy is a clockwork"
                    " animal, monster, or person, such as a frog, mouse, bird,"
                    " dragon, or soldier. When placed on the ground, the toy"
                    "moves 5 feet across the ground on each of your turns in a"
                    " random direction. It makes noises as appropriate to the"
                    " creature it represents.\n"
                    "       \\textit{{Fire Starter.}} The device produces a"
                    " miniature flame, which you can use to light a candle,"
                    " torch, or campfire. Using the device requires your"
                    " action.\n"
                    "       \\textit{{Music Box.}} When opened, this music box"
                    " plays a single song at a moderate volume. The box stops"
                    " playing when it reaches the song’s end or when it is"
                    " closed.\n"
                )
            },
            "skills": {
                'skill': "Extra skills ({n})",
                'description': (
                    "{name} can choose two extra skills."
                )
            },
            "ability": {
                'skill': "Extra Ability Scores ({n})",
                'description': (
                    "{name} has two extra ability scores to put anywhere."
                )
            },
            "relentless": {
                'skill': "Relentless Endurance",
                'description': (
                    "When {name} is reduced to 0 hit points but not killed"
                    " outright, {pronoun1} can drop to 1 hit point instead."
                    " {name} can’t use this feature again until {pronoun1}"
                    " finishes a long rest."
                )
            },
            "savage": {
                'skill': "Savage Attacks",
                'description': (
                    "When {name} scores a critical hit with a melee weapon"
                    " attack, {pronoun1} can roll one of the weapon’s damage"
                    " dice one additional time and add it to the extra damage"
                    " of the critical hit."
                )
            },
            "infernal_legacy": {
                'skill': "Infernal Legacy",
                'description': (
                    "{name} knows the thaumaturgy cantrip. Once {pronoun1}"
                    " reaches 3rd level, {pronoun1} can cast the hellish"
                    " rebuke spell once per day as a 2nd-level spell. Once"
                    " {pronoun1} reaches 5th level, {pronoun1} can also cast"
                    " the darkness spell once per day. Charisma is {pronoun2}"
                    " spellcasting ability for these spells."
                )
            },
            "fire_resistance": {
                'skill': "Fire Resistance",
                'description': (
                    "{name} has resistance to fire damage."
                )
            },
            "lay_on_hands": {
                'skill': "Lay on Hands",
                'description': (
                    "{name} has a pool of healing power that replenishes when"
                    " {pronoun1} takes a long rest. With that pool, {pronoun1}"
                    " can restore a total number of hit points equal to"
                    " {pronoun2} paladin level x 5. As an action, {pronoun1}"
                    " can touch a creature and draw power from the pool to"
                    " restore a number of hit points to that creature, up to"
                    " the maximum amount remaining in {pronoun2} pool."
                    " Alternatively, {pronoun1} can expend 5 hit points from "
                    "{pronoun2} pool of healing to cure the target of one "
                    "disease or neutralize one poison affecting it. {name}"
                    " can cure multiple diseases and neutralize multiple "
                    "poisons with a single use of Lay on Hands, expending "
                    "hit points separately for each one. This feature has "
                    "no effect on undead and constructs. "
                )
            },
            "divine_sense": {
                'skill': "Divine Sense",
                'description': (
                    "As an action, until the end of {pronoun2} next turn, "
                    "{pronoun1} knows the location of any celestial, fiend, or"
                    " undead within 60 feet of {pronoun3} that is not behind "
                    "total cover. {name} knows the type of any being whose "
                    "presence {pronoun1} senses, but not its identity. Within "
                    "the same radius, {pronoun1} also detects the presence of "
                    "any place or object that has been consecrated or "
                    "desecrated. {pronoun1} can use this feature a number of "
                    "times equal to 1 + {pronoun2} Charisma modifier. When "
                    "{pronoun1} finishes a long rest, {pronoun1} regains all "
                    "expended uses. "
                )
            }
        }
        self.char['add'] = list(self.char['add'])
        for i in range(len(self.char['add'])):
            if '*' in self.char['add'][i]:
                a, b = self.char['add'][i].split('*')
                self.char['add'][i] = m.get(
                    a, {'skill': self.char['add']
                        [i], 'description': 'Fill'}
                )
                temp = self.char['add'][i]['skill'].format(n=b)
                self.char['add'][i].loc['skill'] = temp
            elif 'spellcaster' in self.char['add'][i]:
                a, b = self.char['add'][i].split('_')
                self.char['add'][i] = self.spellcaster(b)
            else:
                self.char['add'][i] = m.get(
                    self.char['add'][i],
                    {'skill': self.char['add']
                        [i], 'description': 'Fill'}
                )

    # Logic for spellcasting
    def spellcaster(self, ability):
        m = {
            'wis': "Wisdom",
            'int': "Intelligence",
            'cha': "Charisma"
        }
        out = (
            "{name} is a {lvl}-level spellcaster. {pronoun2} spellcasting"
            " ability is " + m[ability] + " (spell save DC"
            " " + str(self.char[ability+'mod']+8+self.char['bon']) +
            " " + "{:+}".format(self.char[ability+'mod']+self.char['bon']) +
            " to hits with spell attacks). {name} has the following "
            "{class} spells:\n"
            "       Fill"
        )
        return {
            'skill': "Spellcaster",
            'description': out
        }


# Logic for draconic_ancestry
def dragon():
    out = {}
    d_type = choice([
        {
            'dragon': "Black",
            'damage': "Acid",
            'breath': "5 by 30 ft. line (Dex. save)"
        },
        {
            'dragon': "Blue",
            'damage': "Lightning",
            'breath': "5 by 30 ft. line (Dex. save)"
        },
        {
            'dragon': "Brass",
            'damage': "Fire",
            'breath': "5 by 30 ft. line (Dex. save)"
        },
        {
            'dragon': "Bronze",
            'damage': "Lightning",
            'breath': "5 by 30 ft. line (Dex. save)"
        },
        {
            'dragon': "Copper",
            'damage': "Acid",
            'breath': "5 by 30 ft. line (Dex. save)"
        },
        {
            'dragon': "Gold",
            'damage': "Fire",
            'breath': "15 ft. cone (Dex. save)"
        },
        {
            'dragon': "Green",
            'damage': "Poison",
            'breath': "15 ft. cone (Con. save)"
        },
        {
            'dragon': "Red",
            'damage': "Fire",
            'breath': "15 ft. cone (Dex. save)"
        },
        {
            'dragon': "Silver",
            'damage': "Cold",
            'breath': "15 ft. cone (Con. save)"
        },
        {
            'dragon': "Silver",
            'damage': "Cold",
            'breath': "15 ft. cone (Con. save)"
        }
    ])
    out['skill'] = "Draconic Ancestry ({dragon})".format(**d_type)
    temp = (
        "{name} has draconic ancestry. It determines two main things,"
        " {pronoun2} breath weapon and a type of damage resistance.\n"
        "   \\end{{monsteraction}}\n\n"
    )
    temp += "   \\begin{{monsteraction}}[Breath Weapon ("
    temp += "{damage}".format(**d_type)+")]\n"
    temp += "       {name} can use your action to exhale destructive energy. "
    temp += "Of the following shape, size and save: {breath}.".format(
        **d_type)
    temp += " The DC for this saving throw equals 8 + {pronoun2} Constitution"
    temp += " modifier + {pronoun2} proficiency bonus. A creature takes 2d6"
    temp += " damage on a failed save, and half as much damage on a successful"
    temp += " one. The damage increases to 3d6 at 6th level, 4d6 at 11th level"
    temp += ", and 5d6 at 16th level.\n"
    temp += "       After {pronoun1} uses {pronoun3} "
    temp += "breath weapon {pronoun1} can’t use it again until {pronoun1}"
    temp += " completes a short or long rest.\n"
    temp += "   \\end{{monsteraction}}\n\n"
    temp += "   \\begin{{monsteraction}}[Damage Resistance]\n"
    temp += "       {name} has resistance to "
    temp += "{damage}.".format(**d_type)
    out['description'] = temp
    return out


if __name__ == "__main__":
    # Re-do at some point
    l1 = [
        # '~race=human',
        'race=human'
    ]
    l2 = [
        'class=paladin'
    ]
    l3 = [
        ''
    ]
    a = NPC(3, limits_race=l1, limits_class=l2,
            limits_align=l3, Test=True)
