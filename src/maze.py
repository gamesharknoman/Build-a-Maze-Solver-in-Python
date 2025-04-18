from cell import Cell
import time
import random


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win = None,
        seed = None,
        ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._seed = seed
        self._cells = []
        if self._seed != None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)


    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()


    def _break_entrance_and_exit(self):
        enter_i = 0
        enter_j = 0
        exit_i = self._num_cols - 1
        exit_j = self._num_rows - 1
        self._cells[enter_i][enter_j].has_left_wall = False
        self._draw_cell(enter_i,enter_j)
        self._cells[exit_i][exit_j].has_right_wall = False
        self._draw_cell(exit_i,exit_j)


    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)


    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            directions = []
            if i > 0 and not self._cells[i-1][j].visited:
                directions.append((i-1, j, "west"))
            
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                directions.append((i+1, j, "east"))

            if j > 0 and not self._cells[i][j-1].visited:
                directions.append((i, j-1, "north"))
            
            if j < self._num_rows - 1 and not self._cells[i][j+1].visited:
                directions.append((i, j+1, "south"))

            if not directions:  
                self._draw_cell(i, j)
                return
            
            direction_index = random.randrange(0, len(directions))
            next_i, next_j, direction = directions[direction_index]
            
            if direction == "north":
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == "south":
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            elif direction == "west":
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == "east":
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False

            self._break_walls_r(next_i, next_j)


    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False
        
        
    def solve(self):
        return self._solve_r(0 ,0)


    def _solve_r(self, i, j):
        current_cell = self._cells[i][j]
        self._animate()
        current_cell.visited = True
        if current_cell == self._cells[self._num_cols - 1][self._num_rows - 1]:
            return True
        
        if i > 0 and not self._cells[i-1][j].visited and not current_cell.has_left_wall:
            current_cell.draw_move(self._cells[i-1][j])
            check = self._solve_r(i-1,j)
            if check:
                return True
            current_cell.draw_move(self._cells[i-1][j],undo=True)

        if i < self._num_cols - 1 and not self._cells[i+1][j].visited and not current_cell.has_right_wall:
            current_cell.draw_move(self._cells[i+1][j])
            check = self._solve_r(i+1,j)
            if check:
                return True
            current_cell.draw_move(self._cells[i+1][j],undo=True)

        if j > 0 and not self._cells[i][j-1].visited and not current_cell.has_top_wall:
            current_cell.draw_move(self._cells[i][j-1])
            check = self._solve_r(i,j-1)
            if check:
                return True
            current_cell.draw_move(self._cells[i][j-1],undo=True)
        
        if j < self._num_rows - 1 and not self._cells[i][j+1].visited and not current_cell.has_bottom_wall:
            current_cell.draw_move(self._cells[i][j+1])
            check = self._solve_r(i,j+1)
            if check:
                return True
            current_cell.draw_move(self._cells[i][j+1],undo=True)
        
        return False