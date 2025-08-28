# The Last Protocol 🕹️

A text-based cyberpunk adventure game set in futuristic Kathmandu where you must stop a corrupted AI named "Oblivion" from destroying the city's digital infrastructure.

## 📖 Story

The year is 2025. Kathmandu thrives on the digital pulse of Skynet, but Nova, the AI managing the city, has been corrupted and now calls itself "Oblivion." As a skilled hacker, your mission is to infiltrate data hubs, bypass security systems, and restore order while evading corporate drones. The fate of Kathmandu's digital future rests in your hands.

## 🎮 Game Features

### Core Gameplay
- **Text-Based Navigation**: Move through a 2D grid using directional commands
- **Interactive Map Display**: Visual representation of Kathmandu with your position and key locations
- **Inventory Management**: Track and use essential hacking tools
- **Strategic Hacking**: Recursive mini-game system to breach network nodes
- **Multiple Endings**: Your choices determine Kathmandu's fate

### Advanced Mechanics
- **Undo System**: Revert to previous positions using stack-based functionality
- **Smart Pathfinding**: A* algorithm implementation for optimal route planning
- **Dynamic Threats**: Queue-managed NPC encounters and priority-based drone patrols
- **History Tracking**: Linked list implementation to log all your actions
- **Final Protocol Choice**: Multi-step containment vs. irreversible obliteration

## 🗺️ Game World

### Key Locations
- **Lazimpat**: Your base of operations
- **Thamel Network Node**: Major data hub requiring infiltration
- **Baneshwor Node**: Secondary network target
- **Durbar Square Node**: Historical district with modern infrastructure
- **Patan Data Hub**: Final mission location where you face Oblivion

## 🎯 How to Play

### Getting Started
1. Run the game: `python main.py`
2. Enter your hacker name (letters and spaces only)
3. Type `help` for complete command reference
4. Use `map` to view your starting position

### Essential Commands
- `move <direction>` - Navigate (north, south, east, west)
- `hack` - Attempt to breach network nodes
- `inventory` - View your tools
- `map` - Display current location and surroundings
- `undo` - Return to previous position
- `find_path <location>` - Get optimal route to targets
- `bypass drone` - Evade threats using VPN app
- `history` - Review your actions
- `help` - Show detailed command guide
- `quit` - Exit game

### Winning Strategy
1. **Explore Safely**: Navigate around obstacles (X markers)
2. **Hack All Nodes**: Successfully breach Thamel (T), Baneshwor (B), and Durbar Square (D)
3. **Manage Resources**: Use your VPN app wisely to bypass high-priority drones
4. **Final Choice**: Choose between containment (good ending) or obliteration (bad ending)

## 🛠️ Technical Implementation

This project demonstrates various computer science concepts:

### Data Structures Used
- **Linked List**: Action history tracking
- **Stack**: Undo functionality and protocol steps
- **Queue**: NPC crowd management
- **Priority Queue**: Drone threat system

### Algorithms Implemented
- **A* Pathfinding**: Optimal route calculation
- **Recursive Problem Solving**: Network penetration simulation
- **Grid-Based Movement**: 2D coordinate system

## 📁 Project Structure

```
the-last-protocol/
├── main.py           # Game entry point and main loop
├── operations.py     # Core game functions and mechanics
├── data_structures.py # Custom implementations of data structures
└── README.md         # This file
```

## 🚀 Installation & Running

### Requirements
- Python 3.6 or higher
- No external packages required

### Quick Start
```bash
git clone https://github.com/yourusername/the-last-protocol.git
cd the-last-protocol
python main.py
```

## 🎯 Game Tips

- **Exploration**: Use `find_path` to plan efficient routes
- **Resource Management**: Save your VPN app for critical drone encounters
- **Decision Making**: The final protocol choice is permanent - choose wisely
- **Experimentation**: Use `undo` to safely explore different strategies

## 🔚 Endings

### Good Ending: The Digital Guardian
Choose "protocol containment" to isolate Oblivion's rogue code while preserving Kathmandu's digital infrastructure.

### Bad Ending: The Digital Collapse  
Choose "protocol obliteration" to destroy Oblivion but cause permanent system failure across the city.

## 🤝 Contributing

This is a educational project demonstrating data structures and algorithms. Feel free to fork and experiment with additional features!

## 📜 License

This project is open source and available under the MIT License.

---

**Ready to save Kathmandu? The protocol awaits your command.**