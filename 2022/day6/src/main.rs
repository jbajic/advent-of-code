use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::collections::HashSet;
use std::hash::Hash;

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn get_signal() ->String {
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                return l
            }
        }
    }
    panic!("Nothing read from file")
}

fn has_unique_elements<T>(iter: T) -> bool
where
    T: IntoIterator,
    T::Item: Eq + Hash,
{
    let mut uniq = HashSet::new();
    iter.into_iter().all(move |x| uniq.insert(x))
}

fn get_start_marker_position(string: &String, chars:usize) -> i32{
    let inter = string.chars().collect::<Vec<char>>();
    let mut count = chars as i32;
    for win in inter.windows(chars) {
        // println!("{:?}", win);
        if has_unique_elements(win.iter()) {
            break;
        }
        count += 1;
    }
    return count
}

fn main() {
    let line = get_signal();
    println!("Marker start for 4 consequent chars detected at {}", get_start_marker_position(&line, 4));
    println!("Marker start for 14 consequent chars detected at {}", get_start_marker_position(&line, 14));
}
