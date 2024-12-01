from collections import Counter


def first_part():
    with open("input.txt") as file:
        left_list, right_list = zip(
            *[
                (int(left), int(right))
                for line in file
                for left, right in [line.split()]
            ]
        )
    sum_dist = sum(
        abs(left - right) for left, right in zip(sorted(left_list), sorted(right_list))
    )

    print(f"Min sum of distances between left and right is: {sum_dist}")


def second_part():
    map_of_apperances = Counter()
    similarity_sum = 0

    with open("input.txt") as file:
        for line in file:
            left, right = map(int, line.split())
            similarity_sum += left * map_of_apperances[right]
            map_of_apperances[right] += 1    
    print(f"Similarity score is {similarity_sum}")


first_part()
second_part()
