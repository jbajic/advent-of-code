from dataclasses import dataclass
from typing import Optional


def get_literal_operand(operand):
    return operand


def get_combo_operand(operand, registers):
    match operand:
        case operand if 0 <= operand < 4:
            return operand
        case 4:
            return registers["A"]
        case 5:
            return registers["B"]
        case 6:
            return registers["C"]
        case _:
            raise Exception("Using unknown register!")


@dataclass
class Result:
    output: Optional[int]
    instruction_ptr: Optional[int]


def do_op(num, operand, registers):
    match num:
        case 0:
            # adv
            registers["A"] = int(
                registers["A"] / pow(2, get_combo_operand(operand, registers))
            )
        case 1:
            # bxl
            registers["B"] = registers["B"] ^ get_literal_operand(operand)
        case 2:
            # bst
            registers["B"] = get_combo_operand(operand, registers) % 8
        case 3:
            # jnz
            if registers["A"] == 0:
                return None
            return Result(None, get_literal_operand(operand))
        case 4:
            # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        case 5:
            # out
            output = get_combo_operand(operand, registers) % 8
            return Result(output, None)
        case 6:
            # bdv
            registers["B"] = int(
                registers["A"] / pow(2, get_combo_operand(operand, registers))
            )
        case 7:
            # cdv
            registers["C"] = int(
                registers["A"] / pow(2, get_combo_operand(operand, registers))
            )
        case _:
            raise Exception("Using unknown op!")

    return None


def first_part():
    registers = dict()
    program = []
    with open("input.txt") as file:
        for line in file:
            if line.strip() == "":
                break
            splitted = line.strip().split(" ")
            registers[splitted[1][0]] = int(splitted[2])
        for line in file:
            splitted = line.strip().split()
            program = list(map(int, splitted[1].split(",")))

    output = []
    i = 0
    while i < len(program):
        op_i = i
        operand_i = i + 1
        print(f"Registers: {registers}")
        print(f"i: {op_i} Op {program[op_i]} and operand {program[operand_i]}")
        res = do_op(program[op_i], program[operand_i], registers)
        print(f"Res is {res}")
        if res:
            if res.output is not None:
                output.append(res.output)
            if res.instruction_ptr is not None:
                i = res.instruction_ptr
                print(f"Restarting to {i}...")
                continue
        print(f"Registers: {registers}")
        print(f"Output: {output}")
        print("===================")
        i += 2

    print(output)
    print(f"The program output is {','.join(map(str, output))}")



first_part()
