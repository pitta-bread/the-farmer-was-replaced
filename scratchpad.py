from __builtins__ import *
from maze import dfs, spawn_maze
from utils import back_to_start, go_to_position


def simple_sort(input_list: list[int]) -> list:
	swaps = True
	while swaps != False:
		swaps = False
		for i in range(len(input_list)):
			if i + 1 >= len(input_list):
				break
			if input_list[i] <= input_list[i + 1]:
				continue
			if input_list[i] > input_list[i + 1]:
				swaps = True
				first = input_list[i]
				second = input_list[i + 1]
				input_list[i] = second
				input_list[i + 1] = first
	return input_list


def insertion_sort(whole_list: list) -> list:
	sorted_list = [whole_list[0]]
	for i in range(1, len(whole_list)):
		next_up = whole_list[i]
		for j in range(len(sorted_list)):
			if next_up <= sorted_list[j]:
				sorted_list.insert(j, next_up)
				break
			elif j + 1 >= len(sorted_list):
				sorted_list.append(next_up)
				break
			elif next_up >= sorted_list[j] and next_up <= sorted_list[j + 1]:
				sorted_list.insert(j + 1, next_up)
				break
	return sorted_list


my_list = [5, 3, 3, 4, 3, 1, 9, 2, 2, 5]

print(insertion_sort(my_list))

clear()
back_to_start()
for i in range(8):
	move(East)
	move(North)
spawn_maze(4)
dfs()

go_to_position(3, 31)
change_hat(Hats.Top_Hat)
