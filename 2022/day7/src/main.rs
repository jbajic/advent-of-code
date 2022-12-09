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

#[derive(Debug)]
struct Directory {
    name: String,
    subdirectories: Vec<Directory>,
    files: Vec<(String, i32)>,
    size: i32,
}

fn parse_directories() -> Vec<String> {
    let mut commands_lines: Vec<String> = Vec::new();

    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                commands_lines.push(l);
            }
        }
    }
    return commands_lines;
}

fn build_directory(lines: &Vec<String>, index: &mut usize, dir_name: String) -> Directory {
    let mut dir: Directory = Directory {
        name: dir_name,
        subdirectories: Vec::new(),
        files: Vec::new(),
        size: 0,
    };
    while *index < lines.len() {
        println!("Line {}", lines[*index]);
        let splitted: Vec<&str> = lines[*index].split(" ").collect();
        if splitted[0] == "$" {
            // is command
            match splitted[1] {
                "cd" => {
                    if splitted[2] == ".." {
                        return dir;
                    } else if splitted[2] == "/" {
                    } else {
                        *index += 1;
                        dir.subdirectories.push(build_directory(
                            &lines,
                            index,
                            String::from(splitted[2]),
                        ));
                    }
                }
                "ls" => {
                    *index = *index + 1;
                    continue;
                }
                _ => {
                    panic!("Command not found {}", lines[*index])
                }
            }
        } else if splitted[0] == "dir" {
            *index = *index + 1;
            continue;
        } else {
            let res = splitted[0].parse::<i32>();
            match res {
                Ok(size) => {
                    dir.files.push((String::from(splitted[1]), size));
                    dir.size += size;
                }
                Err(..) => panic!("Error happened in {}", lines[*index]),
            }
        }
        *index = *index + 1;
    }
    return dir;
}

fn sum_subdirs(root_dir: &mut Directory) -> i32 {
    for subdir in &mut root_dir.subdirectories {
        root_dir.size += sum_subdirs(subdir);
    }
    return root_dir.size;
}

fn find_sum(root_dir: &Directory) -> i32 {
    let mut dirs_sum = 0;
    for subdir in &root_dir.subdirectories {
        dirs_sum += find_sum(&subdir);
    }
    if root_dir.size <= 100000 {
        return dirs_sum + root_dir.size;
    }
    return dirs_sum;
}

fn find_smallest(root_dir: &Directory, mut current_smallest: i32, needed: i32) -> i32 {
    if root_dir.size > needed && root_dir.size < current_smallest {
        current_smallest = root_dir.size;
    }
    for subdir in &root_dir.subdirectories {
        current_smallest = find_smallest(subdir, current_smallest, needed);
    }
    return current_smallest;
}

fn main() {
    let mut directories = parse_directories();
    directories.remove(0);
    let mut index = 1usize;
    let mut root_dir = build_directory(&directories, &mut index, "/".to_string());
    sum_subdirs(&mut root_dir);

    let sum_of_all_dirs = find_sum(&root_dir);
    println!("Sum of all dirs under 100000 is: {}", sum_of_all_dirs);

    let unused_space = 70000000 - root_dir.size;
    let needed_space = 30000000 - unused_space;
    println!("Unused space {}, needed space {}", unused_space, needed_space);
    let current = root_dir.size;
    let smallest_dir_size = find_smallest(&root_dir, current, needed_space);
    println!("Smallest dir to delete is: {}", smallest_dir_size);
}
