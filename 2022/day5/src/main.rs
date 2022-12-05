use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

struct Move {
    amount: usize,
    from: usize,
    to: usize,
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn read_cargo_and_moves() -> (Vec<String>, Vec<String>) {
    let mut cargo_lines: Vec<String> = Vec::new();
    let mut moves_lines: Vec<String> = Vec::new();
    let mut newline_found = false;
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                if !newline_found && l == "" {
                    newline_found = true;
                    continue;
                } else if !newline_found {
                    cargo_lines.push(l);
                    continue;
                } else {
                    moves_lines.push(l);
                }
            }
        }
    }
    return (cargo_lines, moves_lines);
}

fn get_cargo_stacks(cargo_lines: &mut Vec<String>) -> Vec<Vec<char>> {
    let mut cargo: Vec<Vec<char>> = Vec::new();
    if let Some(stacks_line) = cargo_lines.pop() {
        for elem in stacks_line.chars() {
            if elem != ' ' {
                cargo.push(Vec::new());
            }
        }
    }

    for cargo_line in cargo_lines.iter().rev() {
        let mut cargo_index = 0;
        for chunk in cargo_line.chars().collect::<Vec<char>>().chunks(4) {
            if chunk[1] != ' ' {
                cargo[cargo_index].push(chunk[1]);
            }
            cargo_index += 1;
        }
    }
    return cargo;
}

fn get_moves(moves_lines: &Vec<String>) -> Vec<Move> {
    let mut moves: Vec<Move> = Vec::new();
    for move_line in moves_lines.iter() {
        let splitted: Vec<&str> = move_line.split(" ").collect();
        moves.push(Move {
            amount: splitted[1].parse::<usize>().unwrap(),
            from: splitted[3].parse::<usize>().unwrap(),
            to: splitted[5].parse::<usize>().unwrap(),
        });
    }
    return moves;
}

fn move_cargo_one_by_one(cargo_stacks: &mut Vec<Vec<char>>, movements: &Vec<Move>) {
    for cargo_move in movements.iter() {
        for _ in 0..cargo_move.amount {
            if let Some(moving_elem) = cargo_stacks[cargo_move.from -1].pop() {
                cargo_stacks[cargo_move.to - 1].push(moving_elem);
            }
        }
    }

    let mut last_cargo: String = String::new();
    for cargo in cargo_stacks.iter() {
        if let Some(front) = cargo.last() {
            last_cargo.push(*front);
        }
    }
    println!("{}", last_cargo);
}

fn move_cargo_in_chunk(cargo_stacks: &mut Vec<Vec<char>>, movements: &Vec<Move>) {
    for cargo_move in movements.iter() {
        let from_cargo_size = cargo_stacks[cargo_move.from -1].len() as usize;
        let range_from = from_cargo_size - cargo_move.amount;
        let moving: Vec<char> = cargo_stacks[cargo_move.from -1].drain(range_from..from_cargo_size).collect();
        cargo_stacks[cargo_move.to -1].extend_from_slice(&moving);
    }

    let mut last_cargo: String = String::new();
    for cargo in cargo_stacks.iter() {
        if let Some(front) = cargo.last() {
            last_cargo.push(*front);
        }
    }
    println!("{}", last_cargo);
}


fn main() {
    let (mut cargo_lines, moves_lines) = read_cargo_and_moves();
    let mut cargo_stacks = get_cargo_stacks(&mut cargo_lines);
    let movements = get_moves(&moves_lines);

    // move_cargo_one_by_one(&mut cargo_stacks, &movements);
    move_cargo_in_chunk(&mut cargo_stacks, &movements);
}
