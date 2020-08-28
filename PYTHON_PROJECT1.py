##
# Joe Moon
# RPG Game: Zombie Eviction
# Added Features: 
#   - Zombie combat system: A player can engage and disengage at will
#   - Expanded inventory set: Items either give a damage multiplier or heal
#   - Expanded gameplay environment: 9 rooms 
#   - Available actions guide: Navigable direction display, action menu

from random import randint

def showInstructions():
    print("="* 40)
    print("Welcome to ZOMBIE EVICTION!")
    print("Zombies have overrun your house!  Use items to take them out!")
    print("="* 40)
    print("Commands:")
    print("'go [direction]' = moves you to the next room if possible")
    print("'get [item]' = picks up an item while loosing an exisitng one")
    print("'fight' = use item to fight a zombie")
    print("WIN CONDITION: Kill all zombies...")

def showStatus():
    #print the player's current status
    print()
    print("-" * 10, "PLAYER STATUS", "-" * 10)
    print("Hitpoints : " + str(health))                  # Health meter
    print("Location  : " + rooms[currentRoom]["name"])   # Location
    print("There are " + str(zombieCount) + " zombies remaining") # Z counter
    print("Inventory : " + str(inventory))               # Current Inventory
    
    # --- AVAILABLE ACTIONS GUIDE ---
    # print an item if there is one
    if "item" in rooms[currentRoom] and rooms[currentRoom]["item"]["use"] == 1:
        print("You can 'get' the item: " + rooms[currentRoom]["item"]["name"])
    
    # movement guide
    possibleDirection = ["north", "south", "east", "west", "end"]
    i = 0
    while possibleDirection [i] != "end":   # checks if directions are available
        if possibleDirection[i] in rooms[currentRoom]:
            print("You can 'go': "+ possibleDirection[i])
        i += 1
    
    # presents option to fight a zombie if it exists
    if rooms[currentRoom]["zombie"]["count"] > 0:
        print("You can 'fight' the zombie!")
    
    print("-" * 35)

# Room attributes
# A nested dictionary is used to give attributes to items and zombies
# Item attribute key: damage = multiplier from weapon; use = only pick up once
# Zombie attribute key: count = number of zombies in room; hp = hit points
rooms = {
            1 : {  "name"  : "Entrance" ,
                   "north" : 2,
                   "west" : 9,
                   "item" : {"name" : "umbrella" , "damage" : 1, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30}
                }  ,

            2 : {  "name"  : "Corridor" ,
                   "north" : 3,
                   "east" : 5,
                   "west"  : 8,
                   "south" : 1,
                   "item"  : {"name" : "chair", "damage" : 1.5, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                }  ,            

            3 : {  "name"  : "Stairs" ,
                   "east" : 4,
                   "west" : 7,
                   "south" : 2,
                   "item" : {"name" : "rod" , "damage" : 2, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30}  
                } ,

            4 : {  "name"  : "Living Room" ,
                   "west" : 3,
                   "item" : {"name" : "sword" , "damage" : 4, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                } ,
            
            5 : {  "name"  : "Dinning Room" ,
                   "west" : 2,
                   "south" : 6,
                   "item" : {"name" : "vase" , "damage" : 1.25, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                } ,
            
            6 : {  "name"  : "Kitchen" ,
                   "north" : 5,
                   "item" : {"name" : "sandwich" , "heal" : 25, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                } ,
            
            7 : {  "name"  : "Bedroom" ,
                   "east" : 3,
                   "item" : {"name" : "pillow" , "damage" : 0.1, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                } ,
            
            8 : {  "name"  : "Bathroom" ,
                   "east" : 2,
                   "item" : {"name" : "medkit" , "heal" : 40, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                } ,
            
            9 : {  "name"  : "Garage" ,
                   "east" : 1,
                   "item" : {"name" : "crowbar" , "damage" : 2.5, "use" : 1},
                   "zombie" : {"count" : 1 , "hp" : 30} 
                } ,
         }


# Starting Conditions
currentRoom = 1         # Start the player in room 1
health = 100            # Player's starting health level
zombieCount = 9         # One zombie per room
inventory = []          # The player's inventory, which is initially empty
weaponOutput = 0        # Damage multiper from weapon
combat = "n"            # Default combat engagement option

showInstructions()      # Display game instructions

# continue the game while the player is alive or there are still zombies
while health > 0 and zombieCount > 0:
    showStatus()        # Status update

    #get the player's next 'move'
    #.split() breaks it up into an list array
    #eg typing 'go east' would give the list:
    #['go','east']
    move = input("What do you want to do? > ").lower().split()

    # Command 'go'
    if move[0] == "go":
        #check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            #set the current room to the new room
            currentRoom = rooms[currentRoom][move[1]]
        #there is no door (link) to the new room
        else:
            print("You can't go that way!")

    # Command 'get'
    if move[0] == "get" :
        #if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]["item"]["name"] and rooms[currentRoom]["item"]["use"] == 1:
            if rooms[currentRoom]["item"]["name"] == "medkit" or rooms[currentRoom]["item"]["name"] == "sandwich":
                health += rooms[currentRoom]["item"]["heal"]    # healing item
                rooms[currentRoom]["item"]["use"] = 0           # make item unavailable
                print("You used a " + rooms[currentRoom]["item"]["name"] + " and healed yourself.")
            else:
                inventory = [move[1]]  # add the item to their inventory
                weaponOutput = rooms[currentRoom]["item"]["damage"] # Assign damage multiplier
                print("You picked up a " + move[1] + "!")    # user notification
                rooms[currentRoom]["item"]["use"] = 0       # make item unavailable
        #otherwise, if the item isn't there to get
        else:
            #tell them they can't get it
            print("Can't get " + move[1] + "!")

    # Command 'fight'
    if move[0] == "fight" :
        combat = "y"            # Player initiates combat
        if len(inventory) == 0:
            print("Get a weapon first!")
        elif rooms[currentRoom]["zombie"]["count"] == 0:
            print("There are no zombies to fight here.  Move on.")
        else:
            while combat == "y" and health > 0:
                playerDamage = randint(1,11) * weaponOutput
                zombieDamage = randint(1,20)

                print()
                print("*** You are fighting a zombie! ***")
                print("You used your " + inventory[0] + " and caused " +
                      str(playerDamage) + " damage to the zombie.")
                rooms[currentRoom]["zombie"]["hp"] -= playerDamage
                if rooms[currentRoom]["zombie"]["hp"] > 0:
                    print("The zombie counter-attacked and caused " +
                          str(zombieDamage) + " damage to you!")
                    health -= zombieDamage
                    
                    if health < 0:      # Player is dead, will exit loop
                        health = 0      # for visual effects
                   
                    print("Hitpoints: " + str(health))
                   
                    if health > 0:      # Player is still alive
                        combat = input("Do you still want to fight? [y/n] ").lower()                
                else:
                    print("Good job.  You killed the zombie!")
                    rooms[currentRoom]["zombie"]["count"] = 0
                    zombieCount -= 1
                    combat = "n"

            
# End game conditions
print()
if health < 1:          # Lose condition
    print("The zombie killed you and you've joined their ranks.")
    print("Game Over.")
else:                       # Win condition
    print("Nice one!  You've overcome the undead!  Time for a beer!")