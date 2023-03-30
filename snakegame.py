import numpy as np
import cv2
import random
import time


# def collision_with_apple(apple_position, score):
#     apple_position = [random.randrange(1, 50)*10, random.randrange(1,50)*10]
#     score +=1
#     return apple_position, score

def collision_with_apple(apple_position, score):
    apple_position = [random.randrange(1, 50)*10, random.randrange(1,50)*10]
    score += 1
    return apple_position, score


def collision_with_boundaries(snake_head):
    if snake_head[0]>=500 or snake_head[0]<0 or snake_head[1]>=500 or snake_head[1]<0:
        return 1
    else:
        return 0
    
# def collision_with_self(snake_position):
#     snake_head = snake_position[0]
#     if snake_head in snake_position[1]:
#         return 1
#     else:
#         return 0
    
def collision_with_self(snake_position):
    snake_head = snake_position[0]
    for position in snake_position[1:]:
        if position == snake_head:
            return 1
    return 0

    
img = np.zeros((500,500,3), dtype='uint8')
#Initial Snake and Apple position
snake_position = [[250,250], [240,250], [230,250]]
apple_position = [random.randrange(1,50)*10, random.randrange(1,50)*10]
score = 0
prev_button_direction = 1
button_direction = 1
snake_head = [250,250]

while True:
    cv2.imshow('a', img)
    cv2.waitKey(1)
    img = np.zeros((500,500,3), dtype='uint8')
    #Display Apple
    cv2.rectangle(img, (apple_position[0], apple_position[1]), (apple_position[0]+10, apple_position[1]+10), (0,0,255), 3)
    #Display snake
    for position in snake_position:
        cv2.rectangle(img, (position[0],position[1]), (position[0]+10, position[1]+10), (0, 255, 0), 3)

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

    if k== ord('a') and prev_button_direction != 1:
        button_direction = 0
    elif k == ord('d') and prev_button_direction !=0:
        button_direction = 1
    elif k == ord('w') and prev_button_direction !=2:
        button_direction = 3
    elif k == ord('s') and prev_button_direction !=3:
        button_direction = 2
    elif k==ord('q'):
        break
    else:
        button_direction=button_direction
    prev_button_direction = button_direction

    #Change the head position based on the button direction
    if button_direction==1:
        snake_head[0] +=10
    elif button_direction ==0:
        snake_head[0] -=10
    elif button_direction ==2:
        snake_head[1] +=10
    elif button_direction ==3:
        snake_head[1] -=10

    if k == ord('a') and prev_button_direction != 1:
        pass
        button_direction = 0
    elif k == ord('d') and prev_button_direction != 0:
        button_direction = 1
    elif k == ord('w') and prev_button_direction != 2:
        button_direction = 3
    elif k == ord('s') and prev_button_direction != 3:
        button_direction = 2
    else:
        button_direction = button_direction


    #Increse snake length on eating apple
    if snake_head == apple_position:
        apple_position, score = collision_with_apple(apple_position, score)
        snake_position.insert(0,list(snake_head))

    else:
        snake_position.insert(0, list(snake_head))
        snake_position.pop()

    #on Collision Kill the snake and print the score
    if collision_with_boundaries(snake_head)==1 or collision_with_self(snake_position) ==1:
        font = cv2.FONT_HERSHEY_SIMPLEX
        img = np.zeros((500,500,3), dtype='uint8')
        cv2.putText(img, 'Your score is {}'.format(score), (140,250), font, 1, (255,255,255), 2, cv2.LINE_AA)
        cv2.imshow('a', img)
        cv2.waitKey(0)
        break


cv2.destroyAllWindows()



