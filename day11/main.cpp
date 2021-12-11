#include <bits/types/FILE.h>
#include <cstddef>
#include <fstream>
#include <iostream>
#include <string>
#include <string_view>

template <int n> void FillArray(int arr[][n], std::string filename) {
  std::ifstream input(filename);
  std::string line;

  size_t i = 0;
  while (input >> line) {
    for (size_t j = 0; j < line.size(); j++) {
      arr[i][j] = stoi(std::string(1, line[j]));
    }
    i++;
  }
}
static int flashes = 0;
template <int n> void Flash(int arr[][n], int i, int j) {
  arr[i][j] = 0;
  flashes += 1;
  for (int dx = -1; dx < 2; dx++) {
    for (int dy = -1; dy < 2; dy++) {
      if (dx == 0 && dy == 0)
        continue;
      if (i + dx > -1 && i + dx < n && j + dy > -1 && j + dy < n) {
        if (arr[i + dx][j + dy] == 0)
          continue;
        arr[i + dx][j + dy] += 1;
      }
    }
  }
  for (int dx = -1; dx < 2; dx++) {
    for (int dy = -1; dy < 2; dy++) {
      if (i + dx > -1 && i + dx < n && j + dy > -1 && j + dy < n) {
        if (arr[i + dx][j + dy] > 9)
          Flash(arr, i + dx, j + dy);
      }
    }
  }
}

template <int n> void FlashStep(int arr[][n]) {
  // increase by one
  for (size_t i = 0; i < n; i++) {
    for (size_t j = 0; j < n; j++) {
      arr[i][j] += 1;
    }
  }
  for (size_t i = 0; i < n; i++) {
    for (size_t j = 0; j < n; j++) {
      if (arr[i][j] > 9 && arr[i][j] != 0) {
        Flash(arr, i, j);
      }
    }
  }
}

template <int n> bool AreInSync(int arr[][n]) {
  int num = arr[0][0];
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      if (arr[i][j] != num)
        return false;
    }
  }
  return true;
}

template <int n> void PrintOctos(int octos[][n]) {
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      std::cout << octos[i][j] << ", ";
    }
    std::cout << std::endl;
  }
  std::cout << std::endl;
}

void Puzzle1() {
  int octos[10][10];
  FillArray(octos, "input.txt");
  PrintOctos(octos);
  for (int i = 0; i < 100; i++) {
    FlashStep(octos);
  }
  PrintOctos(octos);
  std::cout << "Flashes: " << flashes << std::endl;
}

void Puzzle2() {
  int octos[10][10];
  FillArray(octos, "input.txt");
  int counter = 0;
  while (!AreInSync(octos)) {
    FlashStep(octos);
    counter++;
  }
  PrintOctos(octos);

  std::cout << "Are in sync after: " << counter << std::endl;
}

int main() {
  Puzzle1();
  Puzzle2();
  return 0;
}
