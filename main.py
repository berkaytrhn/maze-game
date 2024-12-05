from game import MazeGame

import numpy as np
import imageio
from IPython.display import Video
from datetime import datetime
from tqdm import tqdm

def save_video(frames, file_path):
    with imageio.get_writer(file_path, fps=10) as writer:
        for frame in frames:
            writer.append_data(frame)

def value_iteration(env, gamma=0.99, threshold=1e-4):
    n_rows, n_cols = env.maze.shape
    V = np.zeros((n_rows, n_cols))
    policy = -1*np.ones((n_rows, n_cols), dtype=int)


    # Initialize history to store state-action transitions
    history = []    
    frames = []
    max_iterations = 100
    episode=1
    while True:
        
        if episode>=max_iterations:
            break
        delta = 0
        with tqdm(total=n_rows*n_cols, desc="Training Progress...") as pbar:
            for row in range(n_rows):
                for col in range(n_cols):
                    if env.maze[row, col] == 1:
                        continue  # Skip walls
                    
                    v = V[row, col]
                    q_values = []
                    # print(env.action_space.n)
                    for action in range(env.action_space.n):
                        env.state = (row, col)
                        next_state, reward, done, _ = env.step(action)
                        # print(f"row: {row}, col: {col}, action: {action}")
                        # print(next_state, reward, done, _)
                        next_row, next_col = next_state
                        
                        history.append(((row, col), action, next_state, reward))
                        q_value = reward + gamma * V[next_row, next_col]
                        q_values.append(q_value)
                    # print(q_values)
                    V[row, col] = max(q_values)
                    print(q_values)
                    policy[row, col] = np.argmax(q_values)
                    delta = max(delta, abs(v - V[row, col]))
                    
                    _prev =datetime.now()
                    frame = env.render(mode="rgb_array") 
                    pbar.set_description(f"Episode: '{episode}' -> Render took '{(datetime.now()-_prev).total_seconds()}'secs")
                    pbar.update(1)
                    frames.append(frame)

        if delta < threshold:
            break
        
        
        episode+=1
    
    
    return V, policy, history

def main():

    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1, 0, 1, 0, 0],
        [1, 0, 1, 0, 0, 0, 1, 1, 0],
        [1, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0]
    ]
    
    rewards = [
        [1,    1,   1,   1,   1,   1,   1,   1,   1],
        [1,  -10,  -9,  -8,   1,  -8,   1,   0,  -1],
        [1,  -11,   1,  -9,  -8,  -7,   1,   1,  -2],
        [1,  -12,   1,  -8,   1,  -6,  -5,  -4,  -3],
        [1,    1,   1,   1,   1,   1,   1,   1,  -4]
    ]

    game = MazeGame(np.array(maze), np.array(rewards))
    V, policy, history = value_iteration(game)
    print("Value Function:")
    print(V)
    print("Policy:")
    print(policy)
    


if __name__ == "__main__":
    main()
