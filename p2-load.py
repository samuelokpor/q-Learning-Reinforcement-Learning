import gym
from stable_baselines3 import PPO, A2C
import os


env = gym.make("LunarLander-v2")
env.reset()


models_dir = "models/PPO-1672975641"
model_path = f"{models_dir}/550000.zip"

model = PPO.load(model_path, env=env)

episodes = 10

for ep in range(episodes):
    obs = env.reset()
    done = False
    while not done:
        env.render()
        action, _ = model.predict(obs)
        obs, reward, done, info = env.step(action)
        #print(reward)'''


env.close()