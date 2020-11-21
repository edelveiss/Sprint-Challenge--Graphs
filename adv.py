from room import Room
from player import Player
from world import World
from collections import deque
from collections import defaultdict

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

#===================================================================
#------------------add_room_and_directions_to_graph-----------------
def add_room_and_directions_to_graph(directions_arr, graph, curr_room_id):
    for direction in directions_arr:
        graph[curr_room_id].add(direction)

# use this for printing rooms id for debugging
# traversal_rooms = []

# fills out traversal_path
def get_traversal_path(traversal_path):
    # graph for keeping visited rooms and their doorways
    visited_graph = defaultdict(set)
    # stack for adding opposite directions for going back from already visited rooms
    back_path = deque()
     
    # dictionary for converting direction to the opposite value
    back_direction = {
        's': 'n',
        'n': 's',
        'e': 'w',
        'w': 'e'
    }

    # adding starting room and directions for starting room to visited_graph: {0: {'e', 'w', 's', 'n'}}
    add_room_and_directions_to_graph(player.current_room.get_exits(), visited_graph, player.current_room.id)
    
    # keep visit every room until we visit all from room_graph
    while len(visited_graph) < len(room_graph) :
        if player.current_room.id not in visited_graph:
            # if current room is not in visited - add this room and its exits to the visited_graph
            add_room_and_directions_to_graph(player.current_room.get_exits(), visited_graph, player.current_room.id)

            # getting previous room that we came from for removing it from the direction set of the current room
            prev_room_direction = back_path[-1]
            visited_graph[player.current_room.id].discard(prev_room_direction)
        else:
            # if we have already visited current room and direction set is empty, go back to the previous room until there is a way to the next room
            while len(visited_graph[player.current_room.id]) == 0:
                # remove the room where we have been and go back to the previous room
                prev_room_direction = back_path.pop()
                # add prev_room direction to our traversal_path
                traversal_path.append(prev_room_direction)
                # traversal_rooms.append(player.current_room.get_room_in_direction(prev_room_direction).id)
                player.travel(prev_room_direction)

            # go straight for removing reduntant moves
            if len(traversal_path) >0 and traversal_path[-1] in visited_graph[player.current_room.id]:
                visited_graph[player.current_room.id].discard(traversal_path[-1])
                next_room_direction = traversal_path[-1]
            else:
                # pick random room direction from current room direction set
                next_room_direction = visited_graph[player.current_room.id].pop()

            # do not return to visited room where opposite direction was popped, pick up the next direction 
            if player.current_room.get_room_in_direction(next_room_direction).id in visited_graph:
                if back_direction[next_room_direction] not in visited_graph[player.current_room.get_room_in_direction(next_room_direction).id] and len(visited_graph[player.current_room.id]) >0:
                    # pick up the next direction
                    next_room_direction = visited_graph[player.current_room.id].pop()


            # add next_room direction to our traversal_path
            traversal_path.append(next_room_direction)
            # traversal_rooms.append(player.current_room.get_room_in_direction(next_room_direction).id)
            # add opposite direction to back_path for going back from already visited rooms
            back_path.append(back_direction[next_room_direction])
            # travel to the next room which  becomes the current room
            player.travel(next_room_direction)

#========================================================

get_traversal_path(traversal_path)
# print(traversal_path)
# print(traversal_rooms)

# min moves:
#TESTS PASSED: 992 moves, 500 rooms visited




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
