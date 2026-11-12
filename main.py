from __builtins__ import *
from parallel import infinite_carrot
from utils import back_to_start

POWER_UP = True
WATER_ON = True
WATER_LEVEL = 0.4
TARGET_POWER = 10000
TARGET_HAY = 1000000000
TARGET_WOOD = 10000000000
TARGET_CARROT = 1000000000
TARGET_PUMPKIN = 10000000
TARGET_CACTI = 1000000000
TARGET_BONE = 1000000
TARGET_GOLD = 100000000
CHUNK = 10000000000


def goal(item, target):
	# Next stopping point for this crop so main can rotate to the others.
	return min(target, num_items(item) + CHUNK)


if __name__ == "__main__":
	# set_world_size(5)
	clear()
	change_hat(Hats.Carrot_Hat)
	move(South)
	move(West)
	back_to_start()
	print("Starting Power: ", num_items(Items.Power))

	while True:
		infinite_carrot(WATER_ON, WATER_LEVEL, 1000000000)

	# # --- TARGET BALANCING ---
	# while (
	#     num_items(Items.Hay) < TARGET_HAY
	#     or num_items(Items.Wood) < TARGET_WOOD
	#     or num_items(Items.Carrot) < TARGET_CARROT
	#     or num_items(Items.Pumpkin) < TARGET_PUMPKIN
	#     or num_items(Items.Cactus) < TARGET_CACTI
	#     or num_items(Items.Bone) < TARGET_BONE
	#     or (num_items(Items.Gold) < TARGET_GOLD and can_spawn_maze())
	# ):
	#     # if POWER_UP and num_items(Items.Power) < 10000:
	#     # 	clear()
	#     # 	infinite_sun_power(WATER_ON, WATER_LEVEL, 10000)
	#     # if num_items(Items.Gold) < TARGET_GOLD and can_spawn_maze():
	#     #     clear()
	#     #     infinite_maze(goal(Items.Gold, TARGET_GOLD))
	#     # if num_items(Items.Bone) < TARGET_BONE and num_items(Items.Cactus) > 5000:
	#     #     clear()
	#     #     infinite_bones(goal(Items.Bone, TARGET_BONE))
	#     # if num_items(Items.Cactus) < TARGET_CACTI and num_items(Items.Pumpkin) > 5000:
	#     #     clear()
	#     #     infinite_cacti(WATER_ON, WATER_LEVEL, goal(Items.Cactus, TARGET_CACTI))
	#     # if num_items(Items.Pumpkin) < TARGET_PUMPKIN and num_items(Items.Carrot) > 5000:
	#     #     clear()
	#     #     infinite_pumpkin(WATER_ON, WATER_LEVEL, goal(Items.Pumpkin, TARGET_PUMPKIN))
	#     if (
	#         num_items(Items.Carrot) < TARGET_CARROT
	#         and num_items(Items.Hay) > 5000
	#         and num_items(Items.Wood) > 5000
	#     ):
	#         clear()
	#         infinite_carrot(WATER_ON, WATER_LEVEL, goal(Items.Carrot, TARGET_CARROT))
	#         infinite_carrot(WATER_ON, WATER_LEVEL, goal(Items.Carrot, TARGET_CARROT))
	#         infinite_carrot(WATER_ON, WATER_LEVEL, goal(Items.Carrot, TARGET_CARROT))
	#     if num_items(Items.Wood) < TARGET_WOOD:
	#         clear()
	#         infinite_tree(WATER_ON, WATER_LEVEL, goal(Items.Wood, TARGET_WOOD))
	#     if num_items(Items.Hay) < TARGET_HAY:
	#         clear()
	#         infinite_grass(WATER_ON, WATER_LEVEL, goal(Items.Hay, TARGET_HAY))

	print("You DONE son.")
