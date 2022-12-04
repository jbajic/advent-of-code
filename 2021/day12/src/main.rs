use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;

fn read_graph(filename: &str) -> HashMap<String, HashSet<String>> {
    let mut graph: HashMap<String, HashSet<String>> = HashMap::new();
    if let Ok(lines) = read_lines(filename) {
        for line in lines {
            if let Ok(ip) = line {
                let rel: Vec<&str> = ip.split("-").collect();
                let from = rel[0].to_string();
                let to = rel[1].to_string();
                if graph.contains_key(&from) {
                    graph.get_mut(&from).unwrap().insert(to.clone());
                } else {
                    graph.insert(from.clone(), HashSet::from([to.clone()]));
                }

                if graph.contains_key(&to) {
                    graph.get_mut(&to).unwrap().insert(from);
                } else {
                    graph.insert(to, HashSet::from([from.clone()]));
                }
            }
        }
    }
    return graph;
}

fn path_counter(
    from: &str,
    to: &str,
    path_count: &mut i32,
    visited: &mut HashSet<String>,
    graph: &HashMap<String, HashSet<String>>,
) {
    if !from.to_string().chars().next().unwrap().is_uppercase() {
        visited.insert(from.to_string());
    }
    if from == to {
        *path_count += 1;
    } else {
        if graph.contains_key(from) {
            println!("VIsitor {}", from);
            println!("Visiting {:?}", &graph[from]);
            println!("Visited {:?}", visited);
            for new_node in &graph[from] {
                if !visited.contains(new_node) {
                    path_counter(&new_node, to, path_count, visited, graph);
                }
            }
        }
    }
    visited.remove(from);
}

fn puzzle1(graph: &HashMap<String, HashSet<String>>) {
    let mut visited: HashSet<String> = HashSet::new();
    let mut path_count: i32 = 0;
    path_counter("start", "end", &mut path_count, &mut visited, graph);
    println!("The path count is: {}", path_count);
}

fn puzzle2(graph: &HashMap<String, HashSet<String>>) {
    let mut path_count: i32 = 0;
    let start = ("start".to_string(), HashSet::from(["start".to_string()]), "".to_string());
    let mut stack = vec![start];
    while !stack.is_empty() {
        let (current, visited, double) = stack.pop().unwrap();
        if &current == "end" {
            path_count += 1;
            continue;
        }
        for new_node in &graph[&current] {
            if !visited.contains(new_node) {
                let mut new_visited = visited.clone();
                if new_node.chars().next().unwrap().is_lowercase() {
                    new_visited.insert(new_node.to_string());
                }
                stack.push((new_node.clone(), new_visited, double.clone()));
            } else if double == ""
                && new_node != "start"
                && new_node != "end"
                && new_node.chars().next().unwrap().is_lowercase()
            {
                stack.push((new_node.clone(), visited.clone(), new_node.clone()));
            }
        }
    }
    println!("The path count is: {:?}", path_count);
}

fn main() {
    let graph = read_graph("input.txt");
    // for (key, values) in &graph {
    //     println!("{} -> {:?}", key, values);
    // }
    // puzzle1(&graph);
    puzzle2(&graph);
}

fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where
    P: AsRef<Path>,
{
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}
