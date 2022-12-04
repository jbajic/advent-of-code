import collections

polymer = None
rules = dict()
with open("input.txt") as inp:
    polymer = inp.readline()
    for line in inp.readlines():
        if line == "\n":
            continue
        split = line.strip().split(" -> ")
        rules[split[0]] = split[1]


def puzzle1(polymer, rules):
    for _ in range(10):
        new_poly = ""
        print(f"Polymer: {polymer}")
        for i in range(len(polymer) - 1):
            if f"{polymer[i]}{polymer[i+1]}" in rules:
                new_poly += polymer[i] + rules[f"{polymer[i]}{polymer[i+1]}"]
            else:
                new_poly += polymer[i]
        polymer = new_poly + polymer[len(polymer) - 1]

    d = collections.defaultdict(int)
    for c in polymer.strip():
        d[c] += 1
    print(f"{max(d.values()) - min(d.values())}")


def puzzle2(polymer, rules):
    count = collections.defaultdict(int)
    poly_dict = collections.defaultdict(int)
    polymer = polymer.strip()
    for c in polymer:
        count[c] += 1
    for i in range(len(polymer) - 1):
        poly_dict[f"{polymer[i]}{polymer[i+1]}"] += 1
    print(poly_dict)
    print(count)
    print()
    for i in range(40):
        new_poly_dict = poly_dict.copy()
        for k, v in poly_dict.items():
            if k in rules and v > 0:
                new_poly_dict[k] -= v
                new_poly_dict[f"{k[0]}{rules[k]}"] += v
                new_poly_dict[f"{rules[k]}{k[1]}"] += v
                count[rules[k]] += v
        poly_dict = new_poly_dict.copy()
    print(f"{max(count.values()) - min(count.values())}")


# puzzle1(polymer, rules)
puzzle2(polymer, rules)
# P1 4517
