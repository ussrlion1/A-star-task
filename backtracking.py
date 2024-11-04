class Node:# class of the Node
    def __init__(self, curr_x:int, curr_y:int, dest_x:int, dest_y:int):
        self.x =curr_x # x and y coordinates of the Node
        self.y = curr_y
        self.dest_x = dest_x # x coordinate of the keymaker
        self.dest_y = dest_y # y coordinate of the keymaker
        self.g = 0 # g = distance from start

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

x_neo, y_neo = 0,0 # initial Neo coordinates
x_keymaker, y_keymaker = 0,0 # keymaker coordinates 
#(let's consider this string as a decloration of a global variable, since we change these values right after the start of the program )
visitedPoints = [[() for _ in range(9)] for _ in range(9)] # let's follow the visited points using a game map
# where () - not visited yet, ("obstacle") - cell has an obstacle, (neighbour, neighbourNode) - visited but can be improved
obstacles = set() # set of obstacles

# the backtracking algorithm is based on dfs but with some changes.
def dfs(vertex:'Node'):

    global visitedPoints # field of the game.

    print(f'm {vertex.x} {vertex.y}') # print the current cell that we are in. 

    obstacles_counter = int(input()) # read the obstacles which are near this node.

    for _ in range(obstacles_counter): 
            x_obstacle, y_obstacle, type_obstacle = input().split()
            if (str(type_obstacle)=='K'): # if the obstacle is a keymaker, we skip it
                continue
            x_obstacle, y_obstacle = int(x_obstacle), int(y_obstacle) #otherwise we add an obstacle to the field
            visitedPoints[x_obstacle][y_obstacle] = ("obstacle")

    neighbours = vertex.neighbours() # obtain the neighbours of the current node
    for neighbour in neighbours: # let's go through all the neighbours
        if visitedPoints[neighbour[0]][neighbour[1]]!=("obstacle"): # if the neighbour is not an obstacle
            neighbourNode = Node(neighbour[0], neighbour[1], x_keymaker, y_keymaker) # create the neighbour Node
            if visitedPoints[neighbour[0]][neighbour[1]]==(): # if the neighbour is not visited
                neighbourNode.g = vertex.g+1 # the path to the neighbour is one more than the path to the current node
                visitedPoints[neighbour[0]][neighbour[1]] = (neighbour, neighbourNode) # add information about the neighbour to the field
                dfs(neighbourNode) # call the function from the neighbour

                print(f'm {vertex.x} {vertex.y}') # print for coming back
                #(using this print we can ensure that our 2 consecutive outputs contain information about neighboring cells )

                notNeeded = int(input()) # read the unnecessary input data
                for _ in range(notNeeded):
                    _ = input()

            elif (visitedPoints[neighbour[0]][neighbour[1]][1].g > vertex.g+1): # if the neighbour is visited but we can find the shorter path
                    visitedPoints[neighbour[0]][neighbour[1]][1].g = vertex.g+1 # update the g value
                    dfs(visitedPoints[neighbour[0]][neighbour[1]][1])# call the function from the neighbour trying to
                    #improve the pathes of the neighbours of our neighbour
                    print(f'm {vertex.x} {vertex.y}') # print for coming back. 
                    #(using this print we can ensure that our 2 consecutive outputs contain information about neighboring cells )

                    notNeeded = int(input()) # read the unnecessary input data.
                    for _ in range(notNeeded):
                        _ = input()

def first_case()->int: # first case.
    start =Node(x_neo, y_neo, x_keymaker, y_keymaker) # initialization of the start Node.
    visitedPoints[x_neo][y_neo] = ((x_neo, y_neo), start) # put the starting node as already visited
    dfs(start) # start the algorithm from this node.
    try:
        return visitedPoints[x_keymaker][y_keymaker][1].g # try to return the number of moves in the keymaker node
    except:return -1 # if we can't find the path, we return -1  ( in try catch, since if we can't find the path,
    #we do not store a Node in the x-keymaker, y-keymaker cell)

def second_case()->int: # in the second case, the logic of Neo does not change too much so we can simply call the first case function
    return first_case()

if __name__=='__main__':
    game_type = int(input()) # the variant of the game (1 or 2)
    x_keymaker, y_keymaker = map(int,input().split()) # coordinates of the keymaker (finish)
    distance = lambda x: first_case() if x == 1 else second_case()# lambda function of the distance. 
    #It calls the nessecary function depending on the variant of the game. 1 - first case, 2 - second
    print(f'e {distance(game_type)}') # answer or -1 if unsolvable
