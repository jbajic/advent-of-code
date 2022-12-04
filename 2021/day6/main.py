def get_initial_state():
    initial_state = []
    with open("input.txt") as input:
        text = input.readline()
        initial_state = [int(elem) for elem in text.split(",")]
    return initial_state


def get_number_of_fishes(initial_states, days):
    states = dict.fromkeys(range(9), 0)
    for initial_state in initial_states:
        states[initial_state] += 1

    for _ in range(days):
        print(states)
        new_state = states.copy()
        for i, value in states.items():
            if i == 0:
                print(value)
                new_state[6] += value
                new_state[8] += value
                new_state[i] = 0
            else:
                new_state[i] -= value
                new_state[i - 1] += value
        states = new_state

    # print(states)
    # print(len(states))
    return sum(states.values())


def main():
    states = get_initial_state()

    print(get_number_of_fishes(states, 256))


if __name__ == "__main__":
    main()
