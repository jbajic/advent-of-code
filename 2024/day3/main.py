import re

def first_part():
    with open("input.txt") as file:
        sum = 0
        for line in file:
            matches = re.findall(r"mul\((\d+,\d+)\)", line)
            for pair in matches:
                x, y = map(int, pair.split(","))
                sum += x * y
        print(f"Sum is {sum}")

def second_part():
    with open("input.txt") as file:
        sum = 0
        enable = True
        window_size = 4

        text = "".join(line.strip() for line in file)
        for i in range(len(text) - window_size + 1):
            seq = text[i: i + window_size]
            match seq:
                case "do()":
                    enable = True
                case "don'":
                    current = i + window_size
                    # Check for t()
                    if current + 3 < len(text) and text[current:current+3] == "t()":
                        enable = False
                case "mul(":
                    if enable:
                        current = i + window_size
                        while text[current] != ")":
                            current += 1
                        try:
                            left, right = map(int, text[i+window_size:current].split(","))
                            sum += left * right
                        except:
                            continue
                                
                            
        print(f"Sum is {sum}")



first_part()
second_part()
