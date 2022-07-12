import pygame
import random

class Block :
    def __init__(self):
        self.position = {
            'x' : 5,
            'y' : 2
        }
        self.blocks = []

    def InitPosition(self):
        self.position = {
            'x' : 5,
            'y' : 2
        }

    def moveLeft(self):
        self.position['x'] -= 1

    def moveRight(self):
        self.position['x'] += 1

    def moveDown(self):
        self.position['y'] += 1

    def change(self):
        temp = self.blocks[0]
        self.blocks[0] = self.blocks[1]
        self.blocks[1] = self.blocks[2]
        self.blocks[2] = temp

def getInitializedBoard() :
    board = []

    for i in range(0, 20) :
        board.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

    return board

blockColor = [
    (64, 64, 64),
    (255, 255, 255),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (128, 0, 0),
    (0, 128, 0),
    (0, 0, 128),
    (255, 0, 255),
    (0, 255, 255),
]

blocks = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [2, 4, 3],
    [6, 1, 8],
    [2, 9, 1],
    [5, 7, 2],
    [3, 1, 7],
    [2, 8, 5]
]

screenSize = {
    'width' : 480,
    'height' : 800
}

def canMoveLeft(nowBlock) :
    x = nowBlock.position['x']
    y = nowBlock.position['y']
    if x <= 0:
        return False
    elif board[y][x - 1] != 0:
        return False

    return True

def canMoveRight(nowBlock) :
    x = nowBlock.position['x']
    y = nowBlock.position['y']
    if x >= 9:
        return False
    elif board[y][x + 1] != 0:
        return False

    return True

def canMoveDown(nowBlock) :
    x = nowBlock.position['x']
    y = nowBlock.position['y']
    if y >= 19 :
        return False
    elif board[y + 1][x] != 0 :
        return False

    return True

def setValueOnBoard(x, y, value) :
    global board
    board[y][x] = value

def updateGame(board , nowBlock, nextBlock) :
    blockSize = {
        'width' : screenSize['width'] / 12 - 2,
        'height' : screenSize['height'] / 20 - 2
    }

    for y in range(0, len(board)):
        line = board[y]
        for x in range(0, len(line)):
            block = line[x]
            pygame.draw.rect(screen, blockColor[block],
                             [x * (blockSize['width'] + 1), y * (blockSize['height'] + 1),
                              blockSize['width'], blockSize['height']])
    # position = nowBlock.position
    x = nowBlock.position['x']
    for i in range(0, len(nowBlock.blocks)) :
        block = nowBlock.blocks[i]
        y = nowBlock.position['y'] - i
        pygame.draw.rect(screen, blockColor[block],
                         [x * (blockSize['width']+ 1), y * (blockSize['height'] + 1),
                          blockSize['width'], blockSize['height']])
    #

    for i in range(0, len(nextBlock.blocks)) :
        block = nextBlock.blocks[i]
        y = nextBlock.position['y'] - i
        pygame.draw.rect(screen, blockColor[block],
                         [11 * (blockSize['width'] + 1), y * (blockSize['height'] + 1),
                          blockSize['width'], blockSize['height']])

    pygame.display.flip()

def checkAroundHorizontal(x, y, v, p) :
    if x >= 10 :
        return p
    if v == 0 :
        return p
    if board[y][x] != v :
        return p
    if board[y][x] == v :
        p = checkAroundHorizontal(x+1, y, v, p+1)

    return p

def clearAroundHorizontal(board, x, y, len) :
    for ny in range(y, 0, -1) :
        for nx in range(x, x+len) :
            board[ny][nx] = board[ny-1][nx]

def checkBoard(board) :
    for y in range(0, len(board)) :
        line = board[y]
        for x in range(0, len(line)) :
            v = line[x]
            p = checkAroundHorizontal(x, y, v, 0)
            if p >= 3 :
                clearAroundHorizontal(board, x, y, p)

pygame.init()
screen = pygame.display.set_mode((screenSize['width'], screenSize['height']))
pygame.display.set_caption("HEXA")

nowBlock = Block()
nextBlock = Block()
board = getInitializedBoard()

isPlaying = True
sel = random.randint(0, len(blocks) - 1)
nowBlock.blocks = blocks[sel]
nextBlock.InitPosition()
sel = random.randint(0, len(blocks) - 1)
nextBlock.blocks = blocks[sel]

while isPlaying :
    updateGame(board, nowBlock, nextBlock)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                isPlaying = False
                break
            elif event.key == pygame.K_UP :
                break
            elif event.key == pygame.K_LEFT :
                if canMoveLeft(nowBlock) :
                    nowBlock.moveLeft()
                break
            elif event.key == pygame.K_RIGHT :
                if canMoveLeft(nowBlock) :
                    nowBlock.moveRight()
                break
            elif event.key == pygame.K_DOWN :
                if canMoveLeft(nowBlock) :
                    nowBlock.moveDown()
                break
    if canMoveDown(nowBlock) :
        nowBlock.moveDown()
    else :
        for i in range(0, len(nowBlock.blocks)) :
            x = nowBlock.position['x']
            y = (nowBlock.position['y'] - i)
            setValueOnBoard(x, y, nowBlock.blocks[i])

        checkBoard(board)

        nowBlock.InitPosition()
        nowBlock.blocks = nextBlock.blocks

        nextBlock.InitPosition()
        sel = random.randint(0, len(blocks) - 1)
        nextBlock.blocks = blocks[sel]

    pygame.time.delay(500)

