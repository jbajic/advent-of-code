use array2d::Array2D;
use std::cmp;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, Copy,  Clone)]
struct Point(i32, i32);

#[derive(Debug)]
struct Line {
    from: Point,
    to: Point,
}

fn fill_pipes(pipes: &mut Array2D<i32>, lines: &Vec<Line>, diagonal: bool) {
    for line in lines.iter() {
        // println!("Line {:?}", line);
        if line.from.1 == line.to.1 && line.from.0 != line.to.0 {
            // on x axis
            let start: i32 = cmp::min(line.from.0, line.to.0);
            let end: i32 = cmp::max(line.from.0, line.to.0) + 1;
            for i in start..end {
                pipes[(line.from.1 as usize, i as usize)] += 1;
            }
        } else if line.from.0 == line.to.0 && line.from.1 != line.to.1 {
            // on y axis
            let start: i32 = cmp::min(line.from.1, line.to.1);
            let end: i32 = cmp::max(line.from.1, line.to.1) + 1;
            for i in start..end {
                pipes[(i as usize, line.from.0 as usize)] += 1;
            }
        } else if diagonal {
            // diagonal lines
            // println!("Diagonal!");
            let start = line.from;
            let end = line.to;
            let mut i: i32 = 0;
            let mut j: i32 = 0;
            loop {
                pipes[((start.1 + j) as usize, (start.0 + i) as usize)] += 1;
                if start.0 + i == end.0 {
                    break;
                }
                if start.0 + i < end.0 {
                    i += 1;
                } else {
                    i -= 1;
                }
                if start.1 + j < end.1 {
                    j += 1;
                } else {
                    j -= 1;
                }
            }
        }
        // print_pipes(pipes);
    }
}

fn main() {
    // File hosts must exist in current path before this produces output
    let mut lines_vec: Vec<Line> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(ip) = line {
                lines_vec.push(create_line(ip));
            }
        }
    }

    let mut pipes = Array2D::filled_with(0, 1000, 1000);
    fill_pipes(&mut pipes, &lines_vec, true);
    print_pipes(&pipes);
    let mut sum = 0;
    for row_iter in pipes.rows_iter() {
        for element in row_iter {
            if element >= &2 {
                sum += 1;
            }
        }
    }
    println!("Sum is {}", sum);
}

fn print_pipes(pipes: &Array2D<i32>) {
    println!("All elements:");
    for row_iter in pipes.rows_iter() {
        for element in row_iter {
            if element == &0 {
                print!("* ");
            } else {
                print!("{} ", element);
            }
        }
        println!();
    }
}

fn create_line(line: String) -> Line {
    let from_to = line.split(" -> ");
    let vec: Vec<&str> = from_to.collect();

    let from_split = vec[0].split(",");
    let from_split: Vec<&str> = from_split.collect();
    let from = Point(
        from_split[0].parse::<i32>().unwrap(),
        from_split[1].parse::<i32>().unwrap(),
    );

    let to_split = vec[1].split(",");
    let to_split: Vec<&str> = to_split.collect();
    let to = Point(
        to_split[0].parse::<i32>().unwrap(),
        to_split[1].parse::<i32>().unwrap(),
    );

    Line { from, to }
}

// The output is wrapped in a Result to allow matching on errors
// Returns an Iterator to the Reader of the lines of the file.
fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
