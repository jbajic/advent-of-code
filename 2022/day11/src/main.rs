use indicatif::ProgressBar;
use num_bigint::{BigUint, ToBigUint};
use std::collections::HashMap;
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

#[derive(Copy, Clone, Debug)]
enum OperationType {
    ADD,
    SUB,
    MUL,
    DIV,
}

impl FromStr for OperationType {
    type Err = ();

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s {
            "+" => Ok(OperationType::ADD),
            "-" => Ok(OperationType::SUB),
            "*" => Ok(OperationType::MUL),
            "/" => Ok(OperationType::DIV),
            _ => Err(()),
        }
    }
}

#[derive(Debug)]
struct Operation {
    op: OperationType,
    num: Option<BigUint>,
}

impl Operation {
    fn do_operation(&self, old: &mut BigUint) {
        let num = match &self.num {
            Some(n) => n.clone(),
            None => old.clone(),
        };
        match self.op {
            OperationType::ADD => *old += num,
            OperationType::SUB => *old -= num,
            OperationType::MUL => *old *= num,
            OperationType::DIV => *old /= num,
        }
    }
}

#[derive(Debug)]
struct Test {
    div_num: BigUint,
    mon_true: usize,
    mon_false: usize,
}

fn reduce_num(mut num: BigUint) -> BigUint {
    let mut prime_factors = HashSet::new();
    let two = 2.to_biguint().unwrap();
    let zero = 0.to_biguint().unwrap();
    while &num % &two == zero {
        if !prime_factors.contains(&two) {
            prime_factors.insert(two.clone());
        }
        num /= &two;
    }
    for i in num_iter::range_inclusive(BigUint::from(3u32), num.sqrt()) {
        while &num % &i == zero {
            if !prime_factors.contains(&i) {
                prime_factors.insert(i.clone());
            }
            num /= &i;
        }
    }
    let mut common = 1.to_biguint().unwrap();
    if prime_factors.len() > 2 {
        for id in prime_factors {
            common *= id;
        }
        return common;
    }
    return num;
}

impl Test {
    fn do_test(&self, item: &BigUint) -> usize {
        if item % &self.div_num == 0.to_biguint().unwrap() {
            return self.mon_true as usize;
        }
        return self.mon_false as usize;
    }

    fn do_test_and_reduce(&self, item: &mut BigUint) -> usize {
        if &(*item) % &self.div_num == 0.to_biguint().unwrap() {
            return self.mon_true as usize;
        }
        return self.mon_false as usize;
    }
}

#[derive(Debug)]
struct Monkey {
    id: i32,
    starting_items: Vec<BigUint>,
    operation: Operation,
    test: Test,
}

fn read_monkeys() -> Vec<Vec<String>> {
    let mut monkeys_lines: Vec<Vec<String>> = Vec::new();
    let mut monkey_lines: Vec<String> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                if l == "" {
                    monkeys_lines.push(monkey_lines);
                    monkey_lines = Vec::new();
                } else {
                    monkey_lines.push(l);
                }
            }
        }
    }
    monkeys_lines.push(monkey_lines);
    return monkeys_lines;
}

fn get_id(line: &String) -> i32 {
    line.split(" ").collect::<Vec<&str>>()[1]
        .parse::<i32>()
        .unwrap()
}

fn get_starting_items(line: &String) -> Vec<BigUint> {
    let starting_items_line: Vec<_> = line
        .split(" ")
        .skip(4)
        .map(|item| {
            if item.ends_with(",") {
                return &item[0..item.len() - 1];
            }
            return item;
        })
        .collect();
    let mut starting_items: Vec<_> = Vec::new();
    for item in starting_items_line {
        starting_items.push(item.parse::<BigUint>().unwrap());
    }
    return starting_items;
}

fn get_operation(line: &String) -> Operation {
    let operation_line: Vec<_> = line.split(" ").collect();
    let op_type = OperationType::from_str(operation_line[operation_line.len() - 2]).unwrap();
    let value_result = operation_line[operation_line.len() - 1].parse::<BigUint>();
    let op_value = if let Ok(num) = value_result {
        Some(num)
    } else {
        None
    };
    return Operation {
        op: op_type,
        num: op_value,
    };
}

fn get_test(monkey_lines: &Vec<String>) -> Test {
    let test_condition = monkey_lines[3]
        .split(" ")
        .collect::<Vec<&str>>()
        .last()
        .unwrap()
        .parse::<BigUint>()
        .unwrap();
    println!("Test: {}", test_condition);
    let test_true = monkey_lines[4]
        .split(" ")
        .collect::<Vec<&str>>()
        .last()
        .unwrap()
        .parse::<usize>()
        .unwrap();
    let test_false = monkey_lines[5]
        .split(" ")
        .collect::<Vec<&str>>()
        .last()
        .unwrap()
        .parse::<usize>()
        .unwrap();
    return Test {
        div_num: test_condition,
        mon_true: test_true,
        mon_false: test_false,
    };
}

fn create_monkeys(mut monkeys_lines: Vec<Vec<String>>) -> Vec<Monkey> {
    let mut monkeys: Vec<Monkey> = Vec::new();
    for monkey_lines in monkeys_lines.iter_mut() {
        monkey_lines[0].pop();
        let id = get_id(&monkey_lines[0]);
        println!("Id: {}", id);

        let starting_items = get_starting_items(&monkey_lines[1]);
        println!("Starting items: {:?}", starting_items);

        let operation = get_operation(&monkey_lines[2]);
        println!("Operation: {:?}", operation);

        let test = get_test(&monkey_lines);
        println!("Test: {:?}", test);
        monkeys.push(Monkey {
            id: id,
            starting_items: starting_items,
            operation: operation,
            test: test,
        });
    }
    return monkeys;
}

fn simulate_1(mut monkeys: Vec<Monkey>, rounds: i32) {
    let mut inspection: HashMap<usize, BigUint> = HashMap::new();
    for i in 0..monkeys.len() {
        inspection.insert(i, BigUint::from(0u32));
    }
    let pb = ProgressBar::new(rounds as u64);
    let divisor = 3.to_biguint().unwrap();
    let mut common_divisor = 1.to_biguint().unwrap();
    for m in monkeys.iter() {
        common_divisor *= m.test.div_num.clone();
    }

    for round in 0..rounds {
        // println!("#####################");
        // println!("Simulation round P{}:", round + 1);
        // println!("#####################");
        for i in 0..monkeys.len() {
            let monkey_id = monkeys[i].id;
            // println!("Monkey {}", monkey_id);
            while !monkeys[i].starting_items.is_empty() {
                let mut item = monkeys[i].starting_items.remove(0);

                // Register inspection
                inspection
                    .entry(monkey_id as usize)
                    .and_modify(|elem| *elem += BigUint::from(1u32));
                // let old_level = item.clone();

                // Operation
                monkeys[i].operation.do_operation(&mut item);
                // println!("Worry level gets changed from {} to {}", old_level, item);

                // Drop interest
                item = item / divisor.clone();
                // println!("Worry level drops from {} to {}", old_level, item);

                // Throw item
                let monkey_to_throw = monkeys[i].test.do_test(&item);
                item = item % common_divisor.clone();
                // println!(
                //     "Reduced num {} is thrown to {} monkey.",
                //     item, monkey_to_throw
                // );
                monkeys[monkey_to_throw].starting_items.push(item);
            }
        }
        // break;
        pb.inc(1);
    }

    let mut business_levels: Vec<BigUint> = Vec::new();
    for (id, n) in inspection.iter() {
        business_levels.push(n.clone());
        println!("Monkey {} has inspected items {} times", id, n);
    }
    business_levels.sort_by(|a, b| b.cmp(a));
    println!(
        "Monkey business is {}",
        &business_levels[0] * &business_levels[1]
    );
}

fn simulate_2(mut monkeys: Vec<Monkey>, rounds: i32) {
    let mut inspection: HashMap<usize, BigUint> = HashMap::new();
    for i in 0..monkeys.len() {
        inspection.insert(i, BigUint::from(0u32));
    }
    let pb = ProgressBar::new(rounds as u64);
    let divisor = 3.to_biguint().unwrap();
    let mut common_divisor = 1.to_biguint().unwrap();
    for m in monkeys.iter() {
        common_divisor *= m.test.div_num.clone();
    }

    for round in 0..rounds {
        for i in 0..monkeys.len() {
            let monkey_id = monkeys[i].id;
            // println!("Monkey {}", monkey_id);
            while !monkeys[i].starting_items.is_empty() {
                let mut item = monkeys[i].starting_items.remove(0);

                // Register inspection
                inspection
                    .entry(monkey_id as usize)
                    .and_modify(|elem| *elem += BigUint::from(1u32));
                // let old_level = item.clone();

                // Operation
                monkeys[i].operation.do_operation(&mut item);

                // Throw item
                let monkey_to_throw = monkeys[i].test.do_test(&item);
                item = item % common_divisor.clone();

                monkeys[monkey_to_throw].starting_items.push(item);
            }
        }
        // break;
        pb.inc(1);
    }

    let mut business_levels: Vec<BigUint> = Vec::new();
    for (id, n) in inspection.iter() {
        business_levels.push(n.clone());
        println!("Monkey {} has inspected items {} times", id, n);
    }
    business_levels.sort_by(|a, b| b.cmp(a));
    println!(
        "Monkey business is {}",
        &business_levels[0] * &business_levels[1]
    );
}

fn main() {
    let monkeys_lines = read_monkeys();
    let monkeys1 = create_monkeys(monkeys_lines.clone());
    let monkeys2 = create_monkeys(monkeys_lines);

    simulate_1(monkeys1, 20);
    simulate_2(monkeys2, 10000);
}
