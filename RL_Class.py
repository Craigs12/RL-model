from stable_baselines3 import PPO

import main
import gymnasium as gym
import numpy as np
from gymnasium import spaces
from stable_baselines3.common.env_checker import check_env


class CustomEnv(gym.Env):
    """Custom Environment that follows gym interface."""

    metadata = {"render_modes": ["human"], "render_fps": 30}

    def __init__(self):
        super().__init__()
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        self.action_space = spaces.Discrete(2)
        # Example for using image as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=0, high=1000,shape=(11,), dtype=np.uint16)

        self.run_game = main.game()

        self._action_to_direction={0:"left",1:"right",2:"still"}

    def step(self, action):
        self.run_game.create_stars()
        direction = self._action_to_direction[action]
        self.run_game.move(direction)
        self.run_game.check_collisions()
        self.run_game.game_state_WL()
        self.run_game.draw()
        observation = self.run_game.get_observation()
        reward = .05
        terminated = self.run_game.run == False
        if terminated:
            reward -= 100

        return observation, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        self.run_game = main.game()
        observation = self.run_game.get_observation()
        return observation,{}

    def render(self):
        self.run_game.draw()



# Instantiate the env


env = CustomEnv()
check_env(env, warn=True, skip_render_check=False)
# model = PPO.load("SaveFile",env=env)
# # Enjoy trained agent
# vec_env = model.get_env()
# obs = vec_env.reset()
# while True:
#     action, _states = model.predict(obs, deterministic=True)
#     obs, rewards, dones, info = vec_env.step(action)

# Define and Train the agent
model = PPO("MlpPolicy", env, verbose=1,n_steps=6000).learn(total_timesteps=90000)

model.save("SaveFile")