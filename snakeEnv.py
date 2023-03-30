import gym
from gym import spaces
import numpy as np
import cv2
import random
import time
from collections import deque

SNAKE_LEN_GOAL = 30


def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50)*10, random.randrange(1,50)*10]
    score +=1
    return apple_position, score

def collision_with_boundaries(snake_head):
    if snake_head[0]>=500 or snake_head[0]<0 or snake_head[1]>=500 or snake_head[1]<0:
        return 1
    else:
        return 0
    
def collision_with_self(snake_position):
    snake_head = snake_position[0]
    if snake_head in snake_position[1]:
        return 1
    else:
        return 0

class SnekEnv(gym.Env):
    metadata = {'render.modes':['human']}

    def __init__(self):
        super(SnekEnv, self).__init__()

        #Define action and observation space
        #they must be gym.spaces objects
        #Example when using discrete actions:
        self.action_space = spaces.Discrete(4)
        #Example for uisng imagfe as input (channel-first; channel-last also works):
        self.observation_space = spaces.Box(low=500, high=500, shape=(5+SNAKE_LEN_GOAL, ), dtype=np.float32)


    
    def step(self, action):
        #self.prev_actions.append(action)


        cv2.imshow('a', self.img)
        cv2.waitKey(1)
        self.img = np.zeros((500,500,3), dtype='uint8')
        #Display Apple
        cv2.rectangle(self.img, (self.apple_position[0], self.apple_position[1]), (self.apple_position[0]+10, self.apple_position[1]+10), (0,0,255), 3)
        #Display snake
        for position in self.snake_position:
            cv2.rectangle(self.img, (position[0],position[1]), (position[0]+10, position[1]+10), (0, 255, 0), 3)

        #takes step after fixed time
        t_end = time.time() + 0.05
        k = -1
        while time.time() < t_end:
            if k == -1:
                k = cv2.waitKey(1)
            else:
                continue

        # 0 - left, 1-right, 3-up, 2-down, q-break
        #a-left, d-right, w-up, s-down

        

        #Change the head position based on the button direction
        if action==1:
            self.snake_head[0] +=10
        elif action ==0:
            self.snake_head[0] -=10
        elif action ==2:
            self.snake_head[1] +=10
        elif action ==3:
            self.snake_head[1] -=10

        #Increse snake length on eating apple
        if self.snake_head == self.apple_position:
            self.apple_position, self.score = collision_with_apple(self.apple_position, self.score)
            self.snake_position.insert(0,list(self.snake_head))

        else:
            self.snake_position.insert(0, list(self.snake_head))
            self.snake_position.pop()

        #on Collision Kill the snake and print the score
        if collision_with_boundaries(self.snake_head)==1 or collision_with_self(self.snake_position) ==1:
            font = cv2.FONT_HERSHEY_SIMPLEX
            self.img = np.zeros((500,500,3), dtype='uint8')
            cv2.putText(self.img, 'Your score is {}'.format(self.score), (140,250), font, 1, (255,255,255), 2, cv2.LINE_AA)
            cv2.imshow('a', self.img)
            self.done = True


        if self.done:
            self.reward = -10

        else:
            self.reward = self.score #hm apples eaten?

        head_x = self.snake_head[0]
        head_y = self.snake_head[1]

        apple_delta_x = head_x - self.apple_position[0]
        apple_delta_y = head_y - self.apple_position[1]

        snake_length = len(self.snake_position)
        self.prev_actions = deque(maxlen=SNAKE_LEN_GOAL)
        for _ in range(SNAKE_LEN_GOAL):
            self.prev_actions.append(-1)


        self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_length] + list(self.prev_actions)
        self.observation = np.array(self.observation)


        info = {}
        return self.observation, self.reward, self.done, info
    

    def reset(self):
        self.done = False
        self.img = np.zeros((500,500,3), dtype='uint8')
        #Initial Snake and Apple position
        self.snake_position = [[250,250], [240,250], [230,250]]
        self.apple_position = [random.randrange(1,50)*10, random.randrange(1,50)*10]
        self.score = 0
        self.prev_button_direction = 1
        self.button_direction = 1
        self.snake_head = [250, 250]
        # head_x, head_y, apple_delta_x, apple_delta_y, snake_length, previous moves

        head_x = self.snake_head[0]
        head_y = self.snake_head[1]

        apple_delta_x = head_x - self.apple_position[0]
        apple_delta_y = head_y -self.apple_position[1]

        snake_length = len(self.snake_position)

        self.prev_actions = deque(maxlen=SNAKE_LEN_GOAL)
        for _ in range(SNAKE_LEN_GOAL):
            self.prev_actions.append(-1)

        self.observation = [head_x, head_y, apple_delta_x, apple_delta_y, snake_length] + list(self.prev_actions)
        self.observation = np.array(self.observation)



        return self.observation