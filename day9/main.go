package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// An IntHeap is a min-heap of ints.
type IntHeap []int

func (h IntHeap) Len() int           { return len(h) }
func (h IntHeap) Less(i, j int) bool { return h[i] < h[j] }
func (h IntHeap) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *IntHeap) Push(x interface{}) {
	// Push and Pop use pointer receivers because they modify the slice's length,
	// not just its contents.
	*h = append(*h, x.(int))
}

func (h *IntHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func ReadCaves(filename string) [][]int {
	file, err := os.Open(filename)
	if err != nil {
		panic("error opening file")
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var caves [][]int
	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		var row []int
		for _, c := range line {
			character := string(c)
			num, err := strconv.Atoi(character)
			if err != nil {
				panic(fmt.Sprintf("not a num in row %v\n", line))
			}
			row = append(row, num)
		}
		caves = append(caves, row)
	}
	return caves
}

func IsSmallestInRange(caves *[][]int, i, j int) bool {
	if i > 0 && (*caves)[i-1][j] <= (*caves)[i][j] {
		return false
	}
	if j > 0 && (*caves)[i][j-1] <= (*caves)[i][j] {
		return false
	}
	if i < len(*caves)-1 && (*caves)[i+1][j] <= (*caves)[i][j] {
		return false
	}
	if j < len((*caves)[0])-1 && (*caves)[i][j+1] <= (*caves)[i][j] {
		return false
	}
	return true
}

type Point struct {
	x, y int
}

func GetBasinSize(caves *[][]int, iii, jjj int) int {
	size := 0
	queue := make([]Point, 0)
	queue = append(queue, Point{iii, jjj})
	visited := map[Point]bool{}

	// fmt.Print("Starting\n")
	for len(queue) > 0 {
		point := queue[0]
		queue = queue[1:]
		is_visited := !visited[point]
		if !is_visited {
			continue
		} else {
			visited[point] = true
		}
		// fmt.Printf("Point: %v %v value: %v\n", point.x, point.y, (*caves)[point.x][point.y])
		if point.x > 0 && (*caves)[point.x-1][point.y] > (*caves)[point.x][point.y] {
			new_point := Point{point.x - 1, point.y}
			exists := visited[new_point]
			if !exists && (*caves)[new_point.x][new_point.y] != 9 {
				queue = append(queue, new_point)
			}
		}
		if point.y > 0 && (*caves)[point.x][point.y-1] > (*caves)[point.x][point.y] {
			new_point := Point{point.x, point.y - 1}
			exists := visited[new_point]
			if !exists && (*caves)[new_point.x][new_point.y] != 9 {
				queue = append(queue, new_point)
			}
		}
		if point.x < len(*caves)-1 && (*caves)[point.x+1][point.y] > (*caves)[point.x][point.y] {
			new_point := Point{point.x + 1, point.y}
			exists := visited[new_point]
			if !exists && (*caves)[new_point.x][new_point.y] != 9 {
				queue = append(queue, new_point)
			}
		}
		if point.y < len((*caves)[0])-1 && (*caves)[point.x][point.y+1] > (*caves)[point.x][point.y] {
			new_point := Point{point.x, point.y + 1}
			exists := visited[new_point]
			if !exists && (*caves)[new_point.x][new_point.y] != 9 {
				queue = append(queue, new_point)
			}
		}
		size += 1
	}
	return size
}

func Puzzle1() {
	var caves = ReadCaves("input.txt")
	var sum = 0

	for i, row := range caves {
		for j := range row {
			if IsSmallestInRange(&caves, i, j) {
				sum += caves[i][j] + 1
			}
		}
	}
	fmt.Printf("sum is: %v\n", sum)
}

func Puzzle2() {
	var caves = ReadCaves("input.txt")
	var top = make([]int, 3)
	for i, row := range caves {
		for j, height := range row {
			if height == 9 {
				continue
			}
			var bs = GetBasinSize(&caves, i, j)
			// fmt.Printf("BS: %v\n", bs)
			inx, val := -1, -1
			for i, score := range top {
				if bs > score && val == -1 {
					inx, val = i, score
				} else if bs > score && val > score {
					inx, val = i, score
				}
			}
			if val > -1 {
				top[inx] = bs
			}
		}
	}
	var sum = 1
	for i, s := range top {
		sum *= s
		fmt.Printf("%v. score is: %v\n", i+1, s)
	}
	fmt.Printf("sum is: %v\n", sum)
}

func main() {
	Puzzle1()
	Puzzle2()
}
