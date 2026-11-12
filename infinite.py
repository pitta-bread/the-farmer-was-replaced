from __builtins__ import *
from maze import spawn_and_solve_maze
from planting import (
	bone_time,
	harvest_giant_pumpkin,
	plant_field_of_c,
	plant_field_of_crop,
	plant_field_of_sunflower,
	plant_field_of_trees,
	sort_and_harvest_field_of_cacti,
)
from utils import back_to_start, water_all_tiles


def can_spawn_maze() -> bool:
	maze_level = num_unlocked(Unlocks.Mazes)
	if maze_level == 0:
		return False
	substance_needed = get_world_size() * 2 ** (maze_level - 1)
	return num_items(Items.Weird_Substance) >= substance_needed


def infinite_maze(max: int = 50000):
	while num_items(Items.Gold) < max and can_spawn_maze():
		spawn_and_solve_maze()
		back_to_start()
		quick_print("Here we go again")
	if num_items(Items.Gold) < max:
		quick_print("Maze farming stopped: unlock Mazes or add Weird Substance")


def infinite_tree(watering: bool = False, water_level: float = 0.25, max: int = 50000):
	while num_items(Items.Wood) < max + 1:
		plant_field_of_trees()
		back_to_start()
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


def infinite_grass(watering: bool = False, water_level: float = 0.25, max: int = 50000):
	while num_items(Items.Hay) < max + 1:
		plant_field_of_crop(Entities.Grass, False)
		back_to_start()
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


def infinite_carrot(
	watering: bool = False, water_level: float = 0.25, max: int = 50000
):
	while (
		num_items(Items.Carrot) < max + 1
		and num_items(Items.Hay) > 1000
		and num_items(Items.Wood) > 1000
	):
		plant_field_of_crop(Entities.Carrot, True)
		back_to_start()
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


def infinite_pumpkin(
	watering: bool = False, water_level: float = 0.25, max: int = 50000
):
	while num_items(Items.Pumpkin) < max + 1 and num_items(Items.Carrot) > 1000:
		plant_field_of_c(Entities.Pumpkin)
		back_to_start()
		harvest_giant_pumpkin()
		back_to_start()
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


def infinite_sun_power(
	watering: bool = False, water_level: float = 0.25, max: int = 50000
):
	locations_and_sizes = None
	while num_items(Items.Power) < max + 1 and num_items(Items.Carrot) > 1000:
		locations_and_sizes = plant_field_of_sunflower(locations_and_sizes)
		back_to_start()
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


def infinite_cacti(watering: bool = False, water_level: float = 0.25, max: int = 50000):
	while num_items(Items.Cactus) < max + 1 and num_items(Items.Pumpkin) > 1000:
		plant_field_of_c(Entities.Cactus)
		back_to_start()
		sort_and_harvest_field_of_cacti()
		back_to_start()
		if watering:
			water_all_tiles(water_level)
			back_to_start()
		quick_print("Here we go again")


def infinite_bones(max: int = 50000):
	apple_cost = get_cost(Entities.Apple)
	apples_needed = get_world_size() ** 2 - 10
	while num_items(Items.Bone) < max + 1:
		for item in apple_cost:
			if num_items(item) < apple_cost[item] * apples_needed:
				return
		bone_time()
		# The hat can't cross the world border, so take it off before travelling.
		change_hat(Hats.Straw_Hat)
		clear()
		back_to_start()
		quick_print("Here we go again")
