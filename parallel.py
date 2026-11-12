from __builtins__ import *
from maze import dfs, spawn_maze
from planting import insertion_sort_with_swapping, simple_bubble_sort
from utils import (
	back_to_start,
	go_to_position,
	move_cactus_to_position,
	water_all_tiles,
)


def harvest_whole_col():
	for y in range(get_world_size() - 1):
		while can_harvest() != True:
			pass
		harvest()
		if num_items(Items.Fertilizer) > 0:
			use_item(Items.Fertilizer)
		move(North)
	harvest()


def plant_whole_col(crop: Entity, condition):
	for y in range(get_world_size() - 1):
		while can_harvest() != True:
			pass
		harvest()
		if condition():
			plant(crop)
		move(North)
	while can_harvest() != True:
		pass
	harvest()
	if condition():
		plant(crop)


def one_drone_per_col_except_last(drone_function):
	# returns handle for first drone
	first_drone = None
	for x in range(get_world_size() - 1):
		other_drone = None
		if first_drone == None:
			while first_drone == None:
				first_drone = spawn_drone(drone_function)
		else:
			while other_drone == None:
				other_drone = None
				other_drone = spawn_drone(drone_function)
		move(East)
	return first_drone


def one_drone_per_col_except_last_with_args(drone_function, crop: Entity, condition):
	# returns handle for first drone
	first_drone = None
	for x in range(get_world_size() - 1):
		other_drone = None
		if first_drone == None:
			while first_drone == None:
				first_drone = spawn_drone(drone_function, crop, condition)
		else:
			while other_drone == None:
				other_drone = None
				other_drone = spawn_drone(drone_function, crop, condition)
		move(East)
	return first_drone


# --- HAY ---
def infinite_grass(watering: bool = False, water_level: float = 0.25, max: int = 50000):
	while num_items(Items.Hay) < max + 1:
		first_drone = one_drone_per_col_except_last(harvest_whole_col)
		wait_for(first_drone)
		spawn_drone(harvest_whole_col)
		go_to_position(0, 0)
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


# --- TREE ---
def infinite_tree(watering: bool = False, water_level: float = 0.25, max: int = 50000):
	if watering:
		water_lvl = water_level
	else:
		water_lvl = None

	def check_tree_plantable() -> bool:
		cond = (get_pos_x() + get_pos_y()) % 2 == 0
		if cond and water_lvl != None:
			while get_water() < water_lvl:
				use_item(Items.Water)
		return cond

	while num_items(Items.Wood) < max + 1:
		first_drone = one_drone_per_col_except_last_with_args(
			plant_whole_col, Entities.Tree, check_tree_plantable
		)
		wait_for(first_drone)
		spawn_drone(plant_whole_col, Entities.Tree, check_tree_plantable)
		go_to_position(0, 0)
		quick_print("Here we go again")


# --- CARROT ---
def infinite_carrot(
	watering: bool = False, water_level: float = 0.25, max: int = 50000
):
	if watering:
		water_lvl = water_level
	else:
		water_lvl = None

	def check_if_already_tilled():
		if get_ground_type() != Grounds.Soil:
			till()
		if water_lvl != None:
			while get_water() < water_level:
				use_item(Items.Water)
		return True

	while (
		num_items(Items.Carrot) < max + 1
		and num_items(Items.Hay) > 1000
		and num_items(Items.Wood) > 1000
	):
		first_drone = one_drone_per_col_except_last_with_args(
			plant_whole_col, Entities.Carrot, check_if_already_tilled
		)
		wait_for(first_drone)
		spawn_drone(plant_whole_col, Entities.Carrot, check_if_already_tilled)
		go_to_position(0, 0)
		quick_print("Here we go again")


# --- CACTUS ---
def infinite_cacti(watering: bool = False, water_level: float = 0.25, max: int = 50000):
	def scan() -> dict:
		location_sizes: dict[tuple, int] = {}
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
		return location_sizes

	def sort_using_all_drones(location_sizes: dict, rows: bool) -> list:
		def do_col_sort(x, movements_required):
			for movement in movements_required:
				go_to_position(x, movement[0])
				move_cactus_to_position(x, movement[1])

		def do_row_sort(y, movements_required):
			for movement in movements_required:
				go_to_position(movement[0], y)
				move_cactus_to_position(movement[1], y)

		handlers = []
		if rows:
			index = 1
			position = 0
			drone_func = do_row_sort
		else:
			index = 0
			position = 1
			drone_func = do_col_sort

		for i in range(get_world_size()):
			this_col_locations_only = []
			for location in location_sizes:
				if location[index] == i:
					this_col_locations_only.append(location[position])
			sorted_this_col_locations_only = simple_bubble_sort(this_col_locations_only)

			this_col_sizes_only = []
			for j in sorted_this_col_locations_only:
				if rows:
					key = (j, i)
				else:
					key = (i, j)
				size = location_sizes[key]
				this_col_sizes_only.append(size)

			movements_required = insertion_sort_with_swapping(this_col_sizes_only)
			handler = spawn_drone(drone_func, i, movements_required)
			if handler:
				handlers.append(handler)
			else:
				drone_func(i, movements_required)

		return handlers

	if watering:
		water_lvl = water_level
	else:
		water_lvl = None

	def check_if_already_tilled():
		if get_ground_type() != Grounds.Soil:
			till()
		if water_lvl != None:
			while get_water() < water_level:
				use_item(Items.Water)
		return True

	while num_items(Items.Cactus) < max + 1 and num_items(Items.Pumpkin) > 1000:
		clear()
		first_drone = one_drone_per_col_except_last_with_args(
			plant_whole_col, Entities.Cactus, check_if_already_tilled
		)
		wait_for(first_drone)
		spawn_drone(plant_whole_col, Entities.Cactus, check_if_already_tilled)
		go_to_position(0, 0)
		location_sizes = scan()
		handlers = sort_using_all_drones(location_sizes, False)
		for handler in handlers:
			wait_for(handler)
		go_to_position(0, 0)
		location_sizes = scan()
		handlers = sort_using_all_drones(location_sizes, True)
		for handler in handlers:
			wait_for(handler)
		go_to_position(0, 0)
		harvest()
		quick_print("Here we go again")


# --- MAZE ---
def find_32_drone_starting_positions() -> list[tuple[int, int]]:
	positions = []
	x_locs = [2, 10, 18, 26]
	y_locs = [2, 6, 10, 14, 18, 22, 26, 30]
	for x in x_locs:
		for y in y_locs:
			positions.append((x, y))
	return positions


def infinite_maze(max: int = 50000):
	def solve_maze_starting_at(position: tuple[int, int], start_time: float):
		go_to_position(position[0], position[1])
		while get_time() < start_time:
			do_a_flip()
		while True:
			spawn_maze(4)
			dfs()
			go_to_position(position[0], position[1])

	# while num_items(Items.Gold) < max and can_spawn_maze():
	sync_start = get_time() + 2.0
	handlers = []
	go_to_position(0, 0)
	for position in find_32_drone_starting_positions():
		handler = spawn_drone(solve_maze_starting_at, position, sync_start)
		if handler:
			handlers.append(handler)
		else:
			solve_maze_starting_at(position, sync_start)
		# for handler in handlers:
		# 	wait_for(handler)
