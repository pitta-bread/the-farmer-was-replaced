from __builtins__ import *


def sleep(duration):
	start = get_time()
	while get_time() - start < duration:
		pass


def back_to_start():
	go_to_position(0, 0)


def go_to_position(x: int, y: int):
	size = get_world_size()
	# The world wraps, so take whichever direction is shorter.
	move_x = (x - get_pos_x()) % size
	move_y = (y - get_pos_y()) % size

	if move_x <= size - move_x:
		for i in range(move_x):
			move(East)
	else:
		for i in range(size - move_x):
			move(West)

	if move_y <= size - move_y:
		for i in range(move_y):
			move(North)
	else:
		for i in range(size - move_y):
			move(South)


def water_all_tiles(level: float):
	for x in range(get_world_size()):
		if num_items(Items.Water) == 0 or get_water() > level + 0.15:
			break
		for y in range(get_world_size()):
			if num_items(Items.Water) == 0 or get_water() > level + 0.15:
				break
			if get_water() < level and num_items(Items.Water) > 0:
				use_item(Items.Water)
			if y == (get_world_size() - 1):
				pass
			elif x % 2 == 1:
				move(South)
			else:
				move(North)
		move(East)


def move_cactus_to_position(x: int, y: int):
	move_x = x - get_pos_x()
	move_y = y - get_pos_y()

	if move_x == 0:
		pass
	elif move_x > 0:
		for i in range(move_x):
			swap(East)
			move(East)
	elif move_x < 0:
		for i in range(-move_x):
			swap(West)
			move(West)

	if move_y == 0:
		pass
	elif move_y > 0:
		for i in range(move_y):
			swap(North)
			move(North)
	elif move_y < 0:
		for i in range(-move_y):
			swap(South)
			move(South)
