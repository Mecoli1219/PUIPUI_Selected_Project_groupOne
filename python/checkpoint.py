from node import *
import maze as mz
import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os

def main():
    point = score.Scoreboard("data/UID.csv", "team_NTUEE")
    interf = interface.interface()
    # TODO : Initializ1e necessary variables

    print("Mode 0: for checkpoint")
    direction = 2 #input("Enter the initial direction:(1,2,3,4)")
    in_node = 1
    interf.send_action(mz.Action(1))
    while(in_node < 13):
        command = interf.get_command()
        if command == "n":
            if in_node == 1 or in_node == 2 or in_node == 3:
                interf.send_action(mz.Action(1))
                in_node += 1
            elif in_node == 4:
                interf.send_action(mz.Action(3))
                in_node += 1
            elif in_node == 5:
                interf.send_action(mz.Action(2))
                in_node += 1
            elif in_node == 6:
                interf.send_action(mz.Action(1))
                in_node += 1
            elif in_node == 7:
                interf.send_action(mz.Action(3))
                in_node += 1
            elif in_node == 8:
                interf.send_action(mz.Action(4))
                in_node += 1
            elif in_node == 9:
                interf.send_action(mz.Action(3))
                in_node += 1  
            elif in_node == 10:
                interf.send_action(mz.Action(2))
                in_node += 1
            elif in_node == 11:
                interf.send_action(mz.Action(1))
                in_node += 1
            elif in_node == 12:
                interf.send_action(mz.Action(5))
                in_node += 1      
            print(in_node)
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible
        

    interf.end_process()

if __name__ == '__main__':
    main()
