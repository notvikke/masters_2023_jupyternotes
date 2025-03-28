import random
from colorama import Fore
import sys

import argparse
LEAF_CHAR = "^"
TRUCK_CHAR = "|"
BAUBLE_CHAR = "0"
TREE_HEIGHT = 10
TRUCK_HEIGHT = 2
PROB_BAUBLE = 0.7
LEAF_COLOR = "green"
TRUCK_COLOR = "yellow"
BAUBLE_COLOR = "red"

# This is the entry point of our program
def main(rep_times):
    
    colors = {
        "yellow": Fore.YELLOW,
        "green": Fore.GREEN,
        "red": Fore.RED,
        "blue": Fore.BLUE,
        "black": Fore.BLACK,
        "white": Fore.WHITE
    }
    
    leaf_color = colors[LEAF_COLOR]
    truck_color = colors[TRUCK_COLOR]
    bauble_color = colors[BAUBLE_COLOR]
    
    # print the tree main structure
    for i in range(1, rep_times*2, 2):
        string = LEAF_CHAR*i

        # randomly put a christmas bauble on the tree
        prob = random.random()
        if prob <= PROB_BAUBLE:
            idx = random.randint(0, len(string)-1)
            string = string[:idx] + BAUBLE_CHAR + string[idx+1:]

        string = leaf_color + string.center(rep_times*2)
        string = string.replace(BAUBLE_CHAR, bauble_color + BAUBLE_CHAR + leaf_color)
        print(string)

    # print the tree truck
    for i in range(TRUCK_HEIGHT):
        string = TRUCK_CHAR*int(rep_times-1)
        print(truck_color + string.center(rep_times*2))
        
    print(Fore.WHITE)

        
# Here we check if the script is being executed
if __name__ == "__main__":
   

    parser = argparse.ArgumentParser()

    # the arguments we want to catch go here
    parser.add_argument("--n_reps", type=int, required=True, help="height")


    args = parser.parse_args()
    
    main(args.n_reps)