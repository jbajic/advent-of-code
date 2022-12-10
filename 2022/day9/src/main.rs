use std::collections::HashSet;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::str::FromStr;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

#[derive(Debug, Copy, Clone)]
enum Direction {
    UP,
    DOWN,
    LEFT,
    RIGHT,
}

impl FromStr for Direction {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "U" => Ok(Direction::UP),
            "D" => Ok(Direction::DOWN),
            "L" => Ok(Direction::LEFT),
            "R" => Ok(Direction::RIGHT),
            _ => Err(()),
        }
    }
}

#[derive(Debug)]
struct Movement {
    dir: Direction,
    length: i32,
}

fn read_motions() -> Vec<Movement> {
    let mut movements: Vec<Movement> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                let splitted: Vec<_> = l.split(" ").collect();
                movements.push(Movement {
                    dir: Direction::from_str(splitted[0]).unwrap(),
                    length: splitted[1].parse::<i32>().unwrap(),
                });
            }
        }
    }
    return movements;
}

fn move_head(head: (i32, i32), dir: Direction) -> (i32, i32) {
    match dir {
        Direction::UP => (head.0 + 1, head.1),
        Direction::DOWN => (head.0 - 1, head.1),
        Direction::LEFT => (head.0, head.1 - 1),
        Direction::RIGHT => (head.0, head.1 + 1),
    }
}

fn are_adjacent(head: (i32, i32), tail: (i32, i32)) -> bool {
    i32::abs(head.0 - tail.0) < 2 && i32::abs(head.1 - tail.1) < 2
}

fn get_unique_tail_positions(motions: &Vec<Movement>) -> usize {
    let mut positions: HashSet<(i32, i32)> = HashSet::new();
    positions.insert((0, 0));
    let mut head = (0, 0);
    let mut tail = head;
    for motion in motions.iter() {
        for _ in 0..motion.length {
            let moved_head = move_head(head, motion.dir);
            if !are_adjacent(moved_head, tail) {
                tail = head;
                positions.insert(tail);
            }
            head = moved_head;
        }
    }
    // println!("{:?}", positions);
    return positions.len();
}

fn get_next_move(current: &(i32, i32), next: &(i32, i32)) -> (i32, i32) {
    let mut x = current.0;
    let mut y = current.1;
    if current.0 > next.0 {
        x = current.0 - 1;
    } else if current.0 < next.0 {
        x = current.0 + 1;
    }
    if current.1 > next.1 {
        y = current.1 - 1;
    } else if current.1 < next.1 {
        y = current.1 + 1;
    }
    return (x, y);
}

fn get_unique_long_rope_tail_positions(motions: &Vec<Movement>) -> usize {
    let mut positions: HashSet<(i32, i32)> = HashSet::new();
    let mut head = (0, 0);
    positions.insert(head);
    let mut tail: [(i32, i32); 9] = [head; 9];
    let mut states: Vec<Vec<(i32, i32)>> = Vec::new();
    for motion in motions.iter() {
        for _ in 0..motion.length {
            let mut state: Vec<(i32, i32)> = Vec::new();
            let moved_head = move_head(head, motion.dir);
            state.push(moved_head);

            let mut part_in_front = head;
            for tail_part in tail.iter_mut() {
                if !are_adjacent(*tail_part, part_in_front) {
                    *tail_part = get_next_move(tail_part, &part_in_front);
                    part_in_front = *tail_part;
                } else {
                    part_in_front = *tail_part;
                }
            }
            positions.insert(tail[tail.len() - 1]);
            tail.iter().for_each(|&c| state.push(c));
            head = moved_head;
            assert!(state.len() == 10);
            states.push(state);
        }
        // break;
    }

    return positions.len();
}

fn main() {
    let motions = read_motions();
    println!("{}", are_adjacent((2, 2), (3, 1)));

    println!(
        "There are {} unique position",
        get_unique_tail_positions(&motions)
    );
    println!(
        "There are {} unique position with long rope",
        get_unique_long_rope_tail_positions(&motions)
    );
}
