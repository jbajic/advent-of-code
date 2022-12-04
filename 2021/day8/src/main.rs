use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Hash, Eq, PartialEq, Debug)]
enum Segment {
    A,
    B,
    C,
    D,
    E,
    F,
    G,
}

fn find_digit_by_len(s: &str) -> i32 {
    match s.chars().count() {
        2 => return 1,
        3 => return 7,
        4 => return 4,
        7 => return 8,
        _ => return -1,
    }
}



fn string_to_segment(s: char) -> Segment {
    match s {
        'a' => Segment::A,
        'b' => Segment::B,
        'c' => Segment::C,
        'd' => Segment::D,
        'e' => Segment::E,
        'f' => Segment::F,
        'g' => Segment::G,
        _ => panic!("Whaaat?!?!?"),
    }
}

fn to_segments(s: &str) -> HashSet<Segment> {
    let mut seg = HashSet::new();
    for c in s.chars() {
        seg.insert(string_to_segment(c));
    }
    return seg;
}

fn segments_to_num(segments: &HashMap<i32, HashSet<Segment>>, segs: &HashSet<Segment>) -> i32 {
    for (num, seg_pack) in segments {
        if segs == seg_pack {
            return *num;
        }
    }
    return panic!("Segment not found: {:?}", segs);
}

fn puzzle1() -> i32 {
    let mut count = 0;
    if let Ok(lines) = read_lines("input.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(ip) = line {
                let output: Vec<&str> = ip.split(" | ").collect();
                for dig in output[1].split(" ") {
                    println!("Output is: {:?} and len is: {}", dig, dig.chars().count());
                    if find_digit_by_len(dig) != -1 {
                        count += 1;
                    }
                }
            }
        }
    }
    return count;
}

fn puzzle2() -> i32 {
    let mut values: Vec<i32> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        // Consumes the iterator, returns an (Optional) String
        for line in lines {
            if let Ok(ip) = line {
                let mut new_digits = HashMap::<i32, HashSet<Segment>>::new();
                let output: Vec<&str> = ip.split(" | ").collect();

                for dig in output[0].split(" ") {
                    let digit_by_len = find_digit_by_len(dig);
                    if digit_by_len != -1 && !new_digits.contains_key(&digit_by_len) {
                        let seg = to_segments(&dig);
                        new_digits.insert(digit_by_len, seg);
                    }
                    if new_digits.len() == 4 {
                        break;
                    }
                }
                if new_digits.len() == 4 {
                    println!("All unique have been found!");
                }

                for dig in output[0].split(" ") {
                    let digit_by_len = find_digit_by_len(dig);
                    if digit_by_len == -1 && !new_digits.contains_key(&digit_by_len) {
                        let seg = to_segments(&dig);
                        // it is 2, 3 or 5
                        if dig.len() == 5 {
                            //if it has all the segments as 1 its 3
                            if new_digits[&1].is_subset(&seg) {
                                new_digits.insert(3, seg);
                            } else if new_digits[&4].intersection(&seg).count() == 3 {
                                // if it share 3 elements with 4 then its 5
                                new_digits.insert(5, seg);
                            } else {
                                new_digits.insert(2, seg);
                            }
                        } else if dig.len() == 6 {
                            // it is 0, 6, 9
                            if !new_digits[&1].is_subset(&seg) {
                                new_digits.insert(6, seg);
                            } else if new_digits[&4].is_subset(&seg) {
                                new_digits.insert(9, seg);
                            } else {
                                new_digits.insert(0, seg);
                            }
                        }
                    }
                    if new_digits.len() == 10 {
                        break;
                    }
                }

                if new_digits.len() == 10 {
                    println!("All have been found!");
                }
                //decypher
                let mut val = 0;
                for (k, v) in &new_digits {
                    println!("Digit {} is {:?}", k, v);
                }
                for dig in output[1].split(" ") {
                    let segs = to_segments(dig);
                    let num = segments_to_num(&new_digits, &segs);
                    println!("The digits: {:?} are num {}", segs, num);
                    val = val * 10 + num;
                }
                println!("Value is {}", val);
                values.push(val);
            }
        }
    }
    let sum: i32 = values.iter().sum();
    return sum;
}

fn main() {
    let s1 = puzzle1();
    let s2 = puzzle2();
    println!("S1: {}", s1);
    println!("S2: {}", s2);
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
