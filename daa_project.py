import tkinter as tk
from tkinter import messagebox, ttk
import heapq
import time

# Grid settings
WIDTH, HEIGHT = 800, 600
ROWS, COLS = 20, 20
CELL_WIDTH = WIDTH // COLS
CELL_HEIGHT = HEIGHT // ROWS

# Colors
COLOR_EMPTY = "white"
COLOR_OBSTACLE = "black"
COLOR_START = "green"
COLOR_END = "red"
COLOR_PATH = "blue"
COLOR_VISITED = "yellow"

# Cell types
EMPTY, OBSTACLE, START, END, PATH, VISITED = range(6)

class PathfindingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Algorithm Visualizer")

        # Canvas setup
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg=COLOR_EMPTY)
        self.canvas.pack()

        # Initialize grid
        self.grid = [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        
        # Start and End points
        self.start = None
        self.end = None

        # Algorithm selection and setup buttons
        self.setup_ui()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click)  # Add start/end/obstacles
        self.canvas.bind("<Button-3>", self.right_click)  # Remove obstacles

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Dropdown to select algorithm
        self.algorithm_var = tk.StringVar(value="BFS")
        algorithm_menu = ttk.Combobox(frame, textvariable=self.algorithm_var, values=["BFS", "DFS", "Dijkstra"])
        algorithm_menu.pack(side=tk.LEFT, padx=5)
        
        # Button to run selected algorithm
        run_button = tk.Button(frame, text="Start Visualization", command=self.run_algorithm)
        run_button.pack(side=tk.LEFT, padx=5)

        # Reset button to clear grid
        reset_button = tk.Button(frame, text="Reset Grid", command=self.reset_grid)
        reset_button.pack(side=tk.LEFT, padx=5)

        # Clear Obstacles button
        clear_button = tk.Button(frame, text="Clear Obstacles", command=self.clear_obstacles)
        clear_button.pack(side=tk.LEFT, padx=5)

    def left_click(self, event):
        row, col = event.y // CELL_HEIGHT, event.x // CELL_WIDTH

        # Set start, end, or obstacle
        if not self.start:
            self.start = (row, col)
            self.grid[row][col] = START
            self.fill_cell(row, col, COLOR_START)
        elif not self.end:
            self.end = (row, col)
            self.grid[row][col] = END
            self.fill_cell(row, col, COLOR_END)
        else:
            self.grid[row][col] = OBSTACLE
            self.fill_cell(row, col, COLOR_OBSTACLE)

    def right_click(self, event):
        row, col = event.y // CELL_HEIGHT, event.x // CELL_WIDTH
        if (row, col) == self.start:
            self.start = None
        elif (row, col) == self.end:
            self.end = None
        self.grid[row][col] = EMPTY
        self.fill_cell(row, col, COLOR_EMPTY)

    def fill_cell(self, row, col, color):
        x1, y1 = col * CELL_WIDTH, row * CELL_HEIGHT
        x2, y2 = x1 + CELL_WIDTH, y1 + CELL_HEIGHT
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def reset_grid(self):
        self.start = None
        self.end = None
        for row in range(ROWS):
            for col in range(COLS):
                self.grid[row][col] = EMPTY
                self.fill_cell(row, col, COLOR_EMPTY)

    def clear_obstacles(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.grid[row][col] == OBSTACLE:
                    self.grid[row][col] = EMPTY
                    self.fill_cell(row, col, COLOR_EMPTY)

    def run_algorithm(self):
        if not self.start or not self.end:
            messagebox.showwarning("Warning", "Please set both Start and End points.")
            return

        algorithm = self.algorithm_var.get()
        if algorithm == "BFS":
            self.run_bfs()
        elif algorithm == "DFS":
            self.run_dfs()
        elif algorithm == "Dijkstra":
            self.run_dijkstra()

    def run_bfs(self):
        queue = [self.start]
        visited = set()
        came_from = {self.start: None}

        while queue:
            current = queue.pop(0)
            if current in visited:
                continue

            visited.add(current)
            self.fill_cell(*current, COLOR_VISITED)
            self.root.update_idletasks()
            time.sleep(0.05)

            if current == self.end:
                self.reconstruct_path(came_from)
                return

            for neighbor in self.get_neighbors(*current):
                if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] != OBSTACLE:
                    queue.append(neighbor)
                    came_from[neighbor] = current

    def run_dfs(self):
        stack = [self.start]
        visited = set()
        came_from = {self.start: None}

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            self.fill_cell(*current, COLOR_VISITED)
            self.root.update_idletasks()
            time.sleep(0.05)

            if current == self.end:
                self.reconstruct_path(came_from)
                return

            for neighbor in self.get_neighbors(*current):
                if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] != OBSTACLE:
                    stack.append(neighbor)
                    came_from[neighbor] = current

    def run_dijkstra(self):
        queue = [(0, self.start)]
        visited = set()
        came_from = {self.start: None}
        costs = {self.start: 0}

        while queue:
            cost, current = heapq.heappop(queue)
            if current in visited:
                continue

            visited.add(current)
            self.fill_cell(*current, COLOR_VISITED)
            self.root.update_idletasks()
            time.sleep(0.05)

            if current == self.end:
                self.reconstruct_path(came_from)
                return

            for neighbor in self.get_neighbors(*current):
                new_cost = costs[current] + 1
                if neighbor not in visited and self.grid[neighbor[0]][neighbor[1]] != OBSTACLE:
                    if neighbor not in costs or new_cost < costs[neighbor]:
                        costs[neighbor] = new_cost
                        heapq.heappush(queue, (new_cost, neighbor))
                        came_from[neighbor] = current

    def get_neighbors(self, row, col):
        neighbors = []
        for r, c in [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]:
            if 0 <= r < ROWS and 0 <= c < COLS:
                neighbors.append((r, c))
        return neighbors

    def reconstruct_path(self, came_from):
        current = self.end
        while current != self.start:
            if current in came_from:
                self.fill_cell(*current, COLOR_PATH)
                current = came_from[current]
            else:
                break  # If there is no path, stop

        # Ensure start and end colors remain unchanged
        self.fill_cell(self.start[0], self.start[1], COLOR_START)
        self.fill_cell(self.end[0], self.end[1], COLOR_END)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingVisualizer(root)
    root.mainloop()
