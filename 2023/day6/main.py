from functools import reduce
from math import isqrt
from tqdm import tqdm


def get_numbers(l):
    _, nums = l.split(":")
    nums = nums.strip().split()
    return [int(n) for n in nums]


def get_number_of_ways_to_beat_record(time, distance):
    better_times = 0
    for i in range(1, distance):
        current_time = time
        distance_passed = 0

        current_time -= i
        while current_time > 0 and distance_passed <= distance:
            distance_passed += i
            current_time -= 1
        if distance_passed > distance:
            better_times += 1
    return better_times


def first():
    with open("input.txt") as file:
        lines = file.readlines()
        times = get_numbers(lines[0])
        distances = get_numbers(lines[1])

        number_of_ways_to_beat_record = []
        for time, distance in zip(times, distances):
            better_times = get_number_of_ways_to_beat_record(time, distance)
            number_of_ways_to_beat_record.append(better_times)
        ways_multiplied = reduce((lambda x, y: x * y), number_of_ways_to_beat_record)
        print(f"Ways to beat record multiplied {ways_multiplied}")


def does_this_speed_beat_record(time, record, speed):
    current_time = time - speed
    return current_time * speed >= record


def bin_search_last_way(first, last, time, record):
    start = first
    end = last
    mid = start + (end - start) // 2

    while end >= start:
        mid = start + (end - start) // 2
        if does_this_speed_beat_record(time, record, mid):
            if not does_this_speed_beat_record(time, record, mid + 1):
                return mid
            else:
                start = mid + 1
        else:
            end = mid - 1

    return None


def second():
   with open("input.txt") as file:
        lines = file.readlines()
        time = lines[0].split(":")[1].strip().split()
        time = int("".join(time))
        distance = lines[1].split(":")[1].strip().split()
        distance = int("".join(distance))

        print(time)
        print(distance)

        first_better_way = None
        last_better_way = None
        for i in tqdm(range(1, distance)):
            if does_this_speed_beat_record(time, distance, i):
                first_better_way = i
                break
        last_better_way = bin_search_last_way(first_better_way, distance, time, distance) 
                
        ways_to_break_record = last_better_way - first_better_way + 1
        print(f"Ways to beat record multiplied {ways_to_break_record}")
 

first()
second()
