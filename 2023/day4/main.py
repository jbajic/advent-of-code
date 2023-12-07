def get_card_id(card_info):
    _, id = card_info.split()
    return int(id)


def get_nums_seperated(nums):
    winning_nums, card_nums = nums.split("|")
    winning_nums = [int(e) for e in winning_nums.strip().split()]
    card_nums = [int(e) for e in card_nums.strip().split()]

    return winning_nums, card_nums

def first():
    with open("input.txt") as file:
        all_points = []
        for l in file:
            _, nums = l.split(":")
            winning_nums, card_nums = get_nums_seperated(nums)

            num_of_winning_nums = 0
            for card_num in card_nums:
                if card_num in winning_nums:
                    num_of_winning_nums += 1

            points = 0
            if num_of_winning_nums > 0:
                num_of_winning_nums -= 1
                points = 1
                while num_of_winning_nums > 0:
                    points *= 2
                    num_of_winning_nums -= 1

            all_points.append(points)

        print(f"Sum of all winning nums points {sum(all_points)}")


def second():
    with open("input.txt") as file:
        scratchcards = dict()

        def bump_up_card(bump_up_card_id):
            if bump_up_card_id in scratchcards:
                scratchcards[bump_up_card_id] += 1
            else:
                scratchcards[bump_up_card_id] = 1

        for l in file:
            card_info, nums = l.split(":")
            card_id = get_card_id(card_info)
            bump_up_card(card_id)
            winning_nums, card_nums = get_nums_seperated(nums)

            num_of_winning_nums = 0
            for card_num in card_nums:
                if card_num in winning_nums:
                    num_of_winning_nums += 1

            starting_id = card_id + 1
            for other_card_id in range(starting_id, starting_id + num_of_winning_nums):
                num_of_card_copies = scratchcards[card_id]
                for _ in range(num_of_card_copies):
                    bump_up_card(other_card_id)
        print(f"Number of strachcards points: {sum(scratchcards.values())}")

first()
second()

