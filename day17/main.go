package main

import (
	"bufio"
	"container/heap"
	"errors"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Surface struct {
	x_start, x_end int
	y_start, y_end int
}

type Throw struct {
	dx, dy int
	height int
	index  int
}

type PriorityQueue []*Throw

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].height > pq[j].height
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	throw := x.(*Throw)
	throw.index = n
	*pq = append(*pq, throw)
}

func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	throw := old[n-1]
	old[n-1] = nil   //avoid memory leaks
	throw.index = -1 // for safety
	*pq = old[0 : n-1]
	return throw
}

func decodeCoordinate(str_part *string) (int, int) {
	values := strings.Split(*str_part, "..")
	start, err := strconv.Atoi(values[0])
	if err != nil {
		panic(fmt.Sprintf("err occurred with start part of coordinate: %v", err))
	}
	end, err := strconv.Atoi(values[1])
	if err != nil {
		panic(fmt.Sprintf("err occurred with end part of coordinate: %v", err))
	}
	return start, end
}

func ReadInput(filename string) Surface {
	file, err := os.Open(filename)
	if err != nil {
		panic("file could not be opened")
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	scanner.Scan()
	line := strings.TrimSpace(scanner.Text())
	values := strings.Split(line, "target area: ")
	x_values_str := strings.Split(strings.Split(values[1], ",")[0], "=")[1]
	y_values_str := strings.Split(strings.Split(values[1], ",")[1], "=")[1]

	x_start, x_end := decodeCoordinate(&x_values_str)
	y_start, y_end := decodeCoordinate(&y_values_str)

	fmt.Printf("x: %v .. %v\n", x_start, x_end)
	fmt.Printf("y: %v .. %v\n", y_start, y_end)
	return Surface{x_start, x_end, y_start, y_end}
}

func SimulateThrow(dx, dy int, surface *Surface) (int, int, int, error) {
	x, y := 0, 0
	max_height := 0
	for {
		// this must happen
		// stop condition when touch the surface or pass it
		// success condition
		if y > max_height {
			max_height = y
		}
		if x >= surface.x_start && x <= surface.x_end && y >= surface.y_start && y <= surface.y_end {
			return x, y, max_height, nil
		} else if x > surface.x_end || y < surface.y_start {
			// fail condition
			return x, y, max_height, errors.New("no result")
		}
		fmt.Printf("coordinate is %v %v\n", x, y)
		//update x, y
		x += dx
		y += dy
		//update dx, dy
		if dx == 0 {
			dx = 0
		} else {
			dx -= 1
		}
		dy -= 1
	}
}

func GetVelocity(x int) int {
	dist_x := 0
	dx := 0
	for {
		dx += 1
		dist_x = dist_x + dx
		if dist_x >= x {
			return dx - 1
		}
	}
}

func Puzzle1(surface *Surface) {
	// initialize queue
	throws := make(PriorityQueue, 0)
	heap.Init(&throws)

	//calculate minimum and maximum velocity to reach surface
	min_dx, max_dx := GetVelocity(surface.x_start), surface.x_end
	fmt.Printf("min velocity:  %v max vel: %v\n", min_dx, max_dx)
	for dx := min_dx; dx <= max_dx; dx++ {
		negative_dy_streak := 0
		fmt.Printf("iteration: %v\n", dx)
		for dy := -200; negative_dy_streak < 1000 && dy < 2000; dy++ {
			fmt.Printf("solution: %v %v\n", dx, dy)
			dest_x, _, max_height, err := SimulateThrow(dx, dy, surface)
			if err != nil {
				// not a solution solution
				fmt.Printf("%v: %v %v\n", err, dest_x, max_height)
				negative_dy_streak += 1
			} else {
				//probably a solution
				throw := &Throw{
					dx:     dx,
					dy:     dy,
					height: max_height,
				}
				heap.Push(&throws, throw)
				fmt.Printf("res is %v %v index %v\n", throw.dx, throw.dy, throw.index)
				negative_dy_streak = 0
			}
		}
	}
	fmt.Printf("solutions: %v\n", throws.Len())
	best_throw := heap.Pop(&throws).(*Throw)
	fmt.Printf("best throw is: %v %v with height: %v\n", best_throw.dx, best_throw.dy, best_throw.height)
}

func main() {
	fmt.Println("hello world!")
	sur := ReadInput("input.txt")
	Puzzle1(&sur)
}
