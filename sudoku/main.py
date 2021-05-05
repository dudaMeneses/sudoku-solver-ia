from busca_cega import bfs_resultado
from busca_heuristica import h_resultado
import os

def get_grid(str):
    read_file = open(str, "r")

    lines = read_file.readlines()
    read_file.close()

    output_file = open("output.txt", "w")
    for line_index, line in enumerate(lines):
        if(line_index != 3 and line_index != 7):
            str = "".join(line.split(" "))
            str = "".join(str.split("|"))
            output_file.write(str)
    
    output_file.close


grid = [[0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0]]

get_grid("input.txt")
file = open("output.txt", "r")

for line_index, line in enumerate(file):
    for char_index, char in (enumerate([s for s in line])):
        if (char.isnumeric()):
            grid[line_index][char_index] = int(char)

bfs_resultado(grid)
h_resultado(grid)

file.close()
os.remove("output.txt")