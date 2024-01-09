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

        self.is_the_last_rule = True if self.result in ["A", "R"] else False

    def is_evaluator(self):
        return self.value is not None
    
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
            print(parts_string)
            parts = {part_string[0]: int(part_string[2:]) for part_string in parts_string}
            parts_input.append(parts)

        return workflows, parts_input

def first():
    workflows, parts_input = get_input()
    xmas_sum = 0

    for part in parts_input:
        print(f"For part {part}")
        current_rules = workflows["in"]
        part_resolved = False
        current_rule_i = 0

        while current_rule_i < len(current_rules):
            rule = current_rules[current_rule_i]
            print(f"Current rule {rule}")
            if not rule.is_evaluator():
                if rule.is_the_last_rule:
                    if rule.result == "A":
                        xmas_sum += sum(part.values())
                        print(f"Part {part} is accepted")
                    else:
                        print(f"Part {part} is rejected")
                    part_resolved = True
                    break
                else:
                    print(f"Moving to workflow {rule.result}")
                    current_rules = workflows[rule.result]
                    current_rule_i = 0
            else:
                # Evaluator rule
                if rule.evaluate(part[rule.part]):
                    if rule.is_the_last_rule:
                        if rule.result == "A":
                            print(f"Part is {part}")
                            xmas_sum += sum(part.values())
                            print(f"Part {part} is accepted")
                        else:
                            print(f"Part {part} is rejected")
                        part_resolved = True
                        break

                    print(f"Moving to workflow {rule.result}")
                    current_rules = workflows[rule.result]
                    current_rule_i = 0
                else:
                    current_rule_i += 1
            
            if part_resolved:
                break

    print(f"Sum of all accepter parts is {xmas_sum}")


first()
