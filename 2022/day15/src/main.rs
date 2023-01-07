use std::collections::HashMap;
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

#[derive(Debug, PartialEq)]
struct Point(i32, i32);

#[derive(Debug)]
struct SensorBeacon {
    sensor: Point,
    beacon: Point,
    range: i32,
}

fn get_sensor_position(sensor_line: &str) -> Point {
    // Sensor at x=2, y=18:
    let prefix_remove = sensor_line.strip_prefix("Sensor at ").unwrap();
    let coords = prefix_remove.split(", ").collect::<Vec<&str>>();
    let x = coords[0].split("x=").collect::<Vec<&str>>()[1]
        .parse::<i32>()
        .unwrap();
    let y = coords[1].split("y=").collect::<Vec<&str>>()[1]
        .parse::<i32>()
        .unwrap();
    return Point(x, y);
}

fn get_beacon_position(beacon_line: &str) -> Point {
    // closest beacon is at x=-2, y=15
    let prefix_remove = beacon_line.strip_prefix("closest beacon is at").unwrap();
    let coords = prefix_remove.split(", ").collect::<Vec<&str>>();
    let x = coords[0].split("x=").collect::<Vec<&str>>()[1]
        .parse::<i32>()
        .unwrap();
    let y = coords[1].split("y=").collect::<Vec<&str>>()[1]
        .parse::<i32>()
        .unwrap();

    return Point(x, y);
}

fn read_input(input: &str) -> Vec<SensorBeacon> {
    let mut sensors_and_beacons = Vec::new();
    if let Ok(lines) = read_lines(input) {
        for line in lines {
            if let Ok(l) = line {
                let splitted = l.split(": ").collect::<Vec<&str>>();
                let sensor = get_sensor_position(splitted[0]);
                let beacon = get_beacon_position(splitted[1]);
                let dist = manhattan_distance(&sensor, &beacon);

                sensors_and_beacons.push(SensorBeacon {
                    sensor: sensor,
                    beacon: beacon,
                    range: dist,
                });
            }
        }
    }
    return sensors_and_beacons;
}

fn manhattan_distance(a: &Point, b: &Point) -> i32 {
    (b.0 - a.0).abs() + (b.1 - a.1).abs()
}

fn is_position_covered(position: &Point, sensor_beacon: &SensorBeacon) -> bool {
    manhattan_distance(&sensor_beacon.sensor, &position) <= sensor_beacon.range
}

fn is_beacon(position: &Point, sensor_beacon: &SensorBeacon) -> bool {
    *position == sensor_beacon.beacon
}

fn get_min_max_x(sensor_beacon_points: &Vec<SensorBeacon>) -> (i32, i32) {
    let mut min_x = sensor_beacon_points[0].sensor.0;
    let mut max_x = sensor_beacon_points[0].sensor.0;
    for sensor_beacon_pair in sensor_beacon_points.iter() {
        //sensor
        if sensor_beacon_pair.sensor.0 > max_x {
            max_x = sensor_beacon_pair.sensor.0 + sensor_beacon_pair.range;
        }
        if sensor_beacon_pair.sensor.0 < min_x {
            min_x = sensor_beacon_pair.sensor.0 - sensor_beacon_pair.range;
        }
    }

    return (min_x, max_x);
}

fn get_covered_positions_in_row(sensor_beacon_points: &Vec<SensorBeacon>, row: i32) -> i32 {
    let (min_x, max_x) = get_min_max_x(&sensor_beacon_points);

    let mut covered_positions = 0;
    for i in min_x..max_x {
        let mut covered = false;
        for sensor_beacon_point in sensor_beacon_points.iter() {
            let position = Point(i, row);
            if !is_beacon(&position, sensor_beacon_point)
                && is_position_covered(&position, sensor_beacon_point)
            {
                covered = true;
                break;
            }
        }
        if covered {
            covered_positions += 1;
        }
    }
    return covered_positions;
}

fn get_tuning_frequency(sensor_beacons: &Vec<SensorBeacon>, start: i32, end: i32) -> i64 {
    let mut lines = HashMap::new();
    for sensor_beacon in sensor_beacons {
        let top_asc = (
            true,
            sensor_beacon.sensor.1 - sensor_beacon.range - 1 - sensor_beacon.sensor.0,
        );
        let top_desc = (
            false,
            sensor_beacon.sensor.1 - sensor_beacon.range - 1 + sensor_beacon.sensor.0,
        );

        let bottom_asc = (
            true,
            sensor_beacon.sensor.1 + sensor_beacon.range + 1 - sensor_beacon.sensor.0,
        );

        let bottom_desc = (
            false,
            sensor_beacon.sensor.1 + sensor_beacon.range + 1 + sensor_beacon.sensor.0,
        );

        for line in [top_asc, top_desc, bottom_asc, bottom_desc] {
            if lines.contains_key(&line) {
                lines.entry(line).and_modify(|val| *val += 1);
            } else {
                lines.insert(line, 1);
            }
        }
    }

    let mut asc_lines = Vec::new();
    let mut desc_lines = Vec::new();

    for (line, count) in lines.iter() {
        if count > &1 {
            if line.0 {
                desc_lines.push(line.1)
            } else {
                asc_lines.push(line.1)
            }
        }
    }

    let mut points = Vec::new();
    for rising_q in asc_lines.iter() {
        for descending_q in desc_lines.iter() {
            // calculate the intersections between all the rising and descending lines
            let x = (rising_q - descending_q) / 2;
            let y = x + descending_q;
            points.push(Point(x, y));
        }
    }
    for point in points.iter() {
        // Check which of the intersections is the free point
        if (start <= point.1 && point.1 <= end)
            && (start <= point.0 && point.0 <= end)
            && sensor_beacons
                .iter()
                .all(|sensor_beacon| !is_position_covered(point, sensor_beacon))
        {
            return point.0 as i64 * 4000000i64 + point.1 as i64;
        }
    }
    panic!("No solution found!");
}

fn main() {
    let sensor_beacon_points = read_input("input.txt");
    // let covered_positions_in_row = get_covered_positions_in_row(&sensor_beacon_points, 2000000);
    // println!(
    //     "Positions in row 2000000 that cannot contain beacon {}",
    //     covered_positions_in_row
    // );

    let tuning_freq = get_tuning_frequency(&sensor_beacon_points, 0, 4000000);
    println!(
        "Tuning frequency for distress beacon signal is {}",
        tuning_freq
    );
}
