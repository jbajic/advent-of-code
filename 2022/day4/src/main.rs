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

fn are_contained(elf1: (i32, i32), elf2: (i32, i32)) -> bool {
    elf1.0 >= elf2.0 && elf1.1 <= elf2.1
}

fn find_fully_overlapping_assignments(elves_ranges: &Vec<(i32, i32)>) -> i32 {
    let mut count = 0;

    for elf_pair in elves_ranges.chunks(2) {
        if are_contained(elf_pair[0], elf_pair[1]) || are_contained(elf_pair[1], elf_pair[0]) {
            count += 1;
        }
    }
    count
}

fn find_overlapping_assignments(elves_ranges: &Vec<(i32, i32)>) -> i32 {
    let mut count = 0;

    for elf_pair in elves_ranges.chunks(2) {
        if are_contained(elf_pair[0], elf_pair[1]) || are_contained(elf_pair[1], elf_pair[0]) {
            count += 1;
        } else if elf_pair[0].1 >= elf_pair[1].0 && elf_pair[0].1 <= elf_pair[1].1 {
            count += 1;
        } else if elf_pair[0].0 >= elf_pair[1].0 && elf_pair[0].0 <= elf_pair[1].1 {
            count += 1;
        }
    }
    count
}

fn main() {
    let mut elves_ranges: Vec<(i32, i32)> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                l.split(",").by_ref().for_each(|elf| {
                    let elf_r: Vec<&str> = elf.split("-").collect();
                    elves_ranges.push((
                        elf_r[0].parse::<i32>().unwrap(),
                        elf_r[1].parse::<i32>().unwrap(),
                    ));
                });
            }
        }
    }

    println!(
        "There are fully {} overlapping assignments",
        find_fully_overlapping_assignments(&elves_ranges)
    );
    println!(
        "There are {} overlapping assignments",
        find_overlapping_assignments(&elves_ranges)
    );
}
