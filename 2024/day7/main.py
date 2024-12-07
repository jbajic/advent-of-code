from dataclasses import dataclass
from itertools import product

@dataclass
class Equation:
    res: list
    nums: list

def first_part():
    equations = []
    with open("input.txt") as file:
        for line in file:
            res, nums = line.strip().split(":")
            equations.append(Equation(int(res), list(map(int, nums.split())))) 

    calibration = 0
    operations = ["*", "+"]
    for equation in equations:
        for ops in product(operations, repeat=len(equation.nums) - 1):
            sum = equation.nums[0]
            for i, op in enumerate(ops):
                match op:
                    case "*":
                        sum *= equation.nums[i+1]
                    case "+":
                        sum += equation.nums[i+1]
            if sum == equation.res:
                calibration += sum
                break
            

first_part()
second_part()
        
