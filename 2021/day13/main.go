package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Fold struct {
	direction string
	len       int
}

func ReadInput(filename string) ([]int, []int, []Fold) {
	file, err := os.Open(filename)
	if err != nil {
		panic("error opening file")
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	var x []int
	var y []int
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			break
		}
		split := strings.Split(line, ",")
		point_x, err := strconv.Atoi(split[0])
		if err != nil {
			panic(fmt.Sprintf("err occurred with x coordinate: %v", err))
		}
		x = append(x, point_x)
		point_y, err := strconv.Atoi(split[1])
		if err != nil {
			panic(fmt.Sprintf("err occurred with y coordinate: %v", err))
		}
		y = append(y, point_y)
	}
	var folds []Fold
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		split := strings.Split(line, "=")
		fold_len, err := strconv.Atoi(split[1])
		if err != nil {
			panic("err occurred with folding len")
		}
		direction := split[0][len(split[0])-1:]
		folds = append(folds, Fold{direction, fold_len})
	}

	return x, y, folds
}

func max(arr []Fold) (int, int) {
	maxx, maxy := 0, 0
	for _, elem := range arr {
		if elem.direction == "x" && elem.len > maxx {
			maxx = elem.len
		} else if elem.direction == "y" && elem.len > maxy {
			maxy = elem.len
		}
	}
	return maxx*2 + 1, maxy*2 + 1
}

func main() {
	var x, y, folds = ReadInput("input.txt")
	var maxx, maxy = max(folds)
	fmt.Printf("Max x is %v max y is %v\n", maxx, maxy)
	paper := make([][]int, maxy)
	for i := range paper {
		paper[i] = make([]int, maxx)
	}

	for i := range x {
		paper[y[i]][x[i]] = 1
	}

	var lenx, leny = maxx, maxy
	for index, fold := range folds {
		fmt.Printf("Folding %v at %v\n", index+1, fold.len)
		fmt.Printf("Y: %v X: %v,\n", leny, lenx)
		if fold.direction == "x" {
			for i := 0; i < leny; i++ {
				for j := 0; j < fold.len; j++ {
					if paper[i][fold.len+1+j] == 1 {
						paper[i][fold.len-1-j] = 1
					}
				}
			}
			lenx = fold.len
		} else if fold.direction == "y" {
			for i := 0; i < fold.len; i++ {
				for j := 0; j < lenx; j++ {
					if paper[fold.len+1+i][j] == 1 {
						paper[fold.len-1-i][j] = 1
					}
				}
			}
			leny = fold.len
		}
	}
	var count = 0
	for i := 0; i < leny; i++ {
		for j := 0; j < lenx; j++ {
			if paper[i][j] == 1 {
				count = count + 1
				fmt.Print("#")
			} else {
				fmt.Print(".")
			}
		}
		fmt.Println()
	}
	fmt.Printf("Count: %v\n", count)
}
