from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
# Graph of traversed rooms (it's really just a dictionary shh)
graph = {}
# Path for backtracking
current_path = []
# Dictionary containing opposite directions (useful for backtracking)
opposite_direction = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}

def next_direction(current_room):
    """
    Helper function that returns a direction to move in
    or None if you're currently at a dead end
    """
    for direction, room in current_room.items():
        if room is '?':
            return direction
    return None

while len(graph) != len(world.rooms):
    # Reference to current room
    current_room = player.current_room
    current_room_id = player.current_room.id
    previous_room_id = None

    # Check if the current room is stored in the graph
    if current_room_id not in graph:
        # Get every possible direction to move in the current room 
        graph[current_room_id] = { direction: '?' for direction in player.current_room.get_exits()}
    
    # Choose direction to go in
    direction = next_direction(graph[current_room_id])
    
    # If dead end
    if direction is None:
        new_path = current_path.pop()
        player.travel(opposite_direction[new_path])
        traversal_path.append(opposite_direction[new_path])
        continue

    # Update reference to previous rooom
    previous_room_id = player.current_room.id
    # Travel to generated directioon
    player.travel(direction)
    # Add direction traveled to traversal path
    traversal_path.append(direction)
    # Add direction traveled to current_path (for backtracking)
    current_path.append(direction)
    # Update reference of current room
    current_room = player.current_room
    current_room_id = player.current_room.id

    # Check if the current room is stored in the graph
    if current_room_id not in graph:
        # Get every possible direction to move in the current room 
        graph[current_room_id] = { direction: '?' for direction in player.current_room.get_exits()}

    # Link rooms together
    if graph[current_room_id][opposite_direction[direction]] == '?':
        graph[current_room_id][opposite_direction[direction]] = previous_room_id
        graph[previous_room_id][direction] = current_room_id

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
