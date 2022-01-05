import sys

import pygame
from pygame import mouse

from pygame.math import Vector2, Vector3

CELL_SIZE = 100
HEADER_HEIGHT = 70
FOOTER_HEIGHT = 60 
MARGIN_WIDTH = 50

WINDOW_SIZE_X = 2*MARGIN_WIDTH + 3*CELL_SIZE 
WINDOW_SIZE_Y = HEADER_HEIGHT + FOOTER_HEIGHT + 3*CELL_SIZE 

BG_COLOR = [225, 229, 235]
TEXT_COLOR = [20, 20, 20]
SYMBOL_COLOR = TEXT_COLOR
CELL_DIVIDER_COLOR = [180, 180, 200]

def point_in_rect(point, rect_anchor, rect_span):
    return (rect_anchor[0] < point[0] < (rect_anchor[0] + rect_span[0])) and (rect_anchor[1] < point[1] < (rect_anchor[1] + rect_span[1]))

class PygameButton:
    BUTTON_DARK_SHIFT = Vector3(50, 50, 50)
    BUTTON_LIGHT_SHIFT = Vector3(15, 15, 15)

    def __init__(self, text, size, position, color):
        self.screen = pygame.display.get_surface()
        font = pygame.font.SysFont("Arial", 16)

        self.text = font.render(text, True, TEXT_COLOR)
        self.size = size
        self.position = Vector2(position)

        self.color = Vector3(color)
        self.color_dark = self.color - PygameButton.BUTTON_DARK_SHIFT
        self.color_light = self.color + PygameButton.BUTTON_LIGHT_SHIFT

    def draw(self):
        mouseHovering = self.mouse_hovering()
        mouseDown = pygame.mouse.get_pressed()[0] and mouseHovering

        dx = Vector2(self.size[0], 0)
        dy = Vector2(0, self.size[1])

        if mouseDown:
            pygame.draw.rect(self.screen, self.color_dark, pygame.Rect(self.position, self.size))
            pygame.draw.line(self.screen, self.color, self.position + dx, self.position + self.size)
            pygame.draw.line(self.screen, self.color, self.position + dy, self.position + self.size)
        elif mouseHovering:
            pygame.draw.rect(self.screen, self.color_light, pygame.Rect(self.position, self.size))
            pygame.draw.line(self.screen, self.color_dark, self.position + dx, self.position + self.size)
            pygame.draw.line(self.screen, self.color_dark, self.position + dy, self.position + self.size)
        else:
            pygame.draw.rect(self.screen, self.color, pygame.Rect(self.position, self.size))
            pygame.draw.line(self.screen, self.color_dark, self.position + dx, self.position + self.size)
            pygame.draw.line(self.screen, self.color_dark, self.position + dy, self.position + self.size)

        text_x = self.text.get_size()[0]
        offset = 0.5 * (self.size[0] - text_x)

        self.screen.blit(self.text, self.position + Vector2(offset, 0))

    def mouse_hovering(self):
        mousePos = pygame.mouse.get_pos()
        return point_in_rect(mousePos, self.position, self.size)

class PyTicTacToe:
    def __init__(self):
        print("Launching PyTicTacToe")

        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")

        self.font = pygame.font.SysFont("Arial", 20)

        self.screen = pygame.display.set_mode([WINDOW_SIZE_X, WINDOW_SIZE_Y])

        self.reset()

        # Precalculate cell anchors
        self.cellAnchors = []

        for i in range(0, 3):
            for j in range(0, 3):
                self.cellAnchors.append([MARGIN_WIDTH + j*CELL_SIZE, HEADER_HEIGHT + i*CELL_SIZE])

        resetButtonTL = Vector2(MARGIN_WIDTH + (CELL_SIZE/2), WINDOW_SIZE_Y - (2/3.0)*FOOTER_HEIGHT)
        resetButtonSize = Vector2(2 * CELL_SIZE, (1.0/3)*FOOTER_HEIGHT)
        self.resetButton = PygameButton("Reset", resetButtonSize, resetButtonTL, [214, 73, 69])

        x = pygame.image.load("x.png")
        x = pygame.transform.scale(x, (CELL_SIZE, CELL_SIZE))
        self.xSymbol = x.convert_alpha()

        o = pygame.image.load("o.png")
        o = pygame.transform.scale(o, (CELL_SIZE, CELL_SIZE))
        self.oSymbol = o.convert_alpha()

        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.MOUSEBUTTONUP:
                # Calculate if we clicked a cell
                mousePos = Vector2(pygame.mouse.get_pos())

                if point_in_rect(mousePos, [MARGIN_WIDTH, HEADER_HEIGHT], [3 * CELL_SIZE, 3 * CELL_SIZE]):
                    mousePos -= Vector2([MARGIN_WIDTH, HEADER_HEIGHT])
                    cellX = int(mousePos[0] // CELL_SIZE)
                    cellY = int(mousePos[1] // CELL_SIZE)
                    cellIndex = cellX + 3*cellY

                    if 0 <= cellIndex <= 8:
                        self.user_clicked_square(cellIndex)
                        self.update_text()

                if self.resetButton.mouse_hovering():
                    self.reset()

            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_r]:
                    self.reset()

            self.resetButton.draw()

            pygame.display.flip()

    def reset(self):
        self.reset_values()
        self.update_gui()
        self.update_text()

    def reset_values(self):
        self.playerTurn = 0
        self.headerText = "Player 1's Turn"
        self.cells = {i:None for i in range(0, 9)}
        self.moveCount = 0
        self.canPlay = True

    def update_gui(self):
        self.screen.fill(BG_COLOR)

        # Draw lines between cells
        tl = Vector2([MARGIN_WIDTH, HEADER_HEIGHT])
        tr = Vector2([WINDOW_SIZE_X - MARGIN_WIDTH, HEADER_HEIGHT])
        bl = Vector2([MARGIN_WIDTH, WINDOW_SIZE_Y - FOOTER_HEIGHT])
        br = Vector2([WINDOW_SIZE_X - MARGIN_WIDTH, WINDOW_SIZE_Y - FOOTER_HEIGHT])

        dx = Vector2([CELL_SIZE, 0])
        dy = Vector2([0, CELL_SIZE])

        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, tl, tr)
        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, tl, bl)
        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, bl, br)
        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, br, tr)

        # 4 dividing lines
        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, tl + dy, tr + dy)
        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, tl + 2*dy, tr + 2*dy)

        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, tl + dx, bl + dx)
        pygame.draw.aaline(self.screen, CELL_DIVIDER_COLOR, tl + 2*dx, bl + 2*dx)

    def update_text(self):
        self.screen.fill(BG_COLOR, pygame.Rect((0, 0), (WINDOW_SIZE_X, HEADER_HEIGHT)))

        ttSurface = self.font.render(self.headerText, True, TEXT_COLOR)
        ttSurfaceSize = ttSurface.get_size()
        ttOffsetX = (0.5)*(WINDOW_SIZE_X - ttSurfaceSize[0])
        ttOffsetY = (0.5)*(HEADER_HEIGHT - ttSurfaceSize[1])
        self.screen.blit(ttSurface, Vector2(ttOffsetX, ttOffsetY))

    def user_clicked_square(self, index):
        if not self.canPlay:
            return

        if self.cells[index] is not None:
            return

        self.cells[index] = self.playerTurn

        # draw symbol
        if self.playerTurn == 0:
            pygame.Surface.blit(self.screen, self.oSymbol, self.cellAnchors[index])

        if self.playerTurn == 1:
            pygame.Surface.blit(self.screen, self.xSymbol, self.cellAnchors[index])

        self.moveCount += 1

        if self.check_for_victory():
            self.canPlay = False
            return
        elif self.moveCount == 9: # board is filled
            self.canPlay = False
            self.headerText = "TIE!"
            self.update_text()
            return
        else:
            self.playerTurn = self.moveCount % 2
            self.headerText = "Player {}'s Turn".format(self.playerTurn + 1)
            self.update_text()

    def check_for_victory(self):
        lines = (
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6)
        )

        for line in lines:
            if self.cells[line[0]] is not None and self.cells[line[0]] == self.cells[line[1]] == self.cells[line[2]]:
                self.headerText = "PLAYER {} WINS!".format(self.playerTurn + 1)
                self.update_text()
                return True

if __name__ == "__main__":
    PyTicTacToe()