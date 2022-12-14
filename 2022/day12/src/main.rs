use priority_queue::DoublePriorityQueue;
use std::collections::{HashMap, HashSet};
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

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
struct Point(usize, usize);

fn read_input(input: &str) -> Vec<Vec<char>> {
    let mut field: Vec<_> = Vec::new();
    if let Ok(lines) = read_lines(input) {
        for line in lines {
            if let Ok(l) = line {
                field.push(l.chars().collect::<Vec<_>>());
            }
        }
    }
    return field;
}

fn get_mark_point(field: &Vec<Vec<char>>, point: char) -> Point {
    for (i, row) in field.iter().enumerate() {
        for (j, elem) in row.iter().enumerate() {
            if *elem == point {
                return Point(i, j);
            }
        }
    }
    panic!("Point not found!");
}

fn evaluate_point(item: char) -> i32 {
    match item {
        'S' => 0,
        'E' => 'z' as i32 - 97,
        'b' => 1,
        'a'..='z' => item as i32 - 97,
        _ => panic!("Cannot evaluate {}", item),
    }
}

fn get_path(path_map: &HashMap<Point, Point>, goal: Point) -> Vec<Point> {
    let mut current = goal;
    let mut path = Vec::new();
    path.push(current);
    while path_map.contains_key(&current) {
        current = path_map[&current].clone();
        path.push(current);
    }

    return path;
}

fn manhattan_dist(x: Point, y: Point) -> i32 {
    i32::abs(y.0 as i32 - x.0 as i32) + i32::abs(y.1 as i32 - x.1 as i32)
}

fn print_path(field: &Vec<Vec<char>>, path: &Vec<Point>) {
    for (i, row) in field.iter().enumerate() {
        for (j, _) in row.iter().enumerate() {
            let current_point = Point(i, j);
            if path.contains(&current_point) {
                print!(
                    "|{:>2}|",
                    path.iter().position(|&r| r == current_point).unwrap()
                );
            } else {
                print!("|. |");
            }
        }
        println!();
    }
}

fn a_star(field: &Vec<Vec<char>>, start: Point, end: Point) -> Vec<Point> {
    let mut visited: HashSet<Point> = HashSet::new();
    let mut queue = DoublePriorityQueue::new();
    let mut path_map: HashMap<Point, Point> = HashMap::new();

    queue.push(start, 0);
    while !queue.is_empty() {
        let current = queue.pop_min().unwrap();
        visited.insert(current.0);
        if current.0 == end {
            let path = get_path(&path_map, current.0);
            // print_path(field, &path);
            return path;
        }
        let current_field_eval = evaluate_point(field[current.0 .0][current.0 .1]);
        // println!(
        //     "Looking at item {} = {:?} with eval {}",
        //     field[current.0 .0][current.0 .1], current.0, current_field_eval
        // );
        for (i, j) in [(1, 0), (-1, 0), (0, 1), (0, -1)] {
            let x = current.0 .0 as i32 + i;
            let y = current.0 .1 as i32 + j;
            if x < 0 || y < 0 {
                continue;
            }
            let x = x as usize;
            let y = y as usize;
            if x >= field.len() || y >= field[0].len() {
                continue;
            }
            let possible_point = Point(x, y);
            let next_point_eval = evaluate_point(field[x][y]);
            if current_field_eval + 1 >= next_point_eval && !visited.contains(&possible_point) {
                path_map.insert(possible_point, current.0);
                queue.push(possible_point, current.1 + 1);
            }
        }
    }
    return Vec::new();
}

fn get_number_of_steps(field: &Vec<Vec<char>>) -> i32 {
    let start = get_mark_point(&field, 'S');
    let end = get_mark_point(&field, 'E');
    println!("Find path from {:?} to {:?}", start, end);
    let path = a_star(&field, start, end);

    return path.len() as i32 - 1;
}

fn get_number_of_steps_from_zero_elevation(field: &Vec<Vec<char>>) -> i32 {
    let end = get_mark_point(&field, 'E');
    let mut shortest_path = 100000;
    for (i, row) in field.iter().enumerate() {
        for (j, elem) in row.iter().enumerate() {
            if *elem == 'a' || *elem == 'S' {
                let start = Point(i, j);
                println!("Find path from {:?} to {:?}", start, end);
                let path = a_star(&field, start, end);
                if path.len() > 0 && path.len() < shortest_path {
                    shortest_path = path.len();
                }
            }
        }
    }

    return shortest_path as i32 - 1;
}

fn main() {
    let field = read_input(&"input.txt");
    let steps1 = get_number_of_steps(&field);
    let steps2 = get_number_of_steps_from_zero_elevation(&field);
    println!("Number of steps {}", steps1);
    println!("Number of steps {}", steps2);
}
