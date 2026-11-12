from __builtins__ import *
from utils import back_to_start, go_to_position, move_cactus_to_position


def plant_field_of_trees():
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if (
				(((y % 2) == 0) and ((x % 2) == 1))
				or (((y % 2) == 0) and ((x % 2) == 0))
			) and can_harvest():
				harvest()
				plant(Entities.Tree)

			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)


def plant_field_of_crop(entity: Entity, soil: bool):
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if can_harvest():
				harvest()
				if soil and (get_ground_type() != Grounds.Soil):
					till()
				if entity == Entities.Grass:
					pass
				else:
					plant(entity)
			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)


def plant_field_of_c(c: Entity):
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() != c:
				plant(c)
			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)


def harvest_giant_pumpkin():
	dead_pumpkins = []
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if get_entity_type() == Entities.Dead_Pumpkin:
				plant(Entities.Pumpkin)
				dead_pumpkins.append((get_pos_x(), get_pos_y()))
			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)

	def find_dead(locations_to_check: list):
		still_dead = []
		for location in locations_to_check:
			go_to_position(location[0], location[1])
			if get_entity_type() == Entities.Dead_Pumpkin:
				if num_items(Items.Fertilizer) > 1000:
					while get_entity_type() == Entities.Dead_Pumpkin:
						plant(Entities.Pumpkin)
						use_item(Items.Fertilizer, 2)
				else:
					plant(Entities.Pumpkin)
					still_dead.append(location)
		return still_dead

	while len(dead_pumpkins) > 0 and num_items(Items.Carrot) > 1000:
		back_to_start()
		dead_pumpkins = find_dead(dead_pumpkins)

	harvest()


def determine_all_biggest(
	position_flower_sizes: dict[tuple[int, int], int],
) -> tuple[list, dict]:
	biggest_size = -1
	for key in position_flower_sizes:  # noqa: PLC0206
		biggest_size = max(biggest_size, position_flower_sizes[key])

	biggest_locations = []
	for key in position_flower_sizes:  # noqa: PLC0206
		if position_flower_sizes[key] == biggest_size:
			biggest_locations.append(key)

	# Pop only after iteration; the dict can't change size inside the loop.
	for key in biggest_locations:
		position_flower_sizes.pop(key)
	return biggest_locations, position_flower_sizes


# RECURSIVE BEHAVIOUR
def plant_field_of_sunflower(
	last_dict: dict[tuple[int, int], int] | None = None,
) -> dict:
	if last_dict != None:
		biggest_locations, popped_dict = determine_all_biggest(last_dict)
		while len(popped_dict) > 10 and num_items(Items.Carrot) > 1000:
			for biggest in biggest_locations:
				go_to_position(biggest[0], biggest[1])
				harvest()
			back_to_start()
			biggest_locations, popped_dict = determine_all_biggest(popped_dict)

	position_flower_sizes = {}
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if get_ground_type() != Grounds.Soil:
				till()
			if get_entity_type() != Entities.Sunflower:
				plant(Entities.Sunflower)
				position_flower_sizes[(get_pos_x(), get_pos_y())] = measure()
			elif get_entity_type() == Entities.Sunflower and can_harvest():
				harvest()
				plant(Entities.Sunflower)
				position_flower_sizes[(get_pos_x(), get_pos_y())] = measure()
			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)
	return position_flower_sizes


def simple_bubble_sort(input_list: list[int]) -> list:
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


# with tracking
def insertion_sort_with_swapping(whole_list: list[int]) -> list[tuple]:
	sorted_list = [whole_list[0]]
	movements = []
	for i in range(1, len(whole_list)):
		next_up = whole_list[i]
		for j in range(len(sorted_list)):
			if next_up < sorted_list[j]:
				sorted_list.insert(j, next_up)
				movements.append((i, j))
				break
			elif j + 1 >= len(sorted_list):
				sorted_list.append(next_up)
				movements.append((i, i))
				break
			elif next_up >= sorted_list[j] and next_up < sorted_list[j + 1]:
				sorted_list.insert(j + 1, next_up)
				movements.append((i, j + 1))
				break
	return movements


def sort_and_harvest_field_of_cacti():
	location_sizes: dict[tuple, int] = {}

	def scan():
		for x in range(get_world_size()):
			for y in range(get_world_size()):
				if get_entity_type() == Entities.Cactus:
					location_sizes[(get_pos_x(), get_pos_y())] = measure()  # ty: ignore[invalid-assignment]
				if y == (get_world_size() - 1):
					pass
				elif x % 2 == 1:
					move(South)
				else:
					move(North)
			move(East)

		back_to_start()

	back_to_start()
	scan()

	for x in range(get_world_size()):
		this_col_locations_only = []
		for location in location_sizes:
			if location[0] == x:
				this_col_locations_only.append(location[1])
		sorted_this_col_locations_only = simple_bubble_sort(this_col_locations_only)

		this_col_sizes_only = []
		for y in sorted_this_col_locations_only:
			size = location_sizes[(x, y)]
			this_col_sizes_only.append(size)

		# insertion sort, getting just movements required back, always starting at y=0
		movements_required = insertion_sort_with_swapping(this_col_sizes_only)

		# move each cactus, looping through
		for movement in movements_required:
			go_to_position(x, movement[0])
			move_cactus_to_position(x, movement[1])

	back_to_start()
	scan()

	for y in range(get_world_size()):
		this_row_locations_only = []
		for location in location_sizes:
			if location[1] == y:
				this_row_locations_only.append(location[0])
		sorted_this_row_locations_only = simple_bubble_sort(this_row_locations_only)

		this_row_sizes_only = []
		for x in sorted_this_row_locations_only:
			size = location_sizes[(x, y)]
			this_row_sizes_only.append(size)

		# insertion sort, getting just movements required back, always starting at x=0
		movements_required = insertion_sort_with_swapping(this_row_sizes_only)

		# move each cactus, looping through
		for movement in movements_required:
			go_to_position(movement[0], y)
			move_cactus_to_position(movement[1], y)

	harvest()


def bone_time():
	back_to_start()
	# clear field with tilling first
	for x in range(get_world_size()):
		for y in range(get_world_size()):
			if get_ground_type() != Grounds.Soil:
				till()
			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)

	back_to_start()
	change_hat(Hats.Dinosaur_Hat)

	def go_to_position_long_way_round(x: int, y: int):
		move_x = x - get_pos_x()
		move_y = y - get_pos_y()
		if get_pos_y() == get_world_size() - 1:
			move(West)
		elif (move_x >= 0) and (move_y >= 0) and get_pos_x() != 0:
			for i in range(move_x):
				move(East)
			for i in range(move_y):
				move(North)
			return

		if move(East) != True:
			move(North)
			move(West)
		# auto-stops on apples!
		# always goes back to start first, longest way
		for i in range(get_world_size()):
			if get_entity_type() == Entities.Apple:
				break
			move(North)
		for i in range(get_world_size()):
			if get_entity_type() == Entities.Apple:
				break
			move(West)
		for i in range(get_world_size()):
			if get_entity_type() == Entities.Apple:
				break
			move(South)

		# figure out where to go to, always positive movement
		while get_pos_x() != x or get_pos_y() != y:
			if get_entity_type() == Entities.Apple:
				break
			move_x = x - get_pos_x()
			# move_y = y - get_pos_y()

			for i in range(move_x):
				if get_entity_type() == Entities.Apple:
					break
				move(East)
			for i in range(get_world_size()):
				if get_entity_type() == Entities.Apple:
					break
				move(North)

	goal_x, goal_y = measure()  # ty: ignore[not-iterable]
	# initial hunt and peck up to length 40
	for i in range(40):
		go_to_position_long_way_round(goal_x, goal_y)  # ty: ignore[invalid-argument-type]
		print(measure())
		goal_x, goal_y = measure()  # ty: ignore[not-iterable]

	# hamiltonian looping until roughly max
	# always goes back to start next, longest other way
	for i in range(get_world_size()):
		move(North)
	for i in range(get_world_size()):
		move(East)
	for i in range(get_world_size()):
		move(South)
	for i in range(get_world_size()):
		move(West)

	count = 40
	rough_max = get_world_size() ** 2 - 10

	# Derived from the current tile, so it stays on the cycle after any stop.
	def cycle_step():
		# Cycle: up column 0, snake rows (top to y=1) over x>=1,
		# then return west along the bottom row.
		n = get_world_size()
		x = get_pos_x()
		y = get_pos_y()
		if y == 0:
			if x > 0:
				move(West)
			else:
				move(North)
		elif x == 0:
			if y < n - 1:
				move(North)
			else:
				move(East)
		elif (n - 1 - y) % 2 == 0:
			if x < n - 1:
				move(East)
			else:
				move(South)
		else:
			if x > 1:
				move(West)
			else:
				move(South)

	for apple_number in range(count, rough_max):
		while get_entity_type() != Entities.Apple:
			cycle_step()
		cycle_step()

	harvest()
