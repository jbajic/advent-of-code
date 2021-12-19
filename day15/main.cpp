#include <algorithm>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <string>
#include <tuple>
#include <unordered_map>
#include <vector>

template <int n>
void ReadCaves(int arr[n][n], std::string filename, int times = 1) {
  std::ifstream file(filename);
  std::string line;

  size_t i = 0;
  while (file >> line) {
    for (size_t j = 0; j < line.size(); j++) {
      int value = stoi(std::string(1, line[j]));
      arr[i][j] = value;
    }
    i++;
  }
  if (times > 1) {
    int size = n / times;
    for (int i = 0; i < n; i++) {
      for (int j = 0; j < n; j++) {
        if (i >= size && j >= size) {
          arr[i][j] = arr[i - size][j - size] + 1;
        } else if (i >= size) {
          arr[i][j] = arr[i - size][j] + 1;
        }
        if (j >= size) {
          arr[i][j] = arr[i][j - size] + 1;
        }
        if (arr[i][j] > 9) {
          arr[i][j] = 1;
        }
      }
    }
  }
}

struct pair_hash {
  template <typename T, typename K>
  std::size_t operator()(const std::pair<T, K> &pair) const {
    return std::hash<T>()(pair.first) ^ std::hash<K>()(pair.second);
  }
};

template <int n> int AStarSearch(const int caves[n][n]) {
  using point = std::tuple<int, int, int>;

  int movement[4][2]{{1, 0}, {0, 1}, {-1, 0}, {0, -1}};
  auto heuristic([](const int x, const int y) { return n - x + n - y; });
  auto cmp = [](const point lhs, const point rhs) {
    return std::get<2>(lhs) > std::get<2>(rhs);
  };
  int scores[n][n];
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      scores[i][j] = std::numeric_limits<int>::max();
    }
  }
  scores[0][0] = caves[0][0];

  std::priority_queue<point, std::vector<point>, decltype(cmp)> queue;
  std::unordered_map<std::pair<int, int>, std::pair<int, int>, pair_hash>
      came_from;
  queue.push({1, 0, heuristic(1, 0)});
  scores[1][0] = caves[1][0];
  came_from[{1, 0}] = {0, 0};
  queue.push({0, 1, heuristic(0, 1)});
  scores[0][1] = caves[0][1];
  ;
  came_from[{0, 1}] = {0, 0};
  std::vector<std::tuple<int, int>> visited;

  while (!queue.empty()) {
    auto current = queue.top();
    queue.pop();
    visited.emplace_back(std::get<0>(current), std::get<1>(current));

    if (std::get<0>(current) == n - 1 && std::get<1>(current) == n - 1) {
      std::cout << "Found path: " << std::endl;
      int cost = 0;
      std::pair<int, int> elem = {std::get<0>(current), std::get<1>(current)};
      while (came_from.contains(elem)) {
        std::cout << elem.first << ", " << elem.second << ": "
                  << caves[elem.first][elem.second] << std::endl;
        cost += caves[elem.first][elem.second];
        elem = came_from[{elem.first, elem.second}];
      }
      return cost;
    }
    for (const auto &move : movement) {
      const auto new_x = move[0] + std::get<0>(current);
      const auto new_y = move[1] + std::get<1>(current);
      const bool is_visited =
          std::find_if(
              visited.begin(), visited.end(), [new_x, new_y](const auto elem) {
                return std::get<0>(elem) == new_x && std::get<1>(elem) == new_y;
              }) != visited.end();
      if (new_x > -1 && new_x < n && new_y > -1 && new_y < n && !is_visited) {
        const int new_score =
            scores[std::get<0>(current)][std::get<1>(current)] +
            caves[new_x][new_y];
        if (new_score < scores[new_x][new_y]) {
          came_from[{new_x, new_y}] = {std::get<0>(current),
                                       std::get<1>(current)};
          scores[new_x][new_y] = new_score;
          queue.push({new_x, new_y, new_score + heuristic(new_x, new_y)});
        }
      }
    }
  }

  return 0;
}

template <int n> void PrintCaves(const int caves[n][n]) {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      std::cout << caves[i][j] << " ";
    }
    std::cout << std::endl;
  }
}

void Puzzle1() {
  int caves[100][100];
  ReadCaves(caves, "input.txt");
  PrintCaves(caves);
  int cost = AStarSearch(caves);
  std::cout << "Cost: " << cost << std::endl;
}

void Puzzle2() {
  int caves[500][500];
  ReadCaves(caves, "input.txt", 5);
  PrintCaves(caves);
  int cost = AStarSearch(caves);
  std::cout << "Cost: " << cost << std::endl;
}

int main() {
  Puzzle2();
  return 0;
}