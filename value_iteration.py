
from game import MazeGame
import numpy as np
import imageio

class ValueIteration:
    # TODO: Find a better way to integrate gym.Env for actions and obs space
    # TODO: Use custom topological sort or bfs from algorithms repo for dynamic reward calculation
    def __init__(
        self, 
        env: MazeGame,
        gamma: float=0.9, 
        threshold: float=1e-12, 
        max_iteration: int=5_000
    ) -> None:
        self.env = env
        self.gamma = gamma
        self.threshold = threshold
        self.max_iteration = max_iteration
        self.V=None
        self.P=None
    
    def value_iteration(self) -> None:
        """
        - Performs Value Iteration for Provided 
        MazeGame(will be generalized later),
        
        - Updates class field V, no return value
        """
        n_rows, n_cols = self.env.maze.shape
        
        # initialize Values
        self.V = np.zeros_like(self.env.maze)

        episode=1
        delta=float("inf")
        while delta>self.threshold:
            
            # terminate if max iteration reached
            if episode >= self.max_iteration:
                break
            delta = 0
            
            if episode % 10000 == 0:
                print(F"Episode: '{episode}' delta: '{delta}', threshold: '{self.threshold}'")

            for row in range(n_rows):
                for col in range(n_cols):
                    # Set temp state
                    state = (row,col)
                    
                    # Skip if wall
                    if self.env.maze[state] == 1: 
                        continue
                    
                    # current value
                    old_value = self.V[state] # row, col
                    
                    q_values = []
                    
                    # iterate over all possible actions for a state for cumulative value calculation
                    for action in range(self.env.action_space.n):
                        # update env current state
                        self.env.state=state
                        
                        # take one step on environment
                        next_state, reward, done, _ = self.env.step(action)
                        
                        # state -> (row, column)
                        
                        # value calculation with discount factor 
                        q_value = reward + self.gamma * self.V[next_state]
                        
                        # add q values to list for all actions to choose max among them later
                        q_values.append(q_value)
                    
                    # get max value among values for actions
                    max_value = max(q_values)
                    
                    # update value for prev state as max q value
                    self.V[state] = max_value
                    
                    # update delta by comparing delta with temporal difference
                    delta = max(delta, abs(old_value - max_value))
                                        
                    self.env.state = state
            if delta < self.threshold:
                break
            
            episode+=1
    def policy_extraction(self) -> None:
        """
        - Calculates Optimal Policy for provided 
        MazeGame environment(will be generalized later)
        - Updates class field P array, no return policy
        """
        
        if self.V is None:
            return None
        
        # initialize policy
        self.P = np.zeros_like(self.env.maze)
        
        # Loop over all states in environment
        for row in range(self.env.maze.shape[0]):
            for col in range(self.env.maze.shape[1]):
                state = (row, col)
                
                #if goal state, do not modify
                if state == self.env.goal_state:
                    continue
                
                
                values = []
                # Iterate over all possible actions to calculate optimal policy
                for action in range(self.env.action_space.n):
                    # set env state
                    self.env.state=state
                    
                    # take one step on environment
                    next_state, reward, done, _ = self.env.step(action)
                    
                    # calculate value for current state
                    value = reward + self.gamma * self.V[next_state]
                    values.append(value)
                    
                # choose best action among actions by considering value of it to determine policy
                best_action = range(self.env.action_space.n)[np.argmax(values)]
                
                # update policy
                self.P[state] = best_action
                
    def run_policy(self, max_try: int=1000) -> list:
        """
        Run calculated policy on environment
        """
        
        # frames of policy run to create video later
        # initialize with initial state frame 
        frames = [self.env._render_rgb_array()]
        
        # reset all environment states 
        state = self.env.reset()
        steps = 0
        
        # perform actions according to policy until reached goal state
        while state != self.env.goal_state:
            # get best action for current state
            action = self.P[state]
            
            # take one step in environment
            state, _, done, _ = self.env.step(action)
            steps += 1
            
            # For stuck situations, use max try, then terminate
            if steps >= max_try:
                break
            
            # add current state as frame 
            frames.append(self.env._render_rgb_array())
            if done:
                print(f"Reached the goal in {steps} steps.")
                break
        return frames
        
    def save_video(self, frames, file_path):
        """
        Save video to watch later
        """
        with imageio.get_writer(file_path, fps=5) as writer:
            for frame in frames:
                writer.append_data(frame)
            