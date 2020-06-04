from room import Room
from player import Player
from colors import print_color
from item import Item
import time


# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':  Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow': Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),

    'library': Room("Library", """The room appears a mess. As though someone left
in a hurry. Are they trying to hide something?""", False)
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['foyer'].w_to = room['library']
room['library'].e_to = room['foyer']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Items
#

# Library - Room west to the Foyer (initially locked)
# key - Item found in Foyer - will unlock the library
# library will house 3 books
# Book - inherits from Item
# "read" i.e. collect all three books to access pieces of a password
# complete password will unlock "Treasure"

items = {
    'key': Item("key", "A heavy, bronze key.")
}

# add the items to the rooms

room['foyer'].items = [items['key']]

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

player_name = input("What's your name? ")

player = Player(player_name, room['outside'])

print(f'\nWelcome {player.name}!')

print_color('cyan', f'\nWelcome {player.name}!\n\n')

# time.sleep(0.5)


def location_print(color):
    print_color(
        color, f'\033[1m\n\nYour location: {player.current_room.name}\33[00m')
    print_color(color, f'{player.current_room.description} \n')
    # time.sleep(0.5)


while True:
    if player.current_room == room['outside']:
        location_print('green')
    elif player.current_room == room['foyer']:
        location_print('purple')
    elif player.current_room == room['library']:
        # make some if/else statment depending on if the player has a key in their inventory.
        print(f'This room is locked')
        player.current_room == room['foyer']
    elif player.current_room == room['overlook']:
        location_print('light_purple')
    elif player.current_room == room['narrow']:
        location_print('light_grey')
    elif player.current_room == room['treasure']:
        location_print('yellow')

    player_move = input(
        """Move commands: (n, s, e, w)
    Check your inventory: 'i'
    Look around the room: 'l'
    Get item: 'get <item name>'
    Press 'q' to quit.\n\n""").lower()

    if player_move in ['n', 's', 'e', 'w']:
        player.move(player_move)
    # prints the player's inventory
    elif player_move == 'i':
        if len(player.inventory) > 0:
            for item in player.inventory:
                print_color('yellow', '\n\nInventory:')
                print_color('yellow', f'{item.name}')
        else:
            print_color('red', '\n\nNo items in your inventory')
    # prints a list of items in the room
    elif player_move == 'l':
        # loop over them items and print them out!
        if len(player.current_room.items) > 0:
            print_color('green', '\n\nThis room contains:')
            for item in player.current_room.items:
                print(f'{item.name}')
        # if no items are present in the room
        else:
            print_color('red', 'This room has nothing in it.')
    # get the item from the room into the player's inventory
    elif player_move.startswith('get'):
        query = player_move.split()
        # if the specified item is in the room, put in player inventory
        if len(player.current_room.items) > 0 and player.current_room.has_item(item):
            player.grab_item(items[item])
        # if the specified item is not in the room, print this
        else:
            print_color('red', f'This room does not contain item {query[1]}')
    # quits the game
    elif player_move == 'q':
        exit()
    else:
        print_color('red', '\n\n\nInvalid input. Please try again.\n\n')
