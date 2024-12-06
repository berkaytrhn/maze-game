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

def value_iteration(env, gamma=0.9, threshold=1e-4, max_iteration: int=1000):
    n_rows, n_cols = env.maze.shape
    V = np.zeros_like(env.maze)
    policy = -1*np.ones_like(env.maze, dtype=int)


    # Initialize history to store state-action transitions
    episode=1
    while True:
        if episode >= max_iteration:
            break
        delta = 0
        
        if episode % 100 == 0:
            pass
            #print(F"Episode: '{episode}' delta: '{delta}', threshold: '{threshold}'")
        for row in range(n_rows):
            for col in range(n_cols):
                # update current state
                env.state = (row, col)
                
                # Skip if wall
                if env.maze[env.state] == 1: # row, col
                    continue 
                
                # current value
                old_value = V[env.state] # row, col
                
                q_values = []
                for action in range(env.action_space.n):
                    
                    # environment step for agent
                    next_state, reward, done, _ = env.step(action)
                    # state -> (<row>, <column>)
                    # value calculation with discount factor 
                    q_value = reward + gamma * V[next_state]

                    # add q values to list for all actions to choose max among them later
                    q_values.append(q_value)
                
                # update value for prev state as max q value
                V[env.state] = max(q_values)
                
                # update delta by comparing delta with temporal difference
                delta = max(delta, abs(old_value - V[env.state]))
                
                _prev =datetime.now()
        if delta < threshold:
            break
        
        episode+=1
    
    return V, policy

def extract_policy(env: MazeGame, V: np.ndarray, P: np.ndarray, gamma=0.9, ):
    frames = []
    for row in range(env.maze.shape[0]):
        for col in range(env.maze.shape[1]):
            env.state = (row, col)
            if env.state == env.goal:
                continue
            values = []
            for action in range(env.action_space.n):
                next_state, reward, _ = env.step(action)
                value = reward + gamma * V[next_state]
                values.append(value)
            frames.append(env._render_rgb_array())
            best_action = env.action_space[np.argmax(values)]
            P[env.state] = best_action
    save_video(frames, "test_video.mp4")
            
            
        
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
    max_iteration = 75_000
    V, policy = value_iteration(game, max_iteration=max_iteration)
    
    # value iteration debug yapılacak, çözüldükten sonra policy run implement edilecek
    print("Maze")
    print(maze)
    print("Value Function:")
    print(V)
    np.save("values.npy", V)
    print("Policy:")
    print(policy)
    np.save("policy.npy", policy)
    
    extract_policy(game, V, policy)
    


if __name__ == "__main__":
    main()
