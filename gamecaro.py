import pygame as pg
import random
import numpy as np
import copy
import sys


class Labal():
    def __init__(self, screen, x, y, width, height, labalText='Labal', borderradix=-1, bg="#ffffff", cg=(20, 20, 20)):
        self.x = x
        self.y = y
        self.screen = screen
        self.width = width
        self.height = height
        self.alreadyPressed = False
        self.bg = bg
        self.cg = cg
        self.borderradix = borderradix
        font = pg.font.SysFont('Times New Roman', 20, bold=True)
        self.lbSurf = font.render(labalText, True, self.cg)

    def drawlb(self):
        self.lbRect = pg.Rect(self.x, self.y, self.width, self.height)
        self.text_rect = self.lbSurf.get_rect(center=self.lbRect.center)
        pg.draw.rect(self.screen, self.bg, self.lbRect,
                     border_radius=self.borderradix)
        self.screen.blit(self.lbSurf, self.text_rect)

    def setWidth(self, width):
        self.width = width


class Button:
    def __init__(self, screen, text, translation, width, height, pos, elevation=0, clickfunction=None):
        # Core attributes
        self.screen = screen
        self.clickfunction = clickfunction
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pg.Rect(pos, (width, height))
        self.top_color = '#475F77'
        self.translation = translation
        # bottom rectangle
        self.bottom_rect = pg.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text = text
        self.font = pg.font.SysFont('Times New Roman', 20, bold=True)
        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def change_text(self, newtext):
        self.text_surf = self.font.render(newtext, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pg.draw.rect(self.screen, self.bottom_color,
                     self.bottom_rect, border_radius=12)
        pg.draw.rect(self.screen, self.top_color,
                     self.top_rect, border_radius=12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pg.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pg.mouse.get_pressed()[0]:
                # sự kiện giữ chuột trái
                self.dynamic_elecation = 0
                self.pressed = True
                self.change_text(f"{self.translation}")
            else:
                # sự kiện ấn chuốt trái
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    self.change_text(self.text)
                    self.clickfunction()
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'


map = np.zeros((20, 20), dtype=np.int32)

class Game1x1:
    def __init__(self, screen):
        self.map = copy.deepcopy(map)
        self.lenmap = [len(self.map)*31, len(self.map[0])*31]
        self.screen = screen
        self.imgs = []
        self.imgs.append(pg.transform.scale(pg.image.load(
            ".\img\symbol-check-icon.png"), (31, 31)))
        self.imgs.append(pg.transform.scale(pg.image.load(
            ".\img\delete-icon.png"), (31, 31)))
        self.player = 1
        self.cooldown = 0
        self.barcooldown = Labal(self.screen, 630, 500, 160, 30, "", 2, "blue")
        self.lbl = Labal(self.screen, x=650, y=100, width=120, height=40, labalText="Lượt",
                         cg=(255, 0, 0), bg="#00f5ff", borderradix=6)
        self.newbutton = Button(self.screen, 'New game',
                                'New game', 100, 30, (660, 350), clickfunction=self.__reset)
        self.exitbutton = Button(self.screen, 'Exit game',
                                 'Exit game', 100, 30, (660, 400), clickfunction=self.__exit)
        self.checkpoint = [0, 0]
        self.playerwin = 0

    def update(self, event):
        self.event = event
        self.playerisclikMouse()
        self.draw()
        if self.playerwin == 0:
            self.__checkwin()
        self.__turns()
        self.__coolDown()
        self.__drawWinLoss()

    def __coolDown(self):
        self.cooldown += 1
        width = 160-(self.cooldown/16)
        self.barcooldown.setWidth(width)
        self.barcooldown.drawlb()
        if width < 0:
            x = random.randrange(0, self.lenmap[0])
            y = random.randrange(0, self.lenmap[1])
            self.checkpoint = [x//31, y//31]
            self.map[self.checkpoint[0]
                     ][self.checkpoint[1]] = self.player
            self.cooldown = 0

    def __turns(self):
        sum = np.count_nonzero(self.map == 0)
        if sum % 2 == 0:
            self.player = 1
        else:
            self.player = 2

    def playerisclikMouse(self):
        x_mouse, y_mouse = pg.mouse.get_pos()
        if 0 <= x_mouse < self.lenmap[0] and 0 <= y_mouse < self.lenmap[1]:
            if self.map[y_mouse//31][x_mouse//31] == 0 and self.event.type == pg.MOUSEBUTTONDOWN:
                state_mouse = pg.mouse.get_pressed()
                if state_mouse[0]:
                    self.checkpoint = [y_mouse//31, x_mouse//31]
                    self.map[self.checkpoint[0]
                             ][self.checkpoint[1]] = self.player
                    self.cooldown = 0

    def __checkwin(self):
        countrow = 1
        coutcolum = 1
        coutcrossleft = 1
        coutcrossright = 1
        i = self.checkpoint[0]
        j = self.checkpoint[1]
        type = self.map[i][j]
        lenx = self.lenmap[0]//31-1
        leny = self.lenmap[1]//31-1
        if type != 0:
            x = i
           # kiểm tra cột
            while (x > 0) and (self.map[x-1][j] == type):
                coutcolum = coutcolum+1
                x = x-1
            x = i
            while (x < lenx) and (self.map[x+1][j] == type):
                coutcolum = coutcolum+1
                x = x+1
            # kiểm tra hàng
            y = j
            while (y > 0) and (self.map[i][y-1] == type):
                countrow = countrow+1
                y = y-1
            y = j
            while (y < leny) and (self.map[i][y+1] == type):
                countrow = countrow+1
                y = y+1
            # kiểm tra chéo trái
            y = j
            x = i
            while ((y > 0) and (x > 0)) and (self.map[x-1][y-1] == type):
                coutcrossleft = coutcrossleft+1
                y = y-1
                x = x-1
            y = j
            x = i
            while ((y < leny) and (x < lenx)) and (self.map[x+1][y+1] == type):
                coutcrossleft = coutcrossleft+1
                y = y+1
                x = x+1
            # kiểm tra chéo phải
            y = j
            x = i
            while ((y < leny) and (x > 0)) and (self.map[x-1][y+1] == type):
                coutcrossright = coutcrossright+1
                y = y+1
                x = x-1
            y = j
            x = i
            while ((y > 0) and (x < lenx)) and (self.map[x+1][y-1] == type):
                coutcrossright = coutcrossright+1
                y = y-1
                x = x+1
            if coutcolum == 5 or countrow == 5 or coutcrossleft == 5 or coutcrossright == 5:
                if(type == 1):
                    self.playerwin = 1
                elif(type == 2):
                    self.playerwin = 2

    def draw(self):
        x = self.lenmap[0]
        y = self.lenmap[0]
        pg.draw.rect(self.screen, 'white',
                     (0, 0, x, y))
        x_mouse, y_mouse = pg.mouse.get_pos()
        if 0 <= x_mouse < self.lenmap[0] and 0 <= y_mouse < self.lenmap[1]:
            pg.draw.rect(self.screen, (252, 225, 142),
                         (x_mouse//31*31, y_mouse//31*31, 31, 31))
        for i in range(0, x+31, 31):
            pg.draw.line(self.screen, "black", [i, 0], [i, x])  # draw line row
            for j in range(0, y+31, 31):
                pg.draw.line(self.screen, "black", [
                             0, j], [y, j])  # draw line col
                if i < x and j < y:
                    if self.map[i//31][j//31] == 1:
                        self.screen.blit(self.imgs[0], (j, i))
                    elif self.map[i//31][j//31] == 2:
                        self.screen.blit(self.imgs[1], (j, i))
        if self.player == 1:
            self.screen.blit(self.imgs[0], (695, 150))
        if self.player == 2:
            self.screen.blit(self.imgs[1], (695, 150))
        self.lbl.drawlb()
        self.newbutton.draw()
        self.exitbutton.draw()

    def __reset(self):
        self.playerwin = 0
        self.cooldown = 0
        self.checkpoint = [0, 0]
        self.map = copy.deepcopy(map)

    def __exit(self):
        quit()

    def __drawWinLoss(self):
        if self.playerwin != 0:
            imgs = []
            imgs.append(pg.transform.scale(pg.image.load(
                ".\img\Lovepik_com-401644461-win-victory-champion-word-design.png"), (500, 500)))
            imgs.append(pg.transform.scale(pg.image.load(
                ".\img\pngegg.png"), (500, 500)))
            if self.playerwin == 1:
                self.screen.blit(imgs[0], (10, 30))
            else:
                self.screen.blit(imgs[1], (10, 30))
