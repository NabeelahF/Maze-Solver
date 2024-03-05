import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class MazeSolver {
    private char[][] maze;
    private int rows;
    private int cols;
    private int startRow;
    private int startCol;
    private int endRow;
    private int endCol;
    private boolean[][] visited;
    private MyStack<int[]> stack;

    public MazeSolver(String filename) {
        readMazeFromFile(filename);
        visited = new boolean[rows][cols];
        stack = new MyStack<>();
    }

    private void readMazeFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            rows = 0;
            cols = 0; // Initialize cols

            while ((line = reader.readLine()) != null) {
                if (cols == 0) {
                    cols = line.length();
                }
                rows++;
            }

            maze = new char[rows][cols];

            // No need to close the reader here, it will be automatically closed by the try-with-resources

            // Initialize a new BufferedReader for the second pass
            try (BufferedReader reader2 = new BufferedReader(new FileReader(filename))) {
                for (int i = 0; i < rows; i++) {
                    line = reader2.readLine();
                    for (int j = 0; j < cols; j++) {
                        maze[i][j] = line.charAt(j);
                        if (maze[i][j] == 'S') {
                            startRow = i;
                            startCol = j;
                        } else if (maze[i][j] == 'E') {
                            endRow = i;
                            endCol = j;
                        }
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private boolean isSafe(int row, int col) {
        return (row >= 0 && row < rows && col >= 0 && col < cols && maze[row][col] != '#');
    }

    private boolean dfs(int row, int col) {
        if (!isSafe(row, col) || visited[row][col]) {
            return false;
        }

        visited[row][col] = true;
        stack.push(new int[]{row, col});

        if (row == endRow && col == endCol) {
            return true;
        }

        if (dfs(row - 1, col) || dfs(row + 1, col) || dfs(row, col - 1) || dfs(row, col + 1)) {
            return true;
        }

        stack.pop();
        return false;
    }

    public void solveMaze() {
        dfs(startRow, startCol);

        if (visited[endRow][endCol]) {
            System.out.println("Path found:");
            while (!stack.isEmpty()) {
                int[] cell = stack.pop();
                maze[cell[0]][cell[1]] = '*';
            }
        } else {
            System.out.println("No path found.");
        }

        printMaze();
    }

    private void printMaze() {
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                System.out.print(maze[i][j]);
            }
            System.out.println();
        }
    }

}