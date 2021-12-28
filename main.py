# MODULES
import pygame
import sys
import numpy as np
from tkinter import *
from tkinter import messagebox

import random
import time
from function import attacked_queens_pairs, read_input

pygame.init()

WIDTH = 800
HEIGHT = 800

ROWS = 8
COLS = 8
SQUARE_SIZE = 100

# rgb: red green blue
WHITE = (255, 255, 255)
BG_COLOR = (255, 255, 204)
SQ_COLOR = (125, 148, 93)

QUEEN_IMAGE = pygame.image.load('queen.png')
QUEEN = pygame.transform.scale(QUEEN_IMAGE, (80, 80))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('8 QUEENS PROBLEM')

board = np.zeros((ROWS, COLS))

def draw_squares():
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, SQ_COLOR, (row*SQUARE_SIZE,
                             col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def refresh_screen():
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(screen, SQ_COLOR, (row*SQUARE_SIZE,
                             col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.flip()


def draw_queens_line(seq):
    for col in range(8):
        row = seq[col] - 1
        if row >= 0:
            pos = pygame.Rect(col*SQUARE_SIZE + 10, row *
                              SQUARE_SIZE + 10, 80, 80)
            screen.blit(QUEEN, (pos.x, pos.y))
    pygame.display.flip()


def draw_queens_file():
    with open('input.txt') as f:
        lines = f.readlines()
    f.close()

    for i in lines:
        data = i.split(' ')
        data = [int(x) for x in data]
        col = data[0]-1
        row = data[1]-1
        pos = pygame.Rect(col*SQUARE_SIZE + 10, row*SQUARE_SIZE + 10, 80, 80)
        screen.blit(QUEEN, (pos.x, pos.y))


def Astar():
    seqs = read_input()
    frontier_priority_queue = [{'unplaced_queens': seqs.count(
        0), 'pairs': attacked_queens_pairs(seqs), 'seqs': seqs}]
    solution = []

    while frontier_priority_queue:
        first = frontier_priority_queue.pop(0)
        if first['pairs'] == 0 and first['unplaced_queens'] == 0:
            solution = first['seqs']
            break
        nums = list(range(1, 9))
        seqs = first['seqs']
        if seqs.count(0) == 0:
            continue
        for j in range(8):
            pos = seqs.index(0)
            temp_seqs = list(seqs)
            temp = random.choice(nums)
            temp_seqs[pos] = temp
            nums.remove(temp)
            frontier_priority_queue.append({'unplaced_queens': temp_seqs.count(
                0), 'pairs': attacked_queens_pairs(temp_seqs), 'seqs': temp_seqs})
            draw_queens_line(temp_seqs)
            time.sleep(0.005)
            refresh_screen()
            time.sleep(0.005)

        frontier_priority_queue = sorted(
            frontier_priority_queue, key=lambda x: (x['pairs']+x['unplaced_queens']))

    if solution:
        # print('Solution sequence found:' + str(solution))
        # display_board(solution)
        return solution
    else:
        return False


def mark_square(row, col):
    board[row][col] = 1


def unmark_square(row, col):
    board[row][col] = 0


def available_square(row, col):
    return board[row][col] == 0


def is_board_full():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0:
                return False

    return True


def empty_file():
    f = open("input.txt", "r+")
    f.truncate(0)
    f.close()


def restart():
    empty_file()
    draw_squares()
    for row in range(ROWS):
        for col in range(COLS):
            board[row][col] = 0


draw_squares()
queen_remain = 8


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            empty_file()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouseX = event.pos[0]  # x
            mouseY = event.pos[1]  # y

            clicked_row = int(mouseY // SQUARE_SIZE)
            clicked_col = int(mouseX // SQUARE_SIZE)

            print("Yolo")

            if available_square(clicked_row, clicked_col):
                queen_remain -= 1
                if queen_remain > 0:
                    f = open("input.txt", "a")
                    f.write(str(clicked_col+1) + " " +
                            str(clicked_row+1) + "\n")
                    f.close()

                    seq = read_input()
                    attack = attacked_queens_pairs(seq)

                    if attack == 0:
                        mark_square(clicked_row, clicked_col)
                        pos = pygame.Rect(clicked_col*SQUARE_SIZE +
                                        10, clicked_row*SQUARE_SIZE + 10, 80, 80)
                        screen.blit(QUEEN, (pos.x, pos.y))
                    else:
                        f = open("input.txt", "r")
                        lines = f.readlines()
                        f.close()

                        f = open("input.txt", "w")
                        remove_queen = str(clicked_col+1) + " " + str(clicked_row+1)
                        for line in lines:
                            if line.strip("\n") != remove_queen:
                                f.write(line)
                        f.close()
                        queen_remain += 1
                        Tk().wm_withdraw() #to hide the main window
                        messagebox.showerror('Error','This queen will be attacked by the previous one, please try to place another position') 
                        
                              
            else:
                draw_squares()
                queen_remain += 1
                f = open("input.txt", "r")
                lines = f.readlines()
                f.close()

                f = open("input.txt", "w")
                remove_queen = str(clicked_col+1) + " " + str(clicked_row+1)
                for line in lines:
                    if line.strip("\n") != remove_queen:
                        f.write(line)
                f.close()
                unmark_square(clicked_row, clicked_col)
                draw_queens_file()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print("Running...")
                solution = Astar()
                if solution:
                    print("Solution has been found")
                    refresh_screen()
                    draw_queens_line(solution)
                else:
                    print("Failed")

            elif event.key == pygame.K_r:
                print("Restart!")
                restart()

    pygame.display.update()
