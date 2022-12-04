use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

#[derive(Debug, Clone, Copy)]
enum Hand {
    ROCK,
    PAPER,
    SCISSORS,
}

#[derive(Debug, Clone, Copy)]
enum Result {
    LOSE,
    WIN,
    DRAW,
}

fn get_result(result: char) -> Result {
    match result {
        'X' => Result::LOSE,
        'Y' => Result::DRAW,
        'Z' => Result::WIN,
        _ => {
            panic!("Something unexpected happened")
        }
    }
}

fn get_hand(hand: char) -> Hand {
    match hand {
        'A' | 'X' => Hand::ROCK,
        'B' | 'Y' => Hand::PAPER,
        'C' | 'Z' => Hand::SCISSORS,
        _ => {
            panic!("Something unexpected happened")
        }
    }
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

// A, Y is rock worth 1 point
// B, X is paper worth 2 point
// C, Z is scissors worth 3 point
fn shape_score(shape: Hand) -> i32 {
    match shape {
        Hand::ROCK => 1,
        Hand::PAPER => 2,
        Hand::SCISSORS => 3,
    }
}

fn result_score(player: Hand, opponent: Hand) -> i32 {
    match player {
        Hand::ROCK => match opponent {
            Hand::ROCK => 3,
            Hand::PAPER => 0,
            Hand::SCISSORS => 6,
        },
        Hand::PAPER => match opponent {
            Hand::ROCK => 6,
            Hand::PAPER => 3,
            Hand::SCISSORS => 0,
        },
        Hand::SCISSORS => match opponent {
            Hand::ROCK => 0,
            Hand::PAPER => 6,
            Hand::SCISSORS => 3,
        },
    }
}

fn get_player_move(result: Result, opponent: Hand) -> Hand {
    match result {
        Result::LOSE => match opponent {
            Hand::ROCK => Hand::SCISSORS,
            Hand::PAPER => Hand::ROCK,
            Hand::SCISSORS => Hand::PAPER,
        },
        Result::WIN => match opponent {
            Hand::ROCK => Hand::PAPER,
            Hand::PAPER => Hand::SCISSORS,
            Hand::SCISSORS => Hand::ROCK,
        },
        Result::DRAW => opponent
    }
}

fn calculate_score_1(vec: &Vec<(char,char)>) -> i32 {
    let mut score = 0;
    for elem in vec.iter() {
        score += shape_score(get_hand(elem.1)) + result_score(get_hand(elem.1), get_hand(elem.0));
    }
    return score;
}

fn calculate_score_2(vec: &Vec<(char, char)>) -> i32 {
    let mut score = 0;
    for elem in vec.iter() {
        let res = get_result(elem.1);
        let opponent_hand = get_hand(elem.0);
        let player_move = get_player_move(res, opponent_hand);
        score += shape_score(player_move) + result_score(player_move, opponent_hand);
    }
    return score;
}

fn main() {
    let mut vec: Vec<(char, char)> = Vec::new();
    if let Ok(lines) = read_lines("input.txt") {
        for line in lines {
            if let Ok(line) = line {
                let splitted: Vec<&str> = line.split_whitespace().collect();
                assert!(splitted.len() == 2);
                vec.push((
                    splitted[0].chars().take(1).last().unwrap(),
                    splitted[1].chars().take(1).last().unwrap(),
                ));
            }
        }
    }
    println!("First task score is: {}", calculate_score_1(&vec));
    println!("Second task score is: {}", calculate_score_2(&vec));
}
