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

#[derive(Copy, Clone, Debug, PartialEq)]
enum OperationType {
    ADD,
    NOOP,
}

#[derive(Copy, Clone, Debug)]
struct Operation {
    op: OperationType,
    num: i32,
}

impl FromStr for OperationType {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "addx" => Ok(OperationType::ADD),
            "noop" => Ok(OperationType::NOOP),
            _ => Err(()),
        }
    }
}

fn get_cycles(op: OperationType) -> i32 {
    match op {
        OperationType::ADD => 2,
        OperationType::NOOP => 1,
    }
}

fn read_operations() -> Vec<Operation> {
    let mut operations: Vec<Operation> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                let splitted: Vec<_> = l.split(" ").collect();
                let op = OperationType::from_str(splitted[0]).unwrap();
                let num = if op == OperationType::NOOP {
                    0
                } else {
                    splitted[1].parse::<i32>().unwrap()
                };
                operations.push(Operation { op: op, num: num });
            }
        }
    }
    return operations.into_iter().rev().collect();
}

fn get_signal_strength(mut operations: Vec<Operation>) -> i32 {
    let cycles = [20, 60, 100, 140, 180, 220];
    let mut current_cycle = 0;
    let mut x = 1;
    let mut sum = 0;

    let mut current_op = operations.pop().unwrap();
    let mut current_op_cycle = get_cycles(current_op.op);
    loop {
        current_cycle += 1;
        current_op_cycle -= 1;

        if cycles.contains(&current_cycle) {
            println!(
                "Reg is {} Signal at {} is {}",
                x,
                current_cycle,
                current_cycle * x
            );
            sum += current_cycle * x;
        }
        if operations.is_empty() && current_op_cycle == 0 {
            break;
        }

        if current_op_cycle == 0 {
            if current_op.op == OperationType::ADD {
                x = x + current_op.num;
            }
            current_op = operations.pop().unwrap();
            current_op_cycle = get_cycles(current_op.op);
        }
    }

    println!("Finished with {} cycles", current_cycle);
    return sum;
}

fn is_sprite_in_range(current_pixel: i32, sprite_position: i32) -> bool {
    return current_pixel >= sprite_position - 1 && current_pixel <= sprite_position + 1;
}

fn get_sprite_image(mut operations: Vec<Operation>) -> Vec<Vec<char>> {
    let mut crt_current_cycle: usize = 0;
    let mut x = 1;
    let mut sprite = vec![vec!['.'; 40]; 6];

    let mut current_op = operations.pop().unwrap();
    let mut current_op_cycle = get_cycles(current_op.op);
    loop {
        crt_current_cycle += 1;
        current_op_cycle -= 1;

        if crt_current_cycle >= 40 * 6 {
            break;
        }
        let i = (crt_current_cycle - 1usize) / 40;
        let j = (crt_current_cycle - 1usize) - 40 * i;
        let asdas = is_sprite_in_range(j as i32, x);
        if asdas {
            // Draw sprite
            sprite[i][j] = '#';
        }
        if operations.is_empty() && current_op_cycle == 0 {
            break;
        }
        if current_op_cycle == 0 {
            if current_op.op == OperationType::ADD {
                x = x + current_op.num;
            }
            current_op = operations.pop().unwrap();
            current_op_cycle = get_cycles(current_op.op);
        }
    }

    println!("Finished with {} cycles", crt_current_cycle);
    return sprite;
}

fn main() {
    let operations = read_operations();
    println!(
        "Signal strength is {}",
        get_signal_strength(operations.clone())
    );
    let sprite = get_sprite_image(operations);
    for row in sprite.iter() {
        for elem in row {
            print!("{}", elem);
        }
        println!("");
    }
}
