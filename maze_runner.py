import streamlit as st
import random
import matplotlib.pyplot as plt

# Function to generate the maze using DFS
def gen_maze(cols, rows):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    start = (0, 0)
    maze[start[0]][start[1]] = 0
    stack = [start]

    while stack:
        current = stack[-1]
        x, y = current
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 1:
                count = 0
                for ddx, ddy in directions:
                    nnx, nny = nx + ddx, ny + ddy
                    if 0 <= nnx < rows and 0 <= nny < cols and maze[nnx][nny] == 0:
                        count += 1
                if count < 2:
                    neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell
            maze[nx][ny] = 0
            maze[(x + nx) // 2][(y + ny) // 2] = 0
            stack.append(next_cell)
        else:
            stack.pop()

    maze[rows - 1][cols - 1] = 0  # Exit at bottom-right corner
    return maze

# Function to solve the maze using backtracking
def solve_maze(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def is_valid_move(x, y):
        return 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0

    def backtrack(x, y, path):
        if (x, y) == end:
            return path

        maze[x][y] = 2  # Mark as part of the path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if is_valid_move(nx, ny) and maze[nx][ny] != 2:
                result = backtrack(nx, ny, path + [(nx, ny)])
                if result:
                    return result

        maze[x][y] = 0  # Unmark as visited (backtrack)
        return None

    return backtrack(start[0], start[1], [start])

# Streamlit UI
st.header('Maze Runner - Solving Mazes')

# Slider for maze size
cols = st.slider('Maze Columns', 10, 20, 10, 1)
rows = st.slider('Maze Rows', 10, 20, 10, 1)

# Initialize maze state in session
if 'maze' not in st.session_state:
    st.session_state.maze = None
if 'path' not in st.session_state:
    st.session_state.path = None

# Button to generate maze
if st.button('Generate Maze'):
    st.session_state.maze = gen_maze(cols, rows)
    st.session_state.path = None  # Clear any previous path

# Button to solve the maze
if st.session_state.maze and st.button('Solve Maze'):
    start = (0, 0)  # Entrance at top-left
    end = (rows - 1, cols - 1)  # Exit at bottom-right
    path = solve_maze(st.session_state.maze, start, end)
    st.session_state.path = path

# Display the maze if it exists
if st.session_state.maze:
    st.write("Generated Maze:")
    maze = st.session_state.maze

    # Visualize the maze using Matplotlib
    fig, ax = plt.subplots()
    maze_with_path = [row[:] for row in maze]  # Copy the maze for visualization

    # If there is a solution path, mark it
    if st.session_state.path:
        for (x, y) in st.session_state.path:
            maze_with_path[x][y] = 2  # Mark the path

    # Show maze with path marked
    ax.imshow(maze_with_path, cmap='binary')  # Color map for better visualization
    ax.set_title("Maze with Path")
    ax.axis("off")  # Hide axes for better visualization
    st.pyplot(fig)

# Display the solved path if it exists
if st.session_state.path:
    st.write("Solved Path:")
    st.write(st.session_state.path)
