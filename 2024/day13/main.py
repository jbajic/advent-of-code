from collections import namedtuple
from dataclasses import dataclass
from itertools import product
import numpy as np

Button = namedtuple("Button", ["x", "y"])

@dataclass
class Configuration:
    button_a: Button
    button_b: Button
    prize: tuple[int, int]

def get_button_increase(button):
    splitted = button.split()
    x_splitted = splitted[2].split("+")
    y_splitted = splitted[3].split("+")
    
    return int(x_splitted[1].replace(",", "")), int(y_splitted[1])

def get_prize(prize):
    splitted = prize.split()
    x_splitted = splitted[1].split("=")
    y_splitted = splitted[2].split("=")
    
    return int(x_splitted[1].replace(",", "")), int(y_splitted[1])


def first_part():
    lines = []
    with open("input.txt") as file:
        lines = [line.strip() for line in file if line != "\n"]

    claw_machines = []
    for i in range(0, len(lines), 3):
        a_x, a_y = get_button_increase(lines[i])
        b_x, b_y = get_button_increase(lines[i + 1])
        prize_x, prize_y = get_prize(lines[i+2])
        claw_machines.append(Configuration(Button(a_x, a_y), Button(b_x, b_y), (prize_x, prize_y)))

    tokens = 0
    for cm in claw_machines:
        # e.g.
        # 94a + 22b = 8400
        # 34a + 67b = 5400
        equations = np.array([[cm.button_a.x, cm.button_b.x], [cm.button_a.y, cm.button_b.y]])
        # Equations are independent, only one solution
        rank = np.linalg.matrix_rank(equations)
        assert rank == equations.shape[0]

        other_side = np.array([cm.prize[0], cm.prize[1]])
        solution = np.linalg.solve(equations, other_side)
        assert len(solution) == 2

        solution = list(map(round, solution))
        if (solution[0] * cm.button_a.x + solution[1] * cm.button_b.x) != cm.prize[0] or \
            (solution[0] * cm.button_a.y + solution[1] * cm.button_b.y) != cm.prize[1]:
            continue
        if solution[0] > 100 or solution[1] > 100 or solution[0] < 0 or solution[1] < 0:
            continue

        tokens += 3 * solution[0] + solution[1]
    print(f"Tokens used {int(tokens)}")
        

# Brute force
def first_part_2():
    lines = []
    with open("input.txt") as file:
        lines = [line.strip() for line in file if line != "\n"]

    claw_machines = []
    for i in range(0, len(lines), 3):
        a_x, a_y = get_button_increase(lines[i])
        b_x, b_y = get_button_increase(lines[i + 1])
        prize_x, prize_y = get_prize(lines[i+2])
        claw_machines.append(Configuration(Button(a_x, a_y), Button(b_x, b_y), (prize_x, prize_y)))

    tokens = 0
    for cm in claw_machines:
        min_tokens = None
        s1, s2 = None, None
        for sol1, sol2 in product(list(range(0, 100)), list(range(0, 100))):
            if (sol1 * cm.button_a.x + sol2 * cm.button_b.x) == cm.prize[0] and \
                (sol1 * cm.button_a.y + sol2 * cm.button_b.y) == cm.prize[1]:
                if min_tokens is None:
                    min_tokens = sol1 * 3 + sol2
                    s1, s2 = sol1, sol2
                else:
                    if min_tokens > (sol1 * 3 + sol2):
                        s1, s2 = sol1, sol2
                    min_tokens = min(min_tokens, sol1 * 3 + sol2)

        if min_tokens is not None:
            tokens += min_tokens
    print(f"Numer of tokens {tokens}")


        
def second_part():
    lines = []
    with open("input.txt") as file:
        lines = [line.strip() for line in file if line != "\n"]

    claw_machines = []
    for i in range(0, len(lines), 3):
        a_x, a_y = get_button_increase(lines[i])
        b_x, b_y = get_button_increase(lines[i + 1])
        prize_x, prize_y = get_prize(lines[i+2])
        claw_machines.append(Configuration(Button(a_x, a_y), Button(b_x, b_y), (prize_x + 10000000000000, prize_y + 10000000000000)))

    tokens = 0
    for cm in claw_machines:
        # e.g.
        # 94a + 22b = 8400
        # 34a + 67b = 5400
        equations = np.array([[cm.button_a.x, cm.button_b.x], [cm.button_a.y, cm.button_b.y]])
        # Equations are independent, only one solution
        rank = np.linalg.matrix_rank(equations)
        assert rank == equations.shape[0]

        other_side = np.array([cm.prize[0], cm.prize[1]])
        solution = np.linalg.solve(equations, other_side)
        assert len(solution) == 2

        solution = list(map(round, solution))
        if (solution[0] * cm.button_a.x + solution[1] * cm.button_b.x) != cm.prize[0] or \
            (solution[0] * cm.button_a.y + solution[1] * cm.button_b.y) != cm.prize[1]:
            continue

        tokens += 3 * solution[0] + solution[1]
    print(f"Tokens used {int(tokens)}")
        

# 24189
first_part()
second_part()
