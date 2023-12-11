def extrapolate_last_elem(diffs):
    prev_diff = 0
    for diff in reversed(diffs):
       diff.append(diff[-1] + prev_diff)
       prev_diff = diff[-1]

    return diffs


def first():
    with open("input.txt") as file:
        sequances = []
        for line in file:
            sequances.append([int(e) for e in line.strip().split()])

        extrapolated_elements = []
        for seq in sequances:
            diffs = [seq]
            while any(e != 0 for e in diffs[-1]):
                current_seq = diffs[-1]
                current_diff = []
                for first, second in zip(current_seq[0:-1], current_seq[1:]):
                    current_diff.append(second - first)
                diffs.append(current_diff)

            diffs = extrapolate_last_elem(diffs)
            extrapolated_elements.append(diffs[0][-1])

        print(f"Sum of extrapolated elements {sum(extrapolated_elements)}")


def extrapolate_first_elem(diffs):
    prev_diff = 0
    for diff in reversed(diffs):
       diff.insert(0, diff[0] - prev_diff)
       prev_diff = diff[0]

    return diffs


def second():
    with open("input.txt") as file:
        sequances = []
        for line in file:
            sequances.append([int(e) for e in line.strip().split()])

        extrapolated_elements = []
        for seq in sequances:
            diffs = [seq]
            while any(e != 0 for e in diffs[-1]):
                current_seq = diffs[-1]
                current_diff = []
                for first, second in zip(current_seq[0:-1], current_seq[1:]):
                    current_diff.append(second - first)
                diffs.append(current_diff)

            diffs = extrapolate_first_elem(diffs)
            extrapolated_elements.append(diffs[0][0])

        print(f"Sum of extrapolated elements {sum(extrapolated_elements)}")

first()
second()
