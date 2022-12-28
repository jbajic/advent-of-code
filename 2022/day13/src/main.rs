use std::cmp::{self, Ordering};
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Clone, Debug, Hash, PartialEq, Eq)]
enum Value {
    Int(i32),
    List(Vec<Value>),
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn read_input(input: &str) -> Vec<String> {
    let mut pair_lines: Vec<_> = Vec::new();
    if let Ok(lines) = read_lines(input) {
        for line in lines {
            if let Ok(l) = line {
                if l != "" {
                    pair_lines.push(l.to_string());
                }
            }
        }
    }
    return pair_lines;
}

fn transform_num(num: &str, index: &mut usize) -> Value {
    let mut val = Value::List(Vec::new());
    let chars = num.chars().collect::<Vec<char>>();
    while *index < num.len() - 1 {
        match chars[*index] {
            '[' => {
                *index += 1;
                match &mut val {
                    Value::List(list) => {
                        list.push(transform_num(&num, index));
                    }
                    _ => panic!("ladida"),
                }
            }
            ']' => {
                *index += 1;
                return val;
            }
            ',' => {
                *index += 1;
                continue;
            }
            _ => {
                let mut potential_num = String::new();
                for j in *index..chars.len() {
                    if chars[j] == ',' || chars[j] == ']' {
                        break;
                    }
                    potential_num.push(chars[j]);
                    *index += 1;
                }
                let num_val = potential_num.parse::<i32>().unwrap();
                match &mut val {
                    Value::List(list) => {
                        list.push(Value::Int(num_val));
                    }
                    _ => panic!("ladida"),
                }
            }
        }
    }
    return val;
}

#[derive(Debug, PartialEq)]
enum Result {
    True,
    False,
    Unknown,
}

fn compare_pair(num1: &Value, num2: &Value) -> Result {
    // println!("Comparing {:?} and {:?}", num1, num2);
    match (num1, num2) {
        (Value::Int(n1), Value::Int(n2)) => {
            if *n1 == *n2 {
                return Result::Unknown;
            } else if *n1 < *n2 {
                return Result::True;
            } else {
                return Result::False;
            }
        }
        (Value::List(l1), Value::List(l2)) => {
            for i in 0..cmp::min(l1.len(), l2.len()) {
                match compare_pair(&l1[i], &l2[i]) {
                    Result::True => return Result::True,
                    Result::False => return Result::False,
                    Result::Unknown => continue,
                };
            }
            // println!("Comparing lengths");
            if l1.len() < l2.len() {
                return Result::True;
            } else if l1.len() == l2.len() {
                return Result::Unknown;
            } else {
                return Result::False;
            }
        }
        (Value::Int(int), Value::List(_)) => {
            return compare_pair(&Value::List(vec![Value::Int(*int)]), &num2)
        }
        (Value::List(_), Value::Int(int)) => {
            return compare_pair(&num1, &Value::List(vec![Value::Int(*int)]))
        }
    }
}

impl Ord for Value {
    fn cmp(&self, other: &Self) -> Ordering {
        match compare_pair(self, other) {
            Result::True => Ordering::Less,
            Result::False => Ordering::Greater,
            Result::Unknown => Ordering::Equal,
        }
    }
}

impl PartialOrd for Value {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

fn compare_pairs(pair_lines: &Vec<String>) -> i32 {
    let mut sum = 0;
    let mut counter = 0;
    for pair in pair_lines.chunks(2) {
        counter += 1;
        let num1 = transform_num(&pair[0], &mut 1);
        let num2 = transform_num(&pair[1], &mut 1);
        if compare_pair(&num1, &num2) == Result::True {
            println!("Pair 1 {:?}", num1);
            println!("Pair 2 {:?}", num2);
            println!("Adding counter {}", counter);
            sum += counter;
        }
    }
    return sum;
}

fn get_product(pair_lines: Vec<String>) -> i32 {
    let mut pair_values = Vec::new();
    for pair in pair_lines.chunks(2) {
        let num1 = transform_num(&pair[0], &mut 1);
        let num2 = transform_num(&pair[1], &mut 1);
        pair_values.push(num1);
        pair_values.push(num2);
    }

    // Add indexing nums
    let n1 = Value::List(vec![Value::List(vec![Value::Int(2)])]);
    let n2 = Value::List(vec![Value::List(vec![Value::Int(6)])]);
    pair_values.push(Value::List(vec![Value::List(vec![Value::Int(2)])]));
    pair_values.push(Value::List(vec![Value::List(vec![Value::Int(6)])]));

    // Sort pair values
    pair_values.sort();
    let mut product = 1;
    for (i, num) in pair_values.iter().enumerate() {
        if num == &n1 {
            product *= (1+i);
        }
        if num == &n2 {
            product *= (1+i);
        }
    }
    return product as i32;
}

fn main() {
    let pair_lines = read_input("input.txt");
    let sum = compare_pairs(&pair_lines);
    let product = get_product(pair_lines);
    println!("Sum of correct pairs: {}", sum);
    println!("Product of given pairs is: {}", product);
}
