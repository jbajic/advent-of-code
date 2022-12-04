use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

struct Rucksack(String, String);

fn get_item_score(item: char) -> i32 {
    let ascii_val = item as i32;
    if ascii_val > 96 {
        return ascii_val as i32 - 97 + 1;
    } else {
        ascii_val as i32 - 65 + 26 + 1
    }
}

fn get_sum_matching_items(rucksacks: &Vec<Rucksack>) -> i32 {
    let mut score = 0;
    for rucksack in rucksacks.iter() {
        if let Some(common) = rucksack.0.chars().find(|&c| rucksack.1.contains(c)) {
            score += get_item_score(common);
        } else {
            panic!("No common item");
        }
    }
    return score;
}

fn get_sum_matching_items_pre_group(rucksacks: &Vec<Rucksack>) -> i32 {
    let mut score = 0;
    for group in rucksacks.chunks(3) {
        let mut sets: Vec<HashSet<char>> = Vec::new();
        for rucksack in group.iter() {
            let mut set: HashSet<char> = HashSet::new();
            rucksack.0.chars().for_each(|c| {set.insert(c);});
            rucksack.1.chars().for_each(|c| {set.insert(c);});
            sets.push(set);
        }
        let (intersection, others) = sets.split_at_mut(1);
        let intersection = &mut intersection[0];
        for other in others {
            intersection.retain(|e| other.contains(e));
        }
        let common = intersection.iter().next().unwrap();
        score += get_item_score(*common);
    }
    return score;
}

fn main() {
    let mut rucksacks: Vec<Rucksack> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(line) = line {
                assert!(line.len() % 2 == 0);
                let (split1, split2) = line.split_at(line.len() / 2);
                rucksacks.push(Rucksack(split1.to_string(), split2.to_string()));
            }
        }
    }

    println!(
        "Sum of matching items is {}",
        get_sum_matching_items(&rucksacks)
    );
    println!(
        "Sum of matching per group items is {}",
        get_sum_matching_items_pre_group(&rucksacks)
    );
}
