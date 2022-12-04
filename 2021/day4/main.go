package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type board interface {
	markNumber(int)
	isSolved() bool
	finalScore() int
}

type Board struct {
	t    [][]int
	h, w int
}

func (b Board) markNumber(num int) {
	for i := 0; i < b.w; i++ {
		for j := 0; j < b.h; j++ {
			if b.t[i][j] == num {
				b.t[i][j] = -1
			}
		}
	}
}

func (b Board) finalScore() int {
	sum := 0
	for i := 0; i < b.w; i++ {
		for j := 0; j < b.h; j++ {
			if b.t[i][j] != -1 {
				sum += b.t[i][j]
			}
		}
	}
	return sum
}

func (b Board) isSolved() bool {
	// row
	for i := 0; i < b.w; i++ {
		is_solved := true
		for j := 0; j < b.h; j++ {
			if b.t[i][j] != -1 {
				is_solved = false
				break
			}
		}
		if is_solved {
			return true
		}
	}
	//column
	for i := 0; i < b.w; i++ {
		is_solved := true
		for j := 0; j < b.h; j++ {
			if b.t[j][i] != -1 {
				is_solved = false
				break
			}
		}
		if is_solved {
			return true
		}
	}
	return false
}

func StringToArray(s, delimiter string) []int {
	var elems []string
	if delimiter == " " {
		elems = strings.Fields(s)
	} else {
		elems = strings.Split(s, delimiter)
	}
	var numbers []int
	for i := range elems {
		num, err := strconv.Atoi(elems[i])
		if err != nil {
			panic(fmt.Sprintf("wrong conversion: %s", err))
		}
		numbers = append(numbers, num)
	}
	return numbers
}

func ReadBoards(filename string) ([]Board, []int) {
	file, err := os.Open(filename)
	if err != nil {
		panic("error opening file")
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)

	is_first_line := true
	var boards []Board
	var numbers []int
	// optionally, resize scanner's capacity for lines over 64K, see next example
	counter := 0
	boards_size := 0
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if line == "" {
			continue
		}
		if is_first_line {
			is_first_line = false
			numbers = StringToArray(line, ",")
			continue
		}
		if counter%5 == 0 {
			boards = append(boards, Board{make([][]int, 5), 5, 5})
			boards_size += 1
		}
		boards[boards_size-1].t[counter%5] = StringToArray(line, " ")
		counter += 1
	}
	return boards, numbers
}

func PuzzleOne() {
	boards, numbers := ReadBoards("input.txt")

	bingo := false
	for _, num := range numbers {
		for i, board := range boards {
			board.markNumber(num)
			if board.isSolved() {
				fmt.Printf("board: %v num: %v\n", i, num)
				fmt.Printf("bingooo: %v\n", board.finalScore()*num)
				bingo = true
				break
			}
		}
		if bingo {
			break
		}
	}
}

func isIntInArray(arr *[]int, elem int) bool {
	for _, v := range *arr {
		if v == elem {
			return true
		}
	}
	return false
}

func PuzzleTwo() {
	boards, numbers := ReadBoards("input.txt")

	var winners []int
	var last_winning_number int
	for _, num := range numbers {
		fmt.Printf("Num is: %v\n", num)
		if len(winners) == len(boards) {
			fmt.Print("game over!\n")
			break
		}
		for i, board := range boards {
			if isIntInArray(&winners, i) {
				continue
			}
			board.markNumber(num)
			if board.isSolved() {
				fmt.Printf("board: %v num: %v\n", i, num)
				winners = append(winners, i)
				last_winning_number = num
			}
		}
	}
	fmt.Printf("The last winner is: %v and num: %v\n", winners[len(winners)-1], last_winning_number)
	fmt.Printf("Score: %v\n", boards[winners[len(winners)-1]].finalScore())
	fmt.Printf("Result: %v\n", boards[winners[len(winners)-1]].finalScore()*last_winning_number)
}

func main() {
	PuzzleTwo()
}
