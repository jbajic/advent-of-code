def first():
    with open("input.txt", "r") as file:
        numbers = []
        for line in file:
            print(f"Line {line}")
            first, second = None, None
            for c in line:
                if c.isdigit():
                    first = c
                    break
            for c in reversed(line):
                if c.isdigit():
                    second = c
                    break
            numbers.append(int(first) * 10 + int(second))
                
        print(numbers)
        print(f"Calibration is {sum(numbers)}")

def numberfy(a):
    match a:
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case "six":
            return 6
        case "seven":
            return 7
        case "eight":
            return 8
        case "nine":
            return 9
        case _:
            return None

def try_numberfy(a):
    length = len(a)
    if length - 2 < 0:
        return None
    s = "".join(a).strip()
    print(f"{s}")
    for i in range(length):
        for j in range(i+2, length + 1):
            n = numberfy(s[i:j])
            print(f"Numerfy: {s[i:j]} = {n}")
            if (n := numberfy(s[i:j])) is not None:
                return n

    return None

def second():
    with open("input.txt", "r") as file:
        numbers = []
        for line in file:
            first, second = [], []
            for c in line:
                first.append(c)
                if c.isdigit():
                    first = c
                    break
                elif (n := try_numberfy(first)) is not None:
                    first = n
                    break

            for c in reversed(line):
                second.insert(0, c)
                if c.isdigit():
                    second = c
                    break
                elif (n := try_numberfy(second)) is not None:
                    second = n
                    break
                
            print(f"First and second: {first} {second}")
            numbers.append(int(first) * 10 + int(second))
        print(f"Calibration is {sum(numbers)}")

# first()
second()
