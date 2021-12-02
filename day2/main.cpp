#include <fstream>
#include <iostream>

int PartOne() {
  std::ifstream input("input.txt");

  std::string direction;
  int num;
  int x{0};
  int y{0};
  while (input >> direction >> num) {
    if (direction == "forward") {
      x += num;
    } else if (direction == "down") {
      y += num;
    } else if (direction == "up") {
      y -= num;
    }
  }
  std::cout << "Final destination: (x, y) = "
            << "(" << x << ", " << y << ")" << std::endl;
  return x * y;
}

int PartTwo() {
  std::ifstream input("input.txt");

  std::string direction;
  int num;
  int x{0};
  int y{0};
  int aim{0};
  while (input >> direction >> num) {
    if (direction == "forward") {
      x += num;
      y += aim * num;
    } else if (direction == "down") {
      aim += num;
    } else if (direction == "up") {
      aim -= num;
    }
  }
  std::cout << "Final destination: (x, y) = "
            << "(" << x << ", " << y << ")" << std::endl;
  return x * y;
}

int main() {
  std::cout << "Puzzle 1: " << PartOne() << std::endl;
  std::cout << "Puzzle 2: " << PartTwo() << std::endl;

  return 0;
}