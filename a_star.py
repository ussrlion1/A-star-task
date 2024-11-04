import heapq
class Node: # class of the Node
    def __init__(self, curr_x:int, curr_y:int, dest_x:int, dest_y:int):
        self.x =curr_x # x and y coordinates of the Node
        self.y = curr_y
        self.dest_x = dest_x # x coordinate of the keymaker
        self.dest_y = dest_y # y coordinate of the keymaker
        self.g = 0 # g = distance from start
        self.h = dest_x+dest_y # h = distance from end
        self.f = self.h + self.g # f = g + h
        self.fullpath =[] # the shortest path from start to the current Node
        self.parent = None # the parent of the current Node

    def __lt__(self, other:'Node'): # operator < (less than) overloading. 
        if self.f<other.f: # we compare two Node objects by comparing their f values
            return self.f<other.f 
        elif self.f==other.f: # if f values are equal, we compare their h values
            return self.h<other.h
    def __eq__(self,other:'Node'):
        return self.x == other.x and self.y == other.y # operator = (equal to) overloading
    
    def __hash__(self): # hashing the object by its x and y coordinates
        return hash((self.x, self.y))
        
    def neighbours(self)->list: # Function that returns the neighbours of the current Node depending on its coordinates

        # block of coordinates which are not on the sides or corners
        #----------------------------------------------------------------------
        if self.x >0 and self.y>0 and self.x<8 and self.y<8: 
            return { (self.x+1, self.y), (self.x-1, self.y), (self.x, self.y+1), (self.x, self.y-1)}
        #----------------------------------------------------------------------


        #block of coordinates for the sides
        #----------------------------------------------------------------------
        elif self.x==0 and self.y>0 and self.y<8:
            return { (self.x+1, self.y), (self.x, self.y+1), (self.x, self.y-1)}
        elif self.x>0 and self.y==0 and self.x<8:
            return { (self.x+1, self.y), (self.x-1, self.y), (self.x, self.y+1)}
        elif self.x>0 and self.y==8 and self.x<8:
            return { (self.x+1, self.y), (self.x-1, self.y), (self.x, self.y-1)}
        elif self.x==8 and self.y>0 and self.y<8:
            return { (self.x-1, self.y), (self.x, self.y+1), (self.x, self.y-1)}
        #----------------------------------------------------------------------


        # block of coordinates for the corners
        #----------------------------------------------------------------------
        elif self.x==0 and self.y==0:
            return { (self.x+1, self.y), (self.x, self.y+1)}
        elif self.x==0 and self.y==8:
            return { (self.x+1, self.y), (self.x, self.y-1)}
        elif self.x==8 and self.y==0:
            return { (self.x-1, self.y), (self.x, self.y+1)}
        elif self.x==8 and self.y==8:
            return { (self.x-1, self.y), (self.x, self.y-1)}
        #----------------------------------------------------------------------


    def move_from_one_path_to_another(self, previous:'Node'): # fuction that moves Neo from one cell to another if they are not neighbours
        for i in range(len(previous.fullpath)): # firstly we try to find the least common parent.
            if previous.fullpath[i]==self.fullpath[i]: # if the cells are the same, we continue
                continue
            i=i-1 # otherwise, the previous cell is the least common parent. So we should come back to it.
            for forward in range(len(previous.fullpath)-2,i-1,-1): # if we find the least common parent, we print the path 
                #from the previous cell to the least common parent
                print(f'm {previous.fullpath[forward][0]} {previous.fullpath[forward][1]}')

                notNeeded=int(input()) #read the necessary input data.
                for _ in range(notNeeded):
                    _ = input()

            for forward in range(i+1, len(self.fullpath)-1):# and then we print the path from the least common parent to the current cell
                print(f'm {self.fullpath[forward][0]} {self.fullpath[forward][1]}')

                notNeeded=int(input())# read the necessary input data.
                for _ in range(notNeeded):
                    _ = input()
            break # so now we moved from one node to another, so we should break the loop.



x_neo, y_neo = 0,0 # initial Neo coordinates
x_keymaker, y_keymaker = 0,0 # keymaker coordinates 
#(let's consider this string as a decloration of a global variable, since we change these values right after the start of the program )

opened_set = dict() # set of cells which we are going to visit (for fast accessing)
closed_set = set() # set of cells which we already visited
obstacles = [] # list of obstacles.
open_list = [] # list of cells which we are going to visit (required for heap operations)

def first_case()->int:
    #A* algorithm
    start =Node(x_neo, y_neo, x_keymaker, y_keymaker) # initialization of the start Node.
    start.fullpath.append((start.x, start.y)) # add (0,0) to the path of the start Node.
    opened_set[start.x, start.y]=start # put the start Node in the opened set. 
    heapq.heappush(open_list, start) # put the start Node in the open list (heap)

    previousNode = start # for the first iteration we initialize previous node as a start one
    # in other iterations we will use this variable to check if the current node is a neighbour of the previous one

    while open_list: # the cycle which is going to run while we have nodes in the open list
        curr_node = heapq.heappop(open_list)# pop the Node with the smallest f value from the open list
        if curr_node.x == curr_node.dest_x and curr_node.y == curr_node.dest_y: # if we reached the keymaker, we return the number of moves

            print(f'm {curr_node.dest_x} {curr_node.dest_y}')

            notNeeded=int(input())
            for _ in range(notNeeded):
                _ = input()

            return curr_node.g
        #obtain all the neighbours of the current node
        neighbours = curr_node.neighbours() 
        #check, if we current node is a neighbour of the previous one
        if curr_node!=start and (previousNode.x, previousNode.y) not in neighbours:
            #if not, create the path from the previous one to the current
            curr_node.move_from_one_path_to_another(previousNode)
            previousNode = curr_node.parent

        closed_set.add((curr_node.x, curr_node.y))# since we have visited the current node, put it in the closed set

        #read the obstacles and add them to the list
        print(f'm {curr_node.x} {curr_node.y}')
        obstacles_counter=int(input())
        for _ in range(obstacles_counter):
            x_obstacle, y_obstacle, type_obstacle = input().split()
            if (str(type_obstacle) in ['K']): # if the obstacle is a keymaker, we skip it
                continue
            obstacles.append((int(x_obstacle), int(y_obstacle), str(type_obstacle))) # otherwise, add it to the list

        for neighbour in neighbours: # go through all the neighbours
            if neighbour in closed_set:# if the neighbour is in the closed set, we skip it
                continue
            if sum([neighbour[0]==i[0] and neighbour[1]==i[1] for i in obstacles]):# if the neighbour is an obstacle, we skip it
                continue
            # otherwise, initialize a new node.
            open_node = Node(neighbour[0], neighbour[1], curr_node.dest_x, curr_node.dest_y) 
            open_node.g = curr_node.g + 1 # the shortest path to it will be equal to it's parent shortest path + 1
            open_node.h = abs(open_node.dest_x - open_node.x) + abs(open_node.dest_y - open_node.y) # find the probable distance to the keymaker
            #as a Manhattan distance 
            open_node.f = open_node.g + open_node.h # f = g + h
            open_node.parent = curr_node # the parent of the new node will be the current node
            
            open_node.fullpath = curr_node.fullpath.copy() # the path of the new node will be the path of the current node
            open_node.fullpath.append((open_node.x, open_node.y)) # but plus the new node itself

            if opened_set.__contains__((open_node.x, open_node.y)): # so, if the node is in opened set
                #we can improve the path to it
                if opened_set[(open_node.x, open_node.y)].g > open_node.g:
                    opened_set[(open_node.x, open_node.y)].f = open_node.f
                    opened_set[(open_node.x, open_node.y)].g = open_node.g
                    opened_set[(open_node.x, open_node.y)].h = open_node.h
             # otherwise, let's simply add it to the opened set.      
            else:
                opened_set[(open_node.x, open_node.y)] = open_node
            heapq.heappush(open_list, open_node) # and then push the new node to the open list
            
        previousNode = curr_node # after that, we put previous node as the current one
        #and do the next cycle until we reach the keymaker
    return -1 # if the keymaker is not reachable, we return -1

    
def second_case()->int: # in the second case, the logic of Neo does not change too much so we can simply call the first case function
    return first_case()


if __name__=='__main__': 
    zone_variant = int(input()) # the variant of the game (1 or 2)
    x_keymaker, y_keymaker = map(int,input().split()) # coordinates of the keymaker (finish)
    distance = lambda x: first_case() if x == 1 else second_case() # lambda function of the distance. 
    #It calls the nessecary function depending on the variant of the game. 1 - first case, 2 - second
    print(f'e {distance(zone_variant)}') # answer or -1 if unsolvable
'''
P - perception zone 
A - agent smith
S - sentinel 
K - keymaker
B - backdoor key
N - neo
'''
