from __builtins__ import *


def spawn_maze(size=None):
	plant(Entities.Bush)
	if size == None:
		size = get_world_size()
	substance = size * 2 ** (num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)


def opposite_direction(starting_direction: Direction) -> Direction:
	if starting_direction == West:
		way = East
	if starting_direction == East:
		way = West
	if starting_direction == North:
		way = South
	if starting_direction == South:
		way = North
	return way


def reverse_along_a_path(path: list[Direction]):
	reversed_path = []
	end_idx = len(path) - 1
	for i in range(len(path)):
		key = end_idx - i
		reversed_path.append(path[key])

	for step in reversed_path:
		move(opposite_direction(step))


def only_free_directions() -> list[Direction]:
	free_directions = []
	# 1 - 4 free directions always
	for direction in [North, South, East, West]:
		if can_move(direction):
			free_directions.append(direction)
	return free_directions


def move_as_long_as_only_two_directions(last_step: Direction) -> Direction:
	# goes wherever is free next, never going back, returning which step it took
	available = only_free_directions()
	wrong_way = opposite_direction(last_step)
	if len(available) != 2:
		print("Used when not only 2 directions available!!")
	for direction in available:  # find only other way to go
		if direction != wrong_way:
			right_way = direction
	move(right_way)
	return right_way


def find_next_node(starting_directon: Direction) -> tuple[string, list]:
	# goes off in a direction, until it gets stuck
	# item 1 is either "treasure", "dead end", or "node"
	# item 2 is steps that were taken along the way
	steps_taken: list[Direction] = []
	move(starting_directon)
	steps_taken.append(starting_directon)

	if get_entity_type() == Entities.Treasure:
		harvest()
		return "treasure", steps_taken

	available = only_free_directions()
	if len(available) == 1:  # dead end already
		return "dead end", steps_taken
	if len(available) >= 3:
		return "node", steps_taken

	while len(available) == 2:  # ploughing on to next node
		step_just_taken = move_as_long_as_only_two_directions(steps_taken[-1])
		steps_taken.append(step_just_taken)
		available = only_free_directions()
		if get_entity_type() == Entities.Treasure:
			harvest()
			return "treasure", steps_taken
		if len(available) == 1:  # dead end
			return "dead end", steps_taken
		elif len(available) >= 3:
			return "node", steps_taken

	# should never trigger
	return "oops", steps_taken


def initial_move() -> tuple[Direction, dict, int]:
	evolving_graph = {"visited": True, "steps_from_parent": [], "children": []}
	available = only_free_directions()
	for direction in available:
		direction_chosen = direction  # last free path found
		evolving_graph["children"].append(
			{"visited": False, "steps_from_parent": [direction], "children": []}
		)
	move(direction_chosen)
	node_taken = len(evolving_graph["children"]) - 1
	return direction_chosen, evolving_graph, node_taken


def get_nested_node(tree, path):
	current = tree
	for node_index in path:
		current = current["children"][node_index]
	return current


def update_nested_node(tree, path, visited=None, steps_from_parent=None, children=None):
	current = tree
	for node_index in path:
		current = current["children"][node_index]
	for k, v in [
		("visited", visited),
		("steps_from_parent", steps_from_parent),
		("children", children),
	]:
		if v != None:
			current[k] = v


def add_child_node(tree, path, visited=None, steps_from_parent=None) -> int:
	# returns index of node added
	current = tree
	for node_index in path:
		current = current["children"][node_index]
	current["children"].append(
		{"visited": visited, "steps_from_parent": steps_from_parent, "children": []}
	)
	return len(current["children"]) - 1


def dfs():
	if get_entity_type() == Entities.Treasure:
		harvest()
		return
	first_step, evolving_graph, node_taken = initial_move()
	if get_entity_type() == Entities.Treasure:
		harvest()
		return
	move(opposite_direction(first_step))

	next_step = first_step
	result = ""
	nodes_taken = []
	next_node_index = node_taken
	while result != "treasure":
		nodes_taken.append(next_node_index)
		result, steps_taken = find_next_node(next_step)
		if result == "treasure":  # WE DID IT
			harvest()
			return
		elif result == "dead end":  # we need to backtrack and mark visited
			update_nested_node(evolving_graph, nodes_taken, True, steps_taken)

			# go up the tree until another branch is available
			route_available = False
			while route_available != True:
				current_nodes_tree: dict = get_nested_node(evolving_graph, nodes_taken)
				reverse_along_a_path(current_nodes_tree["steps_from_parent"])
				nodes_taken.pop()

				current_nodes_tree: dict = get_nested_node(evolving_graph, nodes_taken)
				available_directions: list[Direction] = only_free_directions()
				for i in range(len(current_nodes_tree["children"])):
					d = current_nodes_tree["children"][i]
					direction = d["steps_from_parent"][0]
					if d["visited"] == False and direction in available_directions:
						next_step = direction
						next_node_index = i
						route_available = True
						break
		elif result == "node":  # we need to go down any open route, creating new node
			# this node is ALWAYS new here
			available = only_free_directions()
			just_came_from = steps_taken[-1]
			therefore_dont_go = opposite_direction(just_came_from)
			available.remove(therefore_dont_go)

			update_nested_node(evolving_graph, nodes_taken, True, steps_taken)

			for direction in available:
				direction_chosen = direction  # last free path found
				child_index_chosen = add_child_node(
					evolving_graph,
					nodes_taken,
					False,
					[direction],
				)
			next_step = direction_chosen
			next_node_index = child_index_chosen


def spawn_and_solve_maze():
	spawn_maze()
	dfs()
	print("MAZE SOLVED")
