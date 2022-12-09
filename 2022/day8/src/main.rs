use std::collections::HashSet;
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

fn read_data() -> Vec<Vec<usize>> {
    let mut forest: Vec<Vec<usize>> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(l) = line {
                let mut tree_line: Vec<usize> = Vec::new();
                l.chars().for_each(|c| {
                    tree_line.push(c.to_digit(10).unwrap().try_into().unwrap());
                });
                forest.push(tree_line);
            }
        }
    }
    return forest;
}

fn get_visible_trees(forest: &Vec<Vec<usize>>) -> HashSet<(usize, usize)> {
    let mut seen: HashSet<(usize, usize)> = HashSet::new();
    for i in 0..forest.len() {
        seen.insert((i, forest[0].len() - 1));
        seen.insert((i, 0));
    }
    for i in 0..forest[0].len() {
        seen.insert((forest[0].len() - 1, i));
        seen.insert((0, i));
    }
    // top to bottom
    for i in 1..forest[0].len() - 1 {
        let mut max_tree = forest[0][i];
        for j in 1..forest.len() - 1 {
            let curr = forest[j][i];
            // let prev = forest[j - 1][i];
            if curr > max_tree {
                seen.insert((j, i));
                max_tree = curr;
            } else {
                continue;
            }
        }
    }
    // bottom to top
    for i in 1..forest[0].len() - 1 {
        let mut max_tree = forest[forest.len() - 1][i];
        for j in (1..forest.len() - 1).rev() {
            let curr = forest[j][i];
            // let prev = forest[j + 1][i];
            // print!("{} > {}, ", curr, prev);
            // print!("({}, {}), ", j, i);
            if curr > max_tree {
                seen.insert((j, i));
                max_tree = curr;
            } else {
                continue;
            }
        }
    }
    //  left to right
    for i in 1..forest.len() - 1 {
        let mut max_tree = forest[i][0];
        for j in 1..forest[i].len() - 1 {
            let curr = forest[i][j];
            // let prev = forest[i][j - 1];
            if curr > max_tree {
                seen.insert((i, j));
                max_tree = curr;
            } else {
                continue;
            }
        }
    }
    // right to left
    for i in 1..forest.len() - 1 {
        let mut max_tree = forest[i][forest[i].len() - 1];
        for j in (1..forest[i].len() - 1).rev() {
            let curr = forest[i][j];
            if curr > max_tree {
                seen.insert((i, j));
                max_tree = curr;
            } else {
                continue;
            }
        }
    }
    return seen;
}

fn get_score(forest: &Vec<Vec<usize>>, index_i: usize, index_j: usize) -> usize {
    // top to bottom
    let mut score_up = 0;
    let watched = forest[index_i][index_j];
    // println!("Top to bottom");
    for i in index_i + 1..forest.len() {
        let curr = forest[i][index_j];
        // println!("({}, {}) = {}", i, index_j, curr);
        score_up += 1;
        if curr >= watched {
            break;
        }
    }

    // bottom to top
    let mut score_down = 0;
    // println!("Bottom to top");
    for i in (0..index_i).rev() {
        let curr = forest[i][index_j];
        // println!("({}, {}) = {}", i, index_j, curr);
        score_down += 1;
        if curr >= watched {
            break;
        }
    }

    // left to right
    let mut score_right = 0;
    // println!("Left to right");
    for j in index_j + 1..forest[0].len() {
        let curr = forest[index_i][j];
        // println!("({}, {}) = {}", index_i, j, curr);
        score_right += 1;
        if curr >= watched {
            break;
        }
    }

    // // right to left
    let mut score_left = 0;
    // println!("Left to right");
    for j in (0..index_j).rev() {
        let curr = forest[index_i][j];
        // println!("({}, {}) = {}", index_i, j, curr);
        score_left += 1;
        if curr >= watched {
            break;
        }
    }

    // println!("{} {} {} {}", score_up, score_down, score_left, score_right);
    return score_up * score_down * score_left * score_right;
}

fn get_highest_scenic_score(forest: &Vec<Vec<usize>>) -> usize {
    let mut score: usize = 0;
    for i in 0..forest.len() {
        for j in 0..forest[i].len() {
            score = std::cmp::max(score, get_score(forest, i, j));
        }
    }
    return score;
}

fn main() {
    let forest = read_data();

    let visible = get_visible_trees(&forest);
    println!("Number of visible trees are {}", visible.len());
    get_score(&forest, 1, 2);
    println!(
        "Highest scenic score is {}",
        get_highest_scenic_score(&forest)
    );
}
