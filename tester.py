from random import randint
import time
from copy import deepcopy
import subprocess
from db_for_a_star_task import db

field = [['' for _ in range(9)] for _ in range(9)]
field[0][0] = 'N'
smith_coorinates = []


def input(string: str):
    return string.encode(encoding='utf-8')


def start(executable_file):
    return subprocess.Popen(
        executable_file,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)


def read(process):
    return process.stdout.readline().decode("utf-8").strip()


def write(process, message):
    process.stdin.write(f"{message.strip()}\n".encode("utf-8"))
    process.stdin.flush()


def terminate(process):
    process.stdin.close()
    process.terminate()
    process.wait(timeout=0.2)


def solution(taskName: str):
    process = start(['python', f'{taskName}.py'])
    write(process, f"1\n")

    write(process, f'{x_keymaker} {y_keymaker}\n')
    program_output = ''

    while 'e' not in program_output:
        program_output = read(process).split()
        # program_output=read(process).split()

        if (len(program_output) == 3):
            curr_x, curr_y = int(program_output[1]), int(program_output[2])
            nearNeo = []
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if not (
                            i == 0 and j == 0) and curr_x + i >= 0 and curr_y + j >= 0 and curr_x + i < 9 and curr_y + j < 9:
                        if (field[curr_x + i][curr_y + j] != ''):
                            nearNeo.append((curr_x + i, curr_y + j, field[curr_x + i][curr_y + j]))
            write(process, str(len(nearNeo)))
            for neo in nearNeo:
                write(process, f'{neo[0]} {neo[1]} {neo[2]}')
        else:
            terminate(process)
            return program_output[1]

    terminate(process)


# smith
for i in range(3):
    x_smith, y_smith = randint(0, 8), randint(0, 8)
    while field[x_smith][y_smith] != '':
        x_smith, y_smith = randint(0, 8), randint(0, 8)
    field[x_smith][y_smith] = 'A'
    smith_coorinates.append((x_smith, y_smith))
    for ii in range(-1, 2, 1):
        for jj in range(-1, 2, 1):
            try:
                if (not (ii == 0 and jj == 0) and ii + x_smith >= 0 and jj + y_smith >= 0 and field[x_smith + ii][
                    y_smith + jj] not in ['A', 'N']):
                    try:
                        field[x_smith + ii][y_smith + jj] = 'P'; smith_coorinates.append((x_smith + ii, y_smith + jj))
                    except:
                        pass
            except:
                pass

        # sentinel
x_sentinel, y_sentinel = 0, 0
while field[x_sentinel][y_sentinel] != '':
    x_sentinel, y_sentinel = randint(0, 8), randint(0, 8)
field[x_sentinel][y_sentinel] = 'S'

if (x_sentinel != 0 and field[x_sentinel - 1][y_sentinel] not in ['P', 'N', 'A']):
    field[x_sentinel - 1][y_sentinel] = 'P1'
if (x_sentinel != 8 and field[x_sentinel + 1][y_sentinel] not in ['P', 'N', 'A']):
    field[x_sentinel + 1][y_sentinel] = 'P1'
if (y_sentinel != 0 and field[x_sentinel][y_sentinel - 1] not in ['P', 'N', 'A']):
    field[x_sentinel][y_sentinel - 1] = 'P1'
if (y_sentinel != 8 and field[x_sentinel][y_sentinel + 1] not in ['P', 'N', 'A']):
    field[x_sentinel][y_sentinel + 1] = 'P1'

x_keymaker, y_keymaker = 0, 0
while field[x_keymaker][y_keymaker] != '':
    x_keymaker, y_keymaker = randint(0, 8), randint(0, 8)
field[x_keymaker][y_keymaker] = 'K'

# start of the game:
field1 = deepcopy(field)

curr_map = ''
for i in field:
    curr_map += f'{i}\n'

'''SOLUTION FOR A-STAR'''
"""--------------------------------------"""
start_time_stamp = time.time()
a_star_answer = solution('a_star')
finish_time_stamp = time.time()
a_star_time = finish_time_stamp - start_time_stamp
"""--------------------------------------"""

'''SOLUTION FOR BACKTRACKING'''
"""--------------------------------------"""
field = deepcopy(field1)
start_time_stamp = time.time()
backtracking_answer = solution('backtracking')
finish_time_stamp = time.time()
backtracking_time = finish_time_stamp - start_time_stamp
"""--------------------------------------"""

'''SET SOLUTIONS INTO DATABASE'''
db = db(database_file='db_for_a_star_task.db')
db.set_new_test(curr_map, a_star_answer, a_star_time, backtracking_answer, backtracking_time)
db.close()




