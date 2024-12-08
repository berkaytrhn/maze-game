from game import MazeGame
import numpy as np
import imageio

class PolicyIteration:
    
    def __init__(
        self,
        env: MazeGame,
        gamma=0.9,
        threshold=1e-6,
        max_iteration= 5000
        ) -> None:
        
        self.env = env
        self.gamma = gamma
        self.threshold = threshold
        self.max_iteration=max_iteration
        self.V=np.zeros_like(self.env.maze)
        self.P=np.zeros_like(self.env.maze)
    
    
    def policy_evaluation(self) -> None:
        """
        -> Policy Evaluation step of policy iteration,
        
        - We simply choose action based on policy for
        each state and calculate bellamn equation like
        values for these states 
        
        -> Updates Value function of this env, does not update policy
        """
        while True:
            delta = 0
            
            # iterate all possible states in environment
            for row in range(self.env.maze.shape[0]):
                for col in range(self.env.maze.shape[1]):

                    # set current state
                    state = (row, col)
                    
                    # pass if reached goal_state
                    if state == self.env.goal_state:
                        continue
                    
                    # value for current state
                    old_value = self.V[state]
                    
                    # set current environment state 
                    self.env.state=state
                    
                    # choosing action based on policy
                    action = self.P[state]
                    
                    # take one step on environment
                    next_state, reward, _, _ = self.env.step(action)
                    
                    # update value for current state
                    self.V[state] = reward + self.gamma * self.V[next_state]
                    
                    # update delta value using temporal difference and previous state value
                    delta = max(delta, abs(old_value - self.V[state]))
            
            # iteration terminate condition
            if delta < self.threshold:
                break
    
    def policy_improvement(self) -> None:
        """
        -> Policy Improvement step of policy ietarion,
        - We simply take all possible action for all possible states 
        and calculate cumulative values for all possible actions for a single state
        
        - Then the action led to highest value chosen and the policy updated accordingly.
        
        -> Updates Policy based on best action, does not change Value function
        """
        policy_stable = True
        
        # iterate all possible states in environment
        for i in range(self.env.maze.shape[0]):
            for j in range(self.env.maze.shape[1]):
                
                # set current state
                state = (i, j)
                
                # pass if reached goal_state
                if state == self.env.goal_state:
                    continue
                
                # get previous action based on state(used for stability determination)
                old_action = self.P[state]
                
                values = []
                # iterate for all possible actions for current state
                for action in range(self.env.action_space.n):
                    # set current environment state 
                    self.env.state=state
                    
                    # take one step on environment using given action
                    next_state, reward, _, _ = self.env.step(action)
                    
                    # calculate cumulative reward using immediate reward and Value function
                    value = reward + self.gamma * self.V[next_state]
                    values.append(value)
                    
                # choose best action by highest value
                # index of "values" array corresponds to an action
                best_action = np.argmax(values)
                
                # update policy by best action 
                self.P[state] = best_action
                
                # check if policy improved or not?
                if old_action != best_action:
                    policy_stable = False
        return policy_stable

    def policy_iteration(self):
        """
        Combine Policy Evaluation and Improvement
        """
        iteration=0
        while True:
            if iteration>=self.max_iteration:
                break

            self.policy_evaluation()
            if self.policy_improvement():
                break
            iteration+=2
        
    def run_policy(self, max_try:int = 1000):
        """
        Run calculated policy on environment
        """
        
        # frames of policy run to create video later
        # initialize with initial state frame 
        frames = [self.env._render_rgb_array(self.P)]
        
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
            frames.append(self.env._render_rgb_array(self.P))
            if done:
                print(f"Reached the goal in {steps} steps.")
                break
        return frames
    def save_video(self, frames, file_path):
        """
        Save video to watch later
        """
        with imageio.get_writer(file_path, fps=2) as writer:
            for frame in frames:
                writer.append_data(frame)
            