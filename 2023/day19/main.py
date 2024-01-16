from os import confstr


class Rule:
    def __init__(self, description):
        splitted = description.split(":")
        self.op = None
        self.part = None
        self.value = None
        if len(splitted) == 1:
            self.result = description
        else:
            self.part = splitted[0][0]
            self.op = splitted[0][1]
            self.value = int(splitted[0][2:])
            self.result = splitted[1]

        self.is_rule_rejection_or_accepting = True if self.result in ["A", "R"] else False

    def is_evaluator(self):
        return self.op is not None
    
    def is_final(self):
        return self.result in ["A", "R"]

    def get_accept_range(self, rang):
        match self.op:
            case ">":
                return (max(self.value + 1, rang[0]), rang[1])
            case "<":
                return (rang[0], min(self.value, rang[1]))
            case _:
                raise Exception("Operator not found!")
    
    def get_reject_range(self, rang):
        match self.op:
            case ">":
                return (rang[0], min(self.value + 1, rang[1]))
            case "<":
                return (max(self.value, rang[0]), rang[1])
            case _:
                raise Exception("Operator not found!")


    def evaluate(self, other):
        match self.op:
            case ">":
                return other > self.value
            case "<":
                return other < self.value
            case _:
                raise Exception("Not an evaluator")
    
    def __repr__(self) -> str:
        if self.part is None:
            return f"RuleOp(result: {self.result})"
        else:
            return f"RuleOp(op: {self.op}, part: {self.part}, value: {self.value}, result: {self.result})"


def get_input():
    with open("input.txt") as file:
        workflows = dict()
        for line in file:
            if line == "\n":
                break
            workflow, rest = line.strip().split("{")
            ops = rest[:-1].split(",")
            rule_ops = [Rule(op) for op in ops]
            workflows[workflow] = rule_ops

        parts_input = []
        for line in file:
            parts_string = line.strip()[1:-1].split(",")
            parts = {part_string[0]: int(part_string[2:]) for part_string in parts_string}
            parts_input.append(parts)

        return workflows, parts_input

def first():
    workflows, parts_input = get_input()
    xmas_sum = 0

    for part in parts_input:
        current_rules = workflows["in"]
        part_resolved = False
        current_rule_i = 0

        while current_rule_i < len(current_rules):
            rule = current_rules[current_rule_i]
            if not rule.is_evaluator():
                if rule.is_final():
                    if rule.result == "A":
                        xmas_sum += sum(part.values())
                    part_resolved = True
                    break
                else:
                    current_rules = workflows[rule.result]
                    current_rule_i = 0
            else:
                # Evaluator rule
                if rule.evaluate(part[rule.part]):
                    if rule.is_final():
                        if rule.result == "A":
                            xmas_sum += sum(part.values())
                        part_resolved = True
                        break

                    current_rules = workflows[rule.result]
                    current_rule_i = 0
                else:
                    current_rule_i += 1
            
            if part_resolved:
                break

    print(f"Sum of all accepter parts is {xmas_sum}")


class Part:
    def __init__(self, workflow, rule_index, ranges) -> None:
        self.workflow = workflow
        self.rule_index = rule_index
        self.ranges = ranges

    def get_range(self, part):
        return self.ranges[part]

    def __repr__(self) -> str:
        return f"Part: {self.ranges}"


def is_rang_valid(rang) -> bool:
    return all(r[0] < r[1] for r in rang.values())


def num_poss(poss):
    sum = 1
    for r in poss.values():
        sum *= (r[1] - r[0])
    return sum


def second():
    workflows, _ = get_input()
    parts_queue = [Part("in", 0, {
        "x": (1, 4001),
        "m": (1, 4001),
        "a": (1, 4001),
        "s": (1, 4001),
    })]
    sum_possibilities = 0

    while parts_queue:

        current_part = parts_queue.pop()
        current_wf = workflows[current_part.workflow]
        current_rule = current_wf[current_part.rule_index]

        if not current_rule.is_evaluator():
            if current_rule.is_final():
                if current_rule.result == "A" and is_rang_valid(current_part.ranges):
                    current_part_possibilities = num_poss(current_part.ranges)
                    sum_possibilities += current_part_possibilities
            else:
                new_part = Part(current_rule.result, 0, current_part.ranges.copy())
                parts_queue.append(new_part)
        else:
            # This is evaluator meaning we have both ranges, reject and accept
            new_rang_reject = current_part.ranges.copy()
            new_rang_reject[current_rule.part] = current_rule.get_reject_range(current_part.get_range(current_rule.part)) 
            if not is_rang_valid(new_rang_reject):
                continue
            part_reject = Part(current_part.workflow, current_part.rule_index + 1, new_rang_reject)
            parts_queue.append(part_reject)

            new_rang_accept = current_part.ranges.copy()
            new_rang_accept[current_rule.part] = current_rule.get_accept_range(current_part.get_range(current_rule.part)) 
            if not is_rang_valid(new_rang_accept):
                continue
            if current_rule.is_final():
                if current_rule.result == "A" and is_rang_valid(new_rang_accept):
                    sum_possibilities += num_poss(new_rang_accept)
            else:
                part_acc = Part(current_rule.result, 0, new_rang_accept)
                parts_queue.append(part_acc)

    print(f"Max num of possibilities {sum_possibilities}")


first()
second()
