use std::char;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn read_file(filename: &str) -> String {
    let mut string: String = "".to_string();
    if let Ok(lines) = read_lines(filename) {
        for line in lines {
            if let Ok(ip) = line {
                string = ip;
            }
        }
    }
    return string;
}

fn to_binary(c: char) -> &'static str {
    match c {
        '0' => "0000",
        '1' => "0001",
        '2' => "0010",
        '3' => "0011",
        '4' => "0100",
        '5' => "0101",
        '6' => "0110",
        '7' => "0111",
        '8' => "1000",
        '9' => "1001",
        'A' => "1010",
        'B' => "1011",
        'C' => "1100",
        'D' => "1101",
        'E' => "1110",
        'F' => "1111",
        _ => "",
    }
}

#[derive(Debug, Copy, Clone)]
struct PackageCounter<'a> {
    name: &'a str,
    value: usize,
}

#[derive(Debug, Clone)]
struct OperatorCounter<'a> {
    name: &'a str,
    value: usize,
    id: isize,
    nums: Vec<isize>,
}

fn decrease_package_counters(counters: &mut Vec<PackageCounter>, value: usize) {
    for counter in counters.iter_mut() {
        if counter.name == "subpackets_len" {
            counter.value = counter.value - value;
        }
    }
}

fn decrease_operator_counters(counters: &mut Vec<OperatorCounter>, value: usize) {
    for counter in counters.iter_mut() {
        if counter.name == "subpackets_len" {
            counter.value = counter.value - value;
        }
    }
}

fn get_operator_result(counter: &OperatorCounter) -> isize {
    match counter.id {
        0 => counter.nums.iter().sum(),
        1 => counter.nums.iter().fold(1,|a, &b| a * b),
        2 => *counter.nums.iter().min().unwrap(),
        3 => *counter.nums.iter().max().unwrap(),
        5 => {
            assert!(counter.nums.len() == 2, "num of subpackets is {}", counter.nums.len());
            if counter.nums[0] > counter.nums[1] {
                1
            } else {
                0
            }
        }
        6 => {
            assert!(counter.nums.len() == 2, "num of subpackets` is {}", counter.nums.len());
            if counter.nums[0] < counter.nums[1] {
                1
            } else {
                0
            }
        }
        7 => {
            assert!(counter.nums.len() == 2, "num of subpackets is {}", counter.nums.len());
            if counter.nums[0] == counter.nums[1] {
                1
            } else {
                0
            }
        }
        _ => 0,
    }
}

fn puzzle2(input: &String) {
    println!("Input: {}", input);
    let mut binary: String = "".to_string();
    for elem in input.chars() {
        binary.push_str(to_binary(elem));
    }
    println!("Input: {}, size: {}", binary, binary.chars().count());

    let mut version_sum = 0;
    let mut lastelem = 0;
    let mut sub = false;
    let mut counters = Vec::<OperatorCounter>::new();
    loop {
        if lastelem + 9 >= binary.chars().count() && sub && counters.len() == 0 {
            break;
        }
        let mut new_counter: Option<OperatorCounter> = None;

        let version = isize::from_str_radix(&binary[lastelem..lastelem + 3], 2).unwrap();
        lastelem = lastelem + 3;
        let packet_id = isize::from_str_radix(&binary[lastelem..lastelem + 3], 2).unwrap();
        lastelem = lastelem + 3;
        let mut decrease_count = 6;
        // decrease_operator_counters(&mut counters, 6);

        version_sum = version_sum + version;
        println!("Version: {}", version);
        println!("Id: {}", packet_id);
        if packet_id == 4 {
            // literal value
            let mut num = "".to_string();
            loop {
                num.push_str(&binary[lastelem + 1..lastelem + 5]);
                println!("Pushing {}", &binary[lastelem + 1..lastelem + 5]);
                decrease_count = decrease_count +5;
                if &binary[lastelem..lastelem + 1] == "0" {
                    lastelem = lastelem + 5;
                    break;
                }
                lastelem = lastelem + 5;
            }
            if !sub {
                let division = lastelem as f64 / 4.0;
                let leftover = division.ceil() as usize * 4 - lastelem;
                println!("Leftover {}", leftover);
                lastelem = lastelem + leftover;
            }
            let inum = isize::from_str_radix(&num, 2).unwrap();
            println!("Num {} is {}", num, inum);
            if counters.len() > 0 {
                counters.last_mut().map(|c| {
                    c.nums.push(inum);
                    c
                });
            }
        } else {
            //operator
            let mode = &binary[lastelem..lastelem + 1];
            lastelem = lastelem + 1;
            println!("Mode: {}", mode);
            sub = true;
            if &mode == &"0" {
                decrease_count = decrease_count + 16;
                let subpackets_len =
                    usize::from_str_radix(&binary[lastelem..lastelem + 15], 2).unwrap();
                lastelem = lastelem + 15;
                new_counter = Some(OperatorCounter {
                    id: packet_id,
                    name: "subpackets_len",
                    value: subpackets_len,
                    nums: Vec::<isize>::new(),
                });
            } else {
                let num_of_subpackets =
                    usize::from_str_radix(&binary[lastelem..lastelem + 11], 2).unwrap();
                lastelem = lastelem + 11;
                decrease_count = decrease_count + 12;
                new_counter = Some(OperatorCounter {
                    id: packet_id,
                    name: "num_of_subpackets",
                    value: num_of_subpackets,
                    nums: Vec::<isize>::new(),
                });
            }
            sub = true;
        }
        println!("AfterCounters: {:?}", counters);
        decrease_operator_counters(&mut counters, decrease_count);
        if counters.len() > 0 && counters.last().unwrap().name == "num_of_subpackets" {
            counters.last_mut().unwrap().value -= 1;
        }
        if new_counter.is_some() {
            counters.push(new_counter.unwrap());
        }
        if counters.len() > 0 {
            let mut index_counters = counters.len() - 1;
            let mut update_num: Option<isize> = None;
            loop {
                if counters[index_counters].value == 0 {
                    match update_num {
                        Some(num) => {
                            counters[index_counters].nums.push(num);
                            update_num = Some(get_operator_result(&counters[index_counters]));
                        }
                        None => {
                            update_num = Some(get_operator_result(&counters[index_counters]));
                        }
                    }
                    if counters.len() == 1 {
                        println!("Last operation: {:?}", get_operator_result(&counters[0]));
                    }
                    counters.pop();
                } else {
                    match update_num {
                        Some(num) => {
                            counters[index_counters].nums.push(num);
                            break;
                        }
                        None => {
                            break;
                        }
                    }
                }
                if index_counters == 0 {
                    break;
                }
                index_counters = index_counters - 1;
            }
        } else {
            panic!("No counters {}", lastelem);
        }
        println!("Counters: {:?}", counters);
        // if lastelem + 9 >= binary.chars().count() {
        //     println!("Last operator: {:?}", get_operator_result(&counters[0]));
        //     counters.pop();
        // }
        // counters.retain(|x| x.value > 0);
        // if counters.last().unwrap().value == 0 {
        //     counters.pop();
        // }
        println!("Last elem {}", lastelem);
        println!("----------");
    }
    println!("Total version sum {}!", version_sum);
}

fn puzzle1(input: &String) {
    println!("Input: {}", input);
    let mut binary: String = "".to_string();
    for elem in input.chars() {
        binary.push_str(to_binary(elem));
    }
    println!("Input: {}, size: {}", binary, binary.chars().count());

    let mut version_sum = 0;
    let mut lastelem = 0;
    let mut sub = false;
    let mut counters = Vec::<PackageCounter>::new();
    loop {
        if lastelem + 7 >= binary.chars().count() && sub && counters.len() == 0 {
            break;
        }
        let mut new_counter: Option<PackageCounter> = None;
        println!("Counters: {:?}", counters);

        let version = isize::from_str_radix(&binary[lastelem..lastelem + 3], 2).unwrap();
        lastelem = lastelem + 3;
        let packet_id = isize::from_str_radix(&binary[lastelem..lastelem + 3], 2).unwrap();
        lastelem = lastelem + 3;
        decrease_package_counters(&mut counters, 6);

        version_sum = version_sum + version;
        println!("Version: {}", version);
        println!("Id: {}", packet_id);
        if packet_id == 4 {
            // literal value
            let mut num = "".to_string();
            loop {
                num.push_str(&binary[lastelem + 1..lastelem + 5]);
                decrease_package_counters(&mut counters, 5);
                if &binary[lastelem..lastelem + 1] == "0" {
                    lastelem = lastelem + 5;
                    break;
                }
                lastelem = lastelem + 5;
            }
            if !sub {
                let division = lastelem as f64 / 4.0;
                let leftover = division.ceil() as usize * 4 - lastelem;
                println!("Leftover {}", leftover);
                lastelem = lastelem + leftover;
            }
            let inum = isize::from_str_radix(&num, 2).unwrap();
            println!("Num {} is {}", num, inum);
        } else {
            //operator
            let mode = &binary[lastelem..lastelem + 1];
            lastelem = lastelem + 1;
            println!("Mode: {}", mode);
            sub = true;
            if &mode == &"0" {
                decrease_package_counters(&mut counters, 16);
                let subpackets_len =
                    usize::from_str_radix(&binary[lastelem..lastelem + 15], 2).unwrap();
                lastelem = lastelem + 15;
                new_counter = Some(PackageCounter {
                    name: "subpackets_len",
                    value: subpackets_len,
                });
            } else {
                let num_of_subpackets =
                    usize::from_str_radix(&binary[lastelem..lastelem + 11], 2).unwrap();
                lastelem = lastelem + 11;
                decrease_package_counters(&mut counters, 12);
                new_counter = Some(PackageCounter {
                    name: "num_of_subpackets",
                    value: num_of_subpackets,
                });
            }
            sub = true;
        }

        for counter in counters.iter_mut() {
            if counter.name == "num_of_subpackets" {
                counter.value = counter.value - 1;
            }
        }
        if new_counter.is_some() {
            counters.push(new_counter.unwrap());
        }
        counters.retain(|&x| x.value > 0);
        println!("Last elem {}", lastelem);
        println!("----------");
    }
    println!("Total version sum {}!", version_sum);
}

fn main() {
    println!("Hello, world!");
    let input = read_file("input.txt");
    // puzzle1(&input);
    puzzle2(&input);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
