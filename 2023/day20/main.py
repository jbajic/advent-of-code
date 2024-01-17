from enum import Enum

def get_input():
    with open("input.txt") as file:
        mapping = dict()
        for line in file:
            source, destinations = line.strip().split(" -> ")
            mapping[source] = [d.replace("&", "").replace("%", "") for d in destinations.split(", ")]
        return mapping


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class Broadcast:
    def __init__(self, name):
        self.name = name
        self.pulse = Pulse.LOW

    def receive(self, pulse: Pulse, source):
        self.pulse = pulse
        return self.pulse

    def __repr__(self) -> str:
        return f"Broadcast: {self.pulse}"


class FlipFlop:
    def __init__(self, name):
        self.name = name
        self.on = False

    def receive(self, pulse: Pulse, source):
        match pulse:
            case Pulse.LOW:
                self.on = not self.on
                if self.on:
                    return Pulse.HIGH
                else:
                    return Pulse.LOW
            case Pulse.HIGH:
                return None
            case _:
                raise Exception("Pulse must be one of enums")

    
    def __repr__(self) -> str:
        return f"FlipFlop: {self.on}"


class Conjuction:
    def __init__(self, name, modules) -> None:
        self.name = name
        self.inputs = dict()
        for k, v in modules.items():
            if name[1:] in v:
                stripped_name = k.replace("&", "").replace("%","")
                self.inputs[stripped_name] = Pulse.LOW

    def receive(self, pulse: Pulse, source):
        self.inputs[source] = pulse
        if all(input == Pulse.HIGH for input in self.inputs.values()):
            return Pulse.LOW
        return Pulse.HIGH
    
    def __repr__(self) -> str:
        return f"Conjuction: {self.inputs}"


def generate_states(input):
    states = dict()
    for module in input.keys():
        if module == "broadcaster":
            states[module] = Broadcast(module)
        elif module[0] == "%":
            states[module[1:]] = FlipFlop(module)
        elif module[0] == "&":
            states[module[1:]] = Conjuction(module, input)

    return states


def first():
    network = get_input()
    states = generate_states(network)


    num_of_low_pulses = 0
    num_of_high_pulses = 0

    for i in range(1000):
        num_of_low_pulses += 1
        action_queue = [("broadcaster", Pulse.LOW, None)]
        while action_queue:
            current_module, current_pulse, source_module = action_queue.pop(0)
                   
            if current_module not in states:
                continue

            send_pulse = states[current_module].receive(current_pulse, source_module)
            if send_pulse is None:
                continue

            if send_pulse == Pulse.LOW:
                num_of_low_pulses += len(network[states[current_module].name])
            else:
                num_of_high_pulses += len(network[states[current_module].name])

            for dest in network[states[current_module].name]:
                action_queue.append((dest, send_pulse, current_module))

    print(f"Low {num_of_low_pulses}")
    print(f"High {num_of_high_pulses}")
    print(f"Product of high and low pulses is {num_of_low_pulses * num_of_high_pulses}")


def second():
    network = get_input()
    states = generate_states(network)

    num_of_low_pulses = 0
    num_of_high_pulses = 0

    found_end = False
    while True:
        num_of_low_pulses += 1
        action_queue = [("broadcaster", Pulse.LOW, None)]
        while action_queue:
            current_module, current_pulse, source_module = action_queue.pop(0)
                   
            if current_module not in states and current_pulse == Pulse.LOW:
                found_end = True
                break

            send_pulse = states[current_module].receive(current_pulse, source_module)
            if send_pulse is None:
                break

            if send_pulse == Pulse.LOW:
                num_of_low_pulses += len(network[states[current_module].name])
            else:
                num_of_high_pulses += len(network[states[current_module].name])

            for dest in network[states[current_module].name]:
                action_queue.append((dest, send_pulse, current_module))
        if found_end:
            break

    print(f"Low {num_of_low_pulses}")
    print(f"High {num_of_high_pulses}")
    print(f"Product of high and low pulses is {num_of_low_pulses * num_of_high_pulses}")


# first()
second()

