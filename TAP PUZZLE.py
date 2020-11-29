from time import sleep

import pygame
import random


def which_brick(my_position, my_dict):
    for i in my_dict:
        x1 = my_dict[i]
        x4 = (my_dict[i][0] + brickSize, my_dict[i][1] + brickSize)
        if x4[0] > my_position[0] > x1[0] and x4[1] > my_position[1] > x1[1]:
            return i
    return None


def flags(n, pos, my_list):
    if pos == my_list[n - 1]:
        the_flags[n - 1] = True
        new_color = (255, 121, 77)
    else:
        the_flags[n - 1] = False
        new_color = color
    return new_color


def change(n, position1, my_dict, my_list):
    new_color = flags(n, position1, my_list)

    pygame.draw.rect(screen, new_color, (position1[0], position1[1], brickSize, brickSize))
    text1 = font.render(str(n), True, text_color)
    screen.blit(text1, (position1[0], position1[1]))
    pygame.draw.rect(screen, black_color, (my_dict[n][0], my_dict[n][1], brickSize, brickSize))
    my_dict[n], position1 = position1, my_dict[n]
    return position1, my_dict


def false_numbers(a, b):
    if a - b == 1 or a - b == -1:
        if min(a, b) % size == 0:
            return False
    return True


def validate(n, position1, my_list, my_dict):
    a1 = my_list.index(my_dict[n]) + 1
    a2 = my_list.index(position1) + 1
    if abs(a1 - a2) == 1 or abs(a1 - a2) == size:
        print(a1, a2)
        return false_numbers(a1, a2)
    return False


def win(flags):
    return all(flags)


pygame.init()

done = False
r1, r2 = 800, 800
entered_Resolution = (r1, r2)
size = int(input('Enter the fucking size: '))
screen = pygame.display.set_mode(entered_Resolution)


brickSize = 50
space = 10
black_color = (0, 0, 0)
color = (204, 51, 0)
text_color = (255, 255, 204)
xcor = (r1 // 2) - (25 * (size % 2)) - (space + brickSize) * (size // 2)
ycor = (r2 // 2) - (25 * (size % 2)) - (space + brickSize) * (size // 2)
started_position = (xcor, ycor)

black_position = 0
the_list = []
the_text = []
the_dict = []
the_flags = []
font = pygame.font.Font(None, brickSize)
a_random_number = random.randrange(0, size ** 2)
random_Num = random.sample(range(1, size ** 2), size ** 2 - 1)
random_Num.insert(a_random_number, None)
for i in range(size):
    for j in range(size):
        position = (started_position[0] + (j * (brickSize + space)), started_position[1] + (i * (brickSize + space)))
        the_list.append(position)

for i in range(size):
    for j in range(size):
        position = the_list[i * size + j]
        if i * size + j == a_random_number:
            pygame.draw.rect(screen, black_color, (position[0], position[1], brickSize, brickSize))
            black_position = position
        else:
            the_flags.append(False)
            if (i * size + j) == random_Num[i * size + j] - 1:
                new_color = (255, 121, 77)
            else:
                new_color = color
            pygame.draw.rect(screen, new_color, (position[0], position[1], brickSize, brickSize))
            text = font.render(str(random_Num[i * size + j]), True, text_color)
            screen.blit(text, (position[0], position[1]))
            the_text.append(random_Num[i * size + j])

            the_dict.append([random_Num[i * size + j], position])

the_dict = dict(the_dict)

for i in range(len(the_flags)):
    new_color = flags(i + 1, the_dict[i + 1], the_list)

done2 = False
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if done2:
            sleep(2)
            done = True
            continue

        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()

            a = which_brick(mousePosition, the_dict)
            # print(a)
            if a is not None:
                b = validate(a, black_position, the_list, the_dict)
                if b:
                    black_position, the_dict = change(a, black_position, the_dict, the_list)
                    if win(the_flags):
                        my_position = (r1 // 4, ycor - (brickSize * 2))
                        text = font.render('Congratulations!!!', True, text_color)
                        screen.blit(text, (my_position[0], my_position[1]))
                        my_position = (r1 // 4, ycor - brickSize)
                        text = font.render('Thank you!', True, text_color)
                        screen.blit(text, (my_position[0], my_position[1]))
                        done2 = True

    pygame.display.flip()
