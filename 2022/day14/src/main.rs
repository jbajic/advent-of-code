use std::cmp;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug)]
struct Point(usize, usize);

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn read_input(input: &str) -> Vec<Vec<Point>> {
    let mut points = Vec::new();
    if let Ok(lines) = read_lines(input) {
        for line in lines {
            if let Ok(l) = line {
                let splitted_points = l.split(" -> ");
                let mut rock_points = Vec::new();
                for pair in splitted_points.into_iter() {
                    let splitted_coordinates = pair.split(",").collect::<Vec<&str>>();
                    rock_points.push(Point(
                        splitted_coordinates[1].parse::<usize>().unwrap(),
                        splitted_coordinates[0].parse::<usize>().unwrap(),
                    ));
                }
                points.push(rock_points);
            }
        }
    }
    return points;
}

static SIZE: usize = 1000;

fn get_field(rocks: &Vec<Vec<Point>>) -> Vec<Vec<char>> {
    let mut field = Vec::new();
    for _ in 0..SIZE {
        let mut row = Vec::new();
        for _ in 0..SIZE {
            row.push('.');
        }
        field.push(row);
    }
    field[0][500] = '+';
    for rock_structure in rocks.iter() {
        let mut prev_point = &rock_structure[0];
        for point in rock_structure {
            for i in cmp::min(prev_point.0, point.0)..cmp::max(prev_point.0, point.0) + 1 {
                field[i][point.1] = '#';
            }
            for i in cmp::min(prev_point.1, point.1)..cmp::max(prev_point.1, point.1) + 1 {
                field[point.0][i] = '#';
            }
            prev_point = point;
        }
    }
    return field;
}

fn simulate(mut field: Vec<Vec<char>>) -> i32 {
    let mut units = 0;
    let mut finished = false;
    loop {
        units += 1;
        let mut sand_position = Point(1, 500);
        loop {
            if sand_position.0 > 650 {
                finished = true;
                break;
            } else if field[sand_position.0 + 1][sand_position.1] == '.' {
                sand_position.0 += 1;
            } else if field[sand_position.0 + 1][sand_position.1 - 1] == '.' {
                sand_position.0 += 1;
                sand_position.1 -= 1;
            } else if field[sand_position.0 + 1][sand_position.1 + 1] == '.' {
                sand_position.0 += 1;
                sand_position.1 += 1;
            } else {
                field[sand_position.0][sand_position.1] = 'o';
                break;
            }
        }
        if finished {
            break;
        }
    }
    return units - 1;
}

fn simulate_with_floor(mut field: Vec<Vec<char>>, floor: usize) -> i32 {
    let mut units = 0;
    let mut finished = false;

    println!("Floor is at {}", floor);
    for i in 0..SIZE {
        field[floor][i] = '#';
    }

    loop {
        units += 1;
        let mut sand_position = Point(0, 500);

        loop {
            if field[sand_position.0][sand_position.1] == 'o' {
                finished = true;
                break;
            } else if field[sand_position.0 + 1][sand_position.1] == '.' {
                sand_position.0 += 1;
            } else if field[sand_position.0 + 1][sand_position.1 - 1] == '.' {
                sand_position.0 += 1;
                sand_position.1 -= 1;
            } else if field[sand_position.0 + 1][sand_position.1 + 1] == '.' {
                sand_position.0 += 1;
                sand_position.1 += 1;
            } else {
                field[sand_position.0][sand_position.1] = 'o';
                break;
            }
        }
        if finished {
            break;
        }
    }
    // for row in field.iter() {
    //     for elem in row {
    //         print!("{}", elem);
    //     }
    //     println!("");
    // }
    return units - 1;
}

fn get_floor(rocks: &Vec<Vec<Point>>) -> usize {
    let mut floor = rocks[0][0].0;
    for row in rocks.iter() {
        for point in row.iter() {
            if point.0 > floor {
                floor = point.0;
            }
        }
    }
    return floor + 2;
}

fn main() {
    let rocks = read_input("input.txt");
    let floor = get_floor(&rocks);
    let field = get_field(&rocks);

    let units = simulate(field.clone());
    println!(
        "Before sand has started falling into abyss, {} units of sand have passed",
        units
    );
    let units_with_floor = simulate_with_floor(field, floor);
    println!(
        "Before sand has blocked the opening the {} units of sand have passed",
        units_with_floor
    );
}
