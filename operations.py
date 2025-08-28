import random, re
from data_structures import LinkedList, Stack, Queue, PriorityQueue

def get_player_name(story_text):
    """
    Prompt the player for a valid name (only letters and spaces).
    Keeps asking until valid input is given.
    """
    while True:
        player_name_input = input(story_text["intro"] + " ")
        if re.fullmatch(r'[A-Za-z\s]+', player_name_input.strip()):
            return player_name_input.strip()
        else:
            print("Invalid name. Name must contain only alphabetic characters and spaces. Please try again.")


def display_map(game_map, player_position, original_map_elements, location_names):
    """
    Display the game map
    A 2-D list is used to model a grid based layout for making positional logic.
    """

    # Top Header Box
    print("\n" + "-"*40)
    print("|{:^38}|".format("▲ North"))
    print("-"*40)
    print("|{:^38}|".format("Kathmandu - The Last Protocol"))

    # Location display
    location_display = location_names.get(player_position, "Unknown Sector")
    print("|    Location: {:<24}|".format(location_display))
    print("-"*40)

    # Map Grid Box
    for i in range(len(game_map)):
        row_display = "| "
        for j in range(len(game_map[i])):
            if (i,j) == player_position:
                row_display += "*  "
            else:
                row_display += f"{original_map_elements[i][j]}  "
        row_display = row_display.rstrip() + " |"
        print(row_display)
    print("-"*40)

    # Map Legend Box
    print("\n" + "-"*40)
    print("|{:^38}|".format("--- Map Legend ---"))
    legend_items = [
        "[*]: Your Position",
        "[L]: Lazimpat (Your Base)",
        "[T]: Thamel Network Node",
        "[B]: Baneshwor Node",
        "[D]: Durbar Square Node",
        "[H]: Patan Data Hub (Final Mission)",
        "[X]: Obstacle",
        "[.]: Empty"
    ]

    for item in legend_items:
        print("| {:<37}|".format(item))
    print("-"*40)


def move_player(player_position, direction, map, history, npc_queue, drone_queue, location_names, undo_stack):
    """
    Moves the player, updates the undo stack, and handles boundary/obstacle checks.
    """
    x, y = player_position
    new_x, new_y = x, y 

    if direction == "north":
        new_x -= 1
    elif direction == "south":
        new_x += 1
    elif direction == "east":
        new_y += 1
    elif direction == "west":
        new_y -= 1
    else:
        print("\nInvalid Direction.\nUse north, south, east, or west.")
        return player_position
    
    if new_x < 0 or new_x >= len(map) or new_y < 0 or new_y >= len(map[0]):
        print("\nYou cannot move outside the city limits")
        return player_position
    
    if map[new_x][new_y] == "X":
        print("\n!!! An obstacle blocks you path.!!!\nFind another way")
        return player_position

    if not npc_queue.is_empty():
        print(f"\nA wave of {npc_queue.dequeue()} slows your movement momentarily")

    handle_drone_patrol(drone_queue)

    undo_stack.push(player_position)

    history.append(f"Moved {direction} to {location_names.get((new_x, new_y), 'Unkown Sector')}")
    return (new_x, new_y)


def recursive_network_penetration(attempts_left):
    """
    Simulates a recursive hacking mini-game by guessing the answer.
    Recursion is used to model the repeated probing of network connections in a branching, tree-like fashion.
    """
    if attempts_left == 0:
        print("!!! Network Penetration Failed !!!\n Max Attempt reached")
        return False 
    
    print(f"\n--- Hacking Protocol ---\n Attempts Left: {attempts_left}")
    print("Trace the network connection.\nEnter 'firewall', 'router' or 'server' to hack the system.")
    correct_path = random.choice(['firewall', 'server', 'router'])
    user_input = input("> ").lower().strip()  # Added strip for better input handling

    if user_input == correct_path:
        print("Correct Path Found! Access Granted")
        return True 
    else:
        print("!!!Incorrect Path!!! \nRetrying.....")
        return recursive_network_penetration(attempts_left - 1)


def hack_node(player_position, node_locations, history, drone_queue, location_names, undo_stack):
    """
    Handles the hacking process of the network node.
    """
    node_id = None 

    for key, loc in node_locations.items():
        if (loc['x'], loc['y']) == player_position and loc['type'] == 'node':
            node_id = key
            break 

    
    if not node_id:
        print("You are not at a hackable network node.")
        return 
    
    if node_locations[node_id]['hacked']:
        print("This node is already hacked")
        return 
    
    undo_stack.push(player_position)

    print(f"Initiating hack on {location_names.get(player_position)} ...")
    hack_success = recursive_network_penetration(3)

    if hack_success:
        node_locations[node_id]['hacked'] = True
        print(f"Node {location_names.get(player_position)} successfully hacked! \nOblivion's control weakens.")
        history.append(f"Hacked {location_names.get(player_position)}")

        if all(node_locations[n]['hacked'] for n in ['T', 'B', 'D']):
            node_locations['H']['unlocked'] = True
            print("All network nodes breached. The Patan Data Hub is now accessible!")
    else:
        print("Hack failed. Oblivion's defenses are strong. A security alert is triggered!")
        history.append(f"Failed hack attempt at {location_names.get(player_position)}")
        drone_queue.enqueue("Kumari Protocol Drone", 1)  # Enqueue only if space available (handled in class)
        handle_drone_patrol(drone_queue)


def undo_move(undo_stack, player_position, history, location_names):
    """
    Reverts the player to previous postion using the undo stack.
    """

    if undo_stack.is_empty():
        print("You cannot do undo. There are no previous moves to revert to.")
        return player_position
    
    previous_position = undo_stack.pop()

    print(f"Reverting to previous location: {location_names.get(previous_position, 'Unknown Sector')}")

    history.append(f"Undid a move, reverting to {location_names.get(previous_position, 'Unknown Sector')}")
  
    return previous_position


def handle_npc_crowd(npc_queue):
    """
    Add NPCs to the queue to slow down the player.
    """

    if random.randint(1, 3) == 1:
        crowd_type = random.choice(["commuters rushing to work", 
                                    "delivery drones crisscrossing the sky", 
                                    "tourists taking selfies"])
        npc_queue.enqueue(crowd_type)


def handle_drone_patrol(drone_queue):
    """
    Manages high-priority drone threats.
    """
    if not drone_queue.is_empty():
        threat = drone_queue.peek()
        if threat == "Kumari Protocol Drone":
            print("\n!!! A high-priority Kumari Protocol Drone is actively pursuing you! Type 'bypass drone' if you have the right tool!")
        else:
            print(f"You encounter a {drone_queue.dequeue()}. You manage to slip past.")


def bypass_drone(inventory, drone_queue):
    """
    Allows player to bypass a high-priority done using a specific item
    """

    if not drone_queue.is_empty() and drone_queue.peek() == "Kumari Protocol Drone":
        if "VPN_app" in inventory:
            inventory.remove("VPN_app")
            drone_queue.dequeue()
            print("You successfully deployed your VPN app and bypassed the Kumari Protocol Drone!")
            return True
        else:
            print("You need a 'VPN_app' in your inventory to bypass the drone.")
            return False
        
    else:
        print("No high priority drone to bypass at the moment")


def trigger_ending(end_type, history, story_text):
    """
    Triggers and displays the final ending.
    """
    if end_type == "good":
        print("\n--- GOOD ENDING: The Digital Guardian ---")
        print(story_text['good_ending'])
        print("\nFinal history log:")
        history.display()
        print("Game Over.")
    elif end_type == "bad":
        print("\n--- BAD ENDING: The Digital Collapse ---")
        print(story_text['bad_ending'])
        print("\nFinal history log:")
        history.display()
        print("Game Over.")


def final_protocol(player_position, node_locations, history, story_text):
    """
    Manages the final choice of the game and lead to an end.
    """
    print(story_text["final_protocol_start"])

    invalid_count = 0  # Added to prevent infinite invalid inputs
    max_invalid = 5

    while True:
        if invalid_count >= max_invalid:
            print("Too many invalid commands. Protocol failed due to errors.")
            trigger_ending("bad", history, story_text)
            return

        final_cmd = input("> ").lower().strip().split()
        
        if not final_cmd:
            invalid_count += 1
            print("Invalid input. Please enter a command.")
            continue

        cmd = final_cmd[0]
        args = final_cmd[1:]

        if cmd == "protocol":
            if not args:
                invalid_count += 1
                print("Usage: protocol <type> (containment or obliteration)")
                continue
        
            protocol_type = args[0]
            if protocol_type == "containment":
                print("\nInitiating Containment Protocol...")

                protocol_steps = Stack()
                protocol_steps.push("Step 3: Upload containment protocol")
                protocol_steps.push("Step 2: Deploy isolation code")
                protocol_steps.push("Step 1: Secure access points")

                print("Protocol steps loaded. Enter 'next' to proceed, or 'undo' to revert.")

                step_invalid_count = 0  # Added for inner loop safety
                max_step_invalid = 5

                while not protocol_steps.is_empty():
                    if step_invalid_count >= max_step_invalid:
                        print("Too many errors in protocol steps. Protocol failed.")
                        trigger_ending("bad", history, story_text)
                        return

                    print(f"Current step: {protocol_steps.peek()}")

                    action = input("> ").lower().strip()

                    if action == "next":
                        history.append(f"Completed step: {protocol_steps.pop()}")
                        print("Step complete.")
                    elif action == "undo":
                        if protocol_steps.peek() == "Step 3: Upload containment protocol":
                            print("This is the final step. You can't undo it. It's now or never.")
                            print("You must enter 'next' to proceed, otherwise the protocol fails.")
                        else:
                            if protocol_steps.is_empty():  # Extra check
                                print("No steps to undo.")
                                continue
                            reverted_step = protocol_steps.pop()
                            print(f"Undoing step: {reverted_step}")
                            history.append(f"Undid step: {reverted_step}")
                            print("Reverted to previous step.")
                    else:
                        step_invalid_count += 1
                        print("Invalid command. Use 'next' or 'undo'.")
                
                trigger_ending("good", history, story_text)
                return

            elif protocol_type == "obliteration":
                print("\nInitiating Obliteration Protocol...")
                print("WARNING: This action is irreversible. There is no undo for Obliteration.")
                confirm = input("Confirm (yes/no): ").lower().strip()

                if confirm == "yes":
                    trigger_ending("bad", history, story_text)
                else:
                    print("Obliteration Protocol cancelled.")
                return
            else:
                invalid_count += 1
                print("Invalid protocol type. Use 'containment' or 'obliteration'.")
        else:
            invalid_count += 1
            print("Invalid command. You must choose a protocol or ask for help.")


def find_path_a_star(start_position, end_position, map):
    """
    Finds the shortest path from start_pos to end_pos using the A* search algorithm.
    """

    class Node:
        def __init__(self, parent=None, position=None):
            self.parent = parent
            self.position = position
            self.g = 0  # Cost from start to current node
            self.h = 0  # Heuristic (estimated cost from current to end)
            self.f = 0  # Total cost (g + h)

        def __eq__(self, other):
            return self.position == other.position

        def __repr__(self):
            return f"Node(pos={self.position}, f={self.f})"
        
    
    def heuristic(a, b):
        """
        Manhattan distance heuristic.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    start_node = Node(None, start_position)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end_position)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []

    open_list.append(start_node)

    max_iterations = 100  # Added to prevent infinite loop in large maps
    iteration = 0

    while len(open_list) > 0 and iteration < max_iterations:
        iteration += 1
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if node_position[0] > (len(map) - 1) or node_position[0] < 0 or node_position[1] > (len(map[0]) - 1) or node_position[1] < 0:
                continue

            if map[node_position[0]][node_position[1]] == 'X':
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)

        for child in children:
            if child in closed_list:
                continue

            child.g = current_node.g + 1
            child.h = heuristic(child.position, end_node.position)
            child.f = child.g + child.h

            if any(open_node for open_node in open_list if child == open_node and child.g >= open_node.g):
                continue

            open_list.append(child)
    
    return None