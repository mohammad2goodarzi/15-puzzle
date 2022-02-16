import sys
from time import sleep

import pygame
import random
import tkinter as tk


def which_brick(clicked_position):
    translated_clicked_position = [clicked_position[0] - started_position[0], clicked_position[1] - started_position[1]]
    row = translated_clicked_position[1] // (BRICK_SIZE + SPACE)
    column = translated_clicked_position[0] // (BRICK_SIZE + SPACE)
    if all([0 <= row < size, 0 <= column < size]):
        return row * size + column
    return None


def change(index):
    black_index = random_num.index(None)
    if abs(index - black_index) == size or (abs(index - black_index) == 1 and index // size == black_index // size):
        random_num[black_index], random_num[index] = random_num[index], random_num[black_index]


def check_win():
    if all([random_num[index] is not None and index == random_num[index] - 1 for index in range(size ** 2 - 1)]):
        my_position = (r1 // 4, ycor - (BRICK_SIZE * 2))
        text = font.render('Congratulations!!!', True, TEXT_COLOR)
        screen.blit(text, (my_position[0], my_position[1]))
        my_position = (r1 // 4, ycor - BRICK_SIZE)
        text = font.render('Thank you!', True, TEXT_COLOR)
        screen.blit(text, (my_position[0], my_position[1]))
        return True
    return False


def give_me_random_numbers():
    all_numbers = list(range(1, size ** 2 + 1))
    the_index = all_numbers.index(size ** 2)
    all_numbers[the_index] = None
    for _ in range(1000):
        picked_neighbor = random.randint(1, 4)
        if picked_neighbor == 1:
            neighbor = the_index - size
        elif picked_neighbor == 2:
            neighbor = the_index + 1
        elif picked_neighbor == 3:
            neighbor = the_index + size
        else:
            neighbor = the_index - 1

        if 0 <= neighbor <= size ** 2 - 1:
            all_numbers[the_index], all_numbers[neighbor] = all_numbers[neighbor], all_numbers[the_index]
            the_index = neighbor

    return all_numbers


def draw():
    for i in range(size):
        for j in range(size):
            position = (
                started_position[0] + (j * (BRICK_SIZE + SPACE)), started_position[1] + (i * (BRICK_SIZE + SPACE))
            )
            if random_num[i * size + j] is not None:
                text = font.render(str(random_num[i * size + j]), True, TEXT_COLOR)
                if random_num[i * size + j] == i * size + j + 1:
                    pygame.draw.rect(screen, CORRECT_COLOR, (position[0], position[1], BRICK_SIZE, BRICK_SIZE))
                else:
                    pygame.draw.rect(screen, SOME_BEAUTIFUL_COLOR, (position[0], position[1], BRICK_SIZE, BRICK_SIZE))
                x_off, y_off = 0, 0
                if random_num[i * size + j] < 10:
                    x_off, y_off = BRICK_SIZE // 3, BRICK_SIZE // 5
                elif random_num[i * size + j] < 100:
                    x_off, y_off = BRICK_SIZE // 4.5, BRICK_SIZE // 5
                screen.blit(text, (position[0] + x_off, position[1] + y_off))


def set_the_size():
    global size
    inp = input_text.get()
    if str(inp).isdigit():
        size = int(inp)
        if size > 10:
            size = 10
        if size < 3:
            size = 3
        frame.destroy()
    else:
        input_text.delete(0, tk.END)


size = -1
frame = tk.Tk()
frame.title("Enter the size")
input_text = tk.Entry(frame)
input_text.grid(row=0, column=1)
print_button = tk.Button(frame, text="Enter", command=set_the_size)
print_button.grid(row=1, column=0, columnspan=2)
lbl = tk.Label(frame, text="Enter the size (between 3 and 10): ")
lbl.grid(row=0, column=0)
frame.mainloop()

if size == -1:
    sys.exit()


BRICK_SIZE = 50
SPACE = 2
BLACK_COLOR = (0, 0, 0)
SOME_BEAUTIFUL_COLOR = (204, 51, 0)
CORRECT_COLOR = (255, 121, 77)
TEXT_COLOR = (255, 255, 204)


pygame.init()

done = False
r1, r2 = (BRICK_SIZE * 6) + 2 * ((25 * (size % 2)) + (SPACE + BRICK_SIZE) * (size // 2)), (BRICK_SIZE * 6) + 2 * ((25 * (size % 2)) + (SPACE + BRICK_SIZE) * (size // 2))
entered_resolution = (r1, r2)
screen = pygame.display.set_mode(entered_resolution)

xcor = (r1 // 2) - (25 * (size % 2)) - (SPACE + BRICK_SIZE) * (size // 2)
ycor = (r2 // 2) - (25 * (size % 2)) - (SPACE + BRICK_SIZE) * (size // 2)
started_position = (xcor, ycor)

black_position = 0
font = pygame.font.SysFont("comicsansms", BRICK_SIZE//2)

random_num = give_me_random_numbers()


done2 = False
while not done:
    screen.fill(BLACK_COLOR)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if done2:
            sleep(2)
            done = True
            continue

        if event.type == pygame.MOUSEBUTTONUP:
            mousePosition = pygame.mouse.get_pos()

            a = which_brick(mousePosition)
            if a is not None:
                change(a)

    if check_win():
        done2 = True

    pygame.display.flip()
