#include <algorithm>
#include <cmath>
#include <cstddef>
#include <fstream>
#include <iostream>
#include <iterator>
#include <numeric>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

auto GetPositions(const std::string &filename) {
  std::vector<int> positions;
  std::ifstream input(filename);
  std::string line;
  input >> line;

  std::stringstream ss(line);
  std::string intermediate;
  while (getline(ss, intermediate, ',')) {
    positions.push_back(stoi(intermediate));
  }

  return positions;
}

auto GetPuzzle2Cost(int n) {
  if (n == 0)
    return 0;
  return n + GetPuzzle2Cost(n - 1);
}

int Closest(std::vector<int> const &vec, int value) {
  auto const it = std::lower_bound(vec.begin(), vec.end(), value);
  if (it == vec.end()) {
    return -1;
  }

  return *it;
}

void Puuzzle2(std::vector<int> positions) {
  int min_cost = 100000000;
  for (int i = 0; i < positions.size(); i++) {
    int cost = 0;
    for (int j = 0; j < positions.size(); j++) {
      if (cost > min_cost)
        break;
      cost += GetPuzzle2Cost(std::abs(positions[j] - i));
    }
    if (cost < min_cost)
      min_cost = cost;
    std::cout << "Puzzle 2 cost: " << cost << " for elem: " << positions[i] << "\n";
  }
  std::cout << "Puzzle 2 min cost: " << min_cost << "\n";
}

void Puuzzle1(std::vector<int> positions) {
  std::sort(positions.begin(), positions.end());
  int med = positions[positions.size() / 2];

  //   std::cout << "Med: " << positions[positions.size() / 2];
  int cost = 0;
  for (const auto p : positions) {
    cost += std::abs(p - med);
  }
  std::cout << "Puzzle 1 cost: " << cost << "\n";
}

int main() {
  auto positions = GetPositions("input.txt");
  Puuzzle1(positions);
  Puuzzle2(positions);
  return 0;
}
