use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn get_max_value(vec: &Vec<i32>) {
    let max_value = vec.iter().max();
    match max_value {
        Some(max) => {
            println!("Max calories are is {}", max)
        }
        None => {
            println!("There are no calories found!")
        }
    }
}

fn get_top_3_calories_values(vec: &mut Vec<i32>) {
    vec.sort();
    let sum:i32 = vec.iter().rev().take(3).sum();
    println!("Top 3 max calories summed are is {}", sum);
}

fn main() {
    let mut vec: Vec<i32> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(line) = line {
                if line == "" {
                    vec.push(0);
                } else if let Some(last) = vec.last_mut() {
                    *last += line.parse::<i32>().unwrap();
                }
            }
        }
    }
    get_max_value(&vec);
    get_top_3_calories_values(&mut vec);
}
