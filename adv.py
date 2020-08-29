
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

# sets up directions in order to "reverse" If we moved east previously it makes it west
reversedir = {"n": "s", "s": "n", "e": "w", "w": "e"}
reverse = [None]

# route for knowing where I've been.

# before refactor
# route = visited = {}  # Note that this is a dictionary, not a set
# before refactor

# after refactor
# Didnt effect number of moves :/
visited = {}  # Note that this is a dictionary, not a set
route = []
DIR = ""
# after refactor

# runs while we have not yet been to all rooms in world
while len(visited) < len(room_graph):
    local = player.current_room.id
    print("Local Room Number is ===>", local)
    # gets exits to the local room
    localexits = player.current_room.get_exits()

    # before refactor
    # DIR = ""
    # before refactor

    # adds local room to route
    # after refactor
    route.append({local: DIR})
    # after refactor

    if local not in visited:
        # if we haven't just started.
        if reverse[-1]:
            # remove the most recently used dir from exits so we don't go back into it when we return to prev room.
            localexits.remove(reverse[-1])
        # sets exits to local to visited
        visited[local] = localexits

# if we have directions to go / room has exits other than the one we came in
#     will try to go east first, then south west north

    if len(visited[local]) > 0:
        # pop off the last one we were just in
        DIR = visited[local].pop()
        # put it in the map
        traversal_path.append(DIR)
        # map the reverse direction
        reverse.append(reversedir[DIR])
        # MOVETO if there is a "forward" path
        print("The Journey continues! Move Forward", DIR)
        player.travel(DIR)
    # if we hit a dead end, initiates reverse and backtracks along path
    else:
        # take off the most recent direction and move the opposite direction until there are available exits
        if reverse[-1]:
            DIR = reverse.pop()
            traversal_path.append(DIR)
            print("Oof Move Back", DIR)
            player.travel(DIR)



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
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")