from node import *
import maze as mz
import score1 as score
# import score
import interface
import time

import numpy as np
import pandas
import time
import sys
import os


def main():
    maze = mz.Maze("data/final_map_109.csv")  # final_map_109
    interf = interface.interface()
    point = score.Scoreboard("data/UID.csv", "換隊員啦")
    # TODO : Initializ1e necessary variables

    if (sys.argv[1] == '0'):
        print("Mode 0: for treasure-hunting")
        direction = "2"  # input("Enter the initial direction:(1,2,3,4)")
        route = ['1', '2', '7', '6', '13', '6', '7', '14', '15', '8', '15', '16', '17', '24', '17', '18', '11', '12', '5', '4', '5', '12', '11', '18', '19', '18', '25', '26',
                 '38', '37', '43', '44', '43', '42', '41', '42', '35', '30', '31', '32', '31', '36', '31', '30', '29', '28', '27', '20', '27', '39', '40', '33']  # maze.strategy("1")
        print(route)
        start = 0
        action = maze.getAction(direction, route[start], route[start + 1])
        interf.send_action(action)
        direction = str(
            int(maze.nd_dict[route[start]].getDirection(route[start + 1])))
        start += 1

        while(start < (len(route)-1)):
            command = interf.get_command()
            print(command)
            if command == "n":
                action = maze.getAction(
                    direction, route[start], route[start + 1])
                interf.send_action(action)
                if action == mz.Action(2):
                    uidcode = interf.get_UID(1)
                    print(uidcode)
                    try:
                        point.add_UID(str(uidcode[2:]))
                    except:
                        pass
                    print(point.getCurrentScore())
                direction = str(
                    int(maze.nd_dict[route[start]].getDirection(route[start + 1])))
                start += 1

#            if uidcode != 0:
                # point.add_UID(str(uidcode))
                # print(point.getCurrentScore())
 #               print(uidcode)
  #              point.add_UID(str(uidcode))
   #             print(point.getCurrentScore())

        command = interf.get_command()
        interf.send_action(mz.Action(5))

        print(route)
        # TODO : for treasure-hunting, which encourages you to hunt as many scores as possible

    elif (sys.argv[1] == '1'):
        # TODO: You can write your code to test specific function.
        print("Mode 1: for checkpoint")
        direction = "2"  # input("Enter the initial direction:(1,2,3,4)")
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
                    uidcode = interf.get_UID()
                    print(uidcode)
                    point.add_UID(str(uidcode))
                    print(point.getCurrentScore())
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
                    uidcode = interf.get_UID()
                    print(uidcode)
                    point.add_UID(str(uidcode))
                    print(point.getCurrentScore())
                elif in_node == 11:
                    interf.send_action(mz.Action(1))
                    in_node += 1
                elif in_node == 12:
                    interf.send_action(mz.Action(5))
                    in_node += 1
                print(in_node)
        command = interf.get_command()
        interf.send_action(mz.Action(5))

    elif (sys.argv[1] == '2'):
        # TODO: You can write your code to test specific function.
        print("Mode 2: for checkpoint with backward")
        direction = "2"  # input("Enter the initial direction:(1,2,3,4)")
        in_node = 1
        interf.send_action(mz.Action(1))
        while(in_node < 13):
            command = interf.get_command()
            if command == "n":
                if in_node == 1 or in_node == 2 or in_node == 3:
                    interf.send_action(mz.Action(1))
                    in_node += 1
                elif in_node == 4:
                    interf.send_action(mz.Action(6))
                    in_node += 2
                    uidcode = interf.get_UID(3)
                    print(uidcode)
                    point.add_UID(str(uidcode))
                    print(point.getCurrentScore())
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
                    uidcode = interf.get_UID(3)
                    print(uidcode)
                    point.add_UID(str(uidcode))
                    print(point.getCurrentScore())
                elif in_node == 11:
                    interf.send_action(mz.Action(1))
                    in_node += 1
                elif in_node == 12:
                    interf.send_action(mz.Action(5))
                    in_node += 1
                print(in_node)

        command = interf.get_command()
        interf.send_action(mz.Action(5))
    elif (sys.argv[1] == '3'):
        interf.send_action(mz.Action(2))
        uidcode = interf.get_UID(2.5)
        print(uidcode)
        point.add_UID(str(uidcode))
        print(point.getCurrentScore())
    interf.end_process()


if __name__ == '__main__':
    main()
