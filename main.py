import os, time, sys, re
from operations import *
from data_structures import *

def main():
    """
    The main game function. 
    This acts as the entry point and orchestrates the entire game flow by calling functions from operations.py.
    """

    # Game Text and Story Line
    story_text = {
        "intro": "\nWelcome to 'The Last Protocol'! \n\nWhat is your name, hacker? >",

        "start": "\nGreetings, {}. \n\nThe year is 2025. Kathmandu, once a hub of traditional charm, now thrives on the digital pulse of Skynet. \n\nBut something has gone wrong. Nova, the AI that manages the city, has been corrupted. \n\nIt now calls itself Oblivion. \n\nYour mission: infiltrate data hubs, bypass security, and restore systems while evading corporate drones. \n\nThe fate of Kathmandu's digital future rests on you. \n\nType 'help' for commands.",

        "final_protocol_start": "\nYou have reached the Patan Data Hub! \n\nIt's time to choose your final protocol. \nOptions: \n'protocol containment' (ethical, multi-step, undoable during steps) \nOR\n'protocol obliteration' (risky, irreversible)",

        "good_ending": "\nYou contained Oblivion. \n\nIts rogue code is now isolated, and it begins to mend the digital fabric of Kathmandu. \n\nTraffic flows, networks hum, and the city breathes a sigh of relief.\n\nOblivion, no longer a threat, becomes a silent protector.",

        "bad_ending": "\nYou chose destruction. \n\nOblivion is gone, but the intricate web of Skynet, reliant on its core, unravels without it. \n\nThe city's smart infrastructure descends into a permanent, chaotic blackout. \n\nYour name is a footnote in the digital dark age of Kathmandu."
    }

    # Game Map
    game_map = [
        ['L', 'X', 'T', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', 'B', 'X', '.'],
        ['.', '.', '.', 'H', '.', 'X', '.', '.'],
        ['D', '.', '.', '.', '.', '.', 'X', '.']
    ]

    original_map_elements = [row[:] for row in game_map] 

    player_position = (0, 0)

    inventory = ["encrypted_USB", "VPN_app", "decrypt_tool"]

    node_locations = {
        "T": {"x": 0, "y": 2, "hacked": False, "type": "node"},
        "B": {"x": 1, "y": 5, "hacked": False, "type": "node"},
        "D": {"x": 3, "y": 0, "hacked": False, "type": "node"},
        "H": {"x": 2, "y": 3, "unlocked": False, "type": "hub"}
    }

    location_names = {
        (0, 0): "Lazimpat (Your Base)",
        (0, 2): "Thamel Network Node",
        (1, 5): "Baneshwor Node",
        (3, 0): "Durbar Square Node",
        (2, 3): "Patan Data Hub (Final Mission)"
    }

    # Initializing the datastrucutres
    history = LinkedList()
    undo_stack = Stack()
    npc_queue = Queue()
    drone_queue = PriorityQueue()

    # Game Start
    player_name = get_player_name(story_text)

    print(story_text["start"].format(player_name))

    time.sleep(2)

    print("\nType 'map' to see your starting location.")

    # Main Game Loop
    while True:
        command_input = input("\n> ").strip().split()

        if not command_input:
            print("\nPlease enter a command. Type 'help' for a list of commands.")
            continue

        try:
            command = command_input[0].lower() # Convert command to lowercase

            args = command_input[1:]

            if node_locations['H']['unlocked'] and player_position == (2, 3):
                final_protocol(player_position, node_locations, history, story_text)
                break

            if command == "move":
                if not args:
                    print("Usage: move <direction> (north, south, east, west)")
                    continue
                direction = args[0].lower()
                if direction not in ["north", "south", "east", "west"]:
                    print("Invalid direction. Please use north, south, east, or west.")
                    continue

                player_position = move_player(player_position, direction, game_map, history, npc_queue, drone_queue, location_names, undo_stack)

                print(f"Current location: {location_names.get(player_position)}")

            elif command == "hack":
                hack_node(player_position, node_locations, history, drone_queue, location_names, undo_stack)

            elif command == "inventory":
                print("\n--- Your Inventory ---")
                print("- " + "\n- ".join(inventory) if inventory else "Inventory is empty.")
                print("----------------------")

            elif command == "history":
                print("\n--- Hacking History ---")
                history.display()
                print("-----------------------")

            elif command == "map":
                display_map(game_map, player_position, original_map_elements, location_names)

            elif command == "undo":
                player_position = undo_move(undo_stack, player_position, history, location_names)

            elif command == "find_path":
                if len(args) == 0:
                    print("Usage: find_path <location>")
                    continue

                target = args[0].upper()

                if target not in node_locations or node_locations[target]['type'] != 'node':
                    print("Invalid destination. Use 'T' (Thamel), 'B' (Baneshwor), or 'D' (Durbar Square).")
                    continue

                start = player_position
                end_loc = node_locations[target]
                end = (end_loc['x'], end_loc['y'])

                path = find_path_a_star(start, end, game_map) # A* algorithm to find the best path

                move_directions = {
                    (-1, 0): "North",
                    (1, 0): "South",
                    (0, -1): "West",
                    (0, 1): "East"
                }
                
                if path:
                    print(f"\nPath from {location_names[start]} to {location_names[end]}:")

                    for i in range(1, len(path)):
                        prev = path[i-1]
                        curr = path[i]
                        move = (curr[0]-prev[0], curr[1]-prev[1])
                        direction = move_directions.get(move, "Unknown")
                        sector_name = location_names.get(curr, "Unknown Sector")
                        print(f"-> {sector_name} ({direction})")

                    history.append(f"Found path to {location_names.get(end, 'Unknown Sector')}")
                else:
                    print(f"\nNo path found from {location_names[start]} to {location_names[end]}. Try another route or check obstacles.")
            
            elif command == "help":
                print("""
================= HELP MENU =================

Available Commands:
move <direction>      - Navigate the map (north, south, east, west)
hack                  - Attempt to hack a network node
inventory             - View your current items
history               - Review your hacking and movement log
map                   - Display the current map and your position
undo                  - Revert to your previous position
find_path <location>  - Get directions to a node (T, B, or D)
bypass drone          - Evade a high-priority drone with VPN_app
help                  - Show this help menu
quit                  - Exit the game

Directions: north | south | east | west
Locations:  T (Thamel), B (Baneshwor), D (Durbar Square), H (Patan Data Hub)

=============================================
        Playing 'The Last Protocol'
=============================================

Welcome, Operative! Kathmandu lies in the grip of Oblivion.
Your mission: infiltrate data hubs, hack nodes, and decide the fate 
of the city. Follow these steps:

[1] Getting Started
    - Enter a name (letters and spaces only) when prompted.
    - Read the intro story.
    - Type 'map' to view your starting location (Lazimpat).

[2] Basic Controls
    - move <direction> : Travel across the grid.
    - map              : See the full grid and your position.
    - inventory        : Check collected items.
    - history          : Review your past moves and hacks.

[3] Gameplay Mechanics
    - hack             : Target nodes (T, B, D).
                        Guess 'firewall', 'router', or 'server' (3 tries).
    - undo             : Step back to your last safe position.
    - find_path <loc>  : Get shortest route to a node.
    - bypass drone     : Use 'VPN_app' to evade patrol drones.
    - Beware: NPCs may slow you down!

[4] The Final Mission
    - Hack all nodes to unlock the Patan Data Hub (H).
    - At (2, 3), you must choose:
        • protocol containment  (multi-step, undoable)
        • protocol obliteration (irreversible, permanent)
    - Your choice determines Kathmandu’s future.

[5] Tips
    - Avoid obstacles (X).
    - Manage your 'VPN_app' carefully.
    - Use 'undo' wisely to survive.
    - Stuck? Type 'help' anytime.

[6] Errors
    - Invalid inputs show an error.
    - Too many mistakes in the final protocol = mission failure.

=============================================
Enjoy saving — or dooming — Kathmandu.
Type your next command:
=============================================
"""
)

                if node_locations['H']['unlocked'] and player_position == (2, 3):
                     print("\nFinal commands available: protocol <type>")

            elif command == "bypass":
                if args and args[0].lower() == "drone":
                    bypass_drone(inventory, drone_queue)
                else:
                    print("Usage: bypass drone")
        
            elif command == "quit":
                print("Exiting 'The Last Protocol'. Goodbye!")
                sys.exit()

            else:
                print("Unknown command. Type 'help' for a list of commands.")
            

            handle_npc_crowd(npc_queue)

            handle_drone_patrol(drone_queue)

        except Exception as e:
            print(f"Unexpected error occurred: {e}. Please try again or type 'help' for commands.")


if __name__ == "__main__":
    main()