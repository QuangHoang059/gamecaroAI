import pygame as pg
import random
import numpy as np
import copy
import os
import ctypes
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the DLL file
dll_path = os.path.join(script_dir, 'brain.dll')
brain = ctypes.CDLL(dll_path)
brain.minmaxalphabeta.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
brain.minmaxalphabeta.restype = ctypes.c_float
brain.getLegalActions.argtypes = [
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int)
]
brain.getLegalActions.restype = ctypes.c_int
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

eval = {2: [9999999999, 900, 900, 900, 900, 700, 700, 700, 900, 300, 300, 50, 300, 300, 300, 300, 300, 250, 250, 200, 200, 200, 10, 300, 50],
        1: [-9999999999, -900, -900, -900, -900, - 700, - 700, - 700, -900, -300, -300, -50, -300, -300, -300, -300, -300, - 250, -250, -200, -200, -200, - 10, -300, -50]
        }

lines = np.array([
    [3, 3, 3, 3, 3],

    [3, 3, 3, 3, 0],
    [3, 0, 3, 3, 3],
    [3, 3, 0, 3, 3],
    [3, 3, 3, 0, 3],

    [3, 3, 3, 0, 0],
    [3, 0, 3, 3, 0],
    [3, 3, 0, 3, 0],

    [3, 3, 3, 3, 5],
    [3, 5, 3, 3, 3],
    [3, 3, 3, 5, 3],
    [3, 3, 5, 3, 3],

    [3, 3, 3, 0, 5],
    [3, 3, 3, 5, 0],
    [3, 3, 3, 5, 5],
    [3, 0, 3, 3, 5],
    [3, 3, 0, 3, 5],

    [3, 3, 0, 0, 0],
    [3, 0, 3, 0, 0],

    [3, 3, 0, 0, 5],
    [3, 3, 0, 5, 5],
    [3, 0, 3, 0, 5],
    [3, 0, 3, 5, 5],

    [3, 3, 5, 5, 5],
    [3, 3, 5, 0, 5],
    [3, 3, 5, 0, 0],
    [3, 3, 5, 3, 5],
    [3, 5, 3, 3, 5],

    [3, 0, 5, 0, 0],
    [3, 5, 0, 0, 0],

])


def checkdraw(maps):
    return not np.any(maps == 0)


def getvalue(line, head, tail, player):
    line[line == player] = 3
    line[line == 3-player] = 5
    for i, l in enumerate(lines):
        if np.array_equal(line, l):
            if i == 0 and tail == 4 and head == 4:
                return 0
            elif 1 <= i <= 4:
                if tail == 4 and head == 4:
                    return 0
            elif 5 <= i <= 7:
                if tail == 4 and head == 4:
                    return 0
                elif head == 4:
                    return eval[player][-2]
            elif 8 <= i <= 11:
                if tail == 4 and head == 4:
                    return 0
                if (i == 8 or i == 11) and head == 4:
                    return 0
            elif 12 <= i <= 16:
                if head == 4:
                    return 0
            elif 17 <= i <= 18:
                if tail == 4 and head == 4:
                    return 0
                elif head == 4:
                    return eval[player][-1]
            elif 19 <= i <= 22:
                if head == 4:
                    return 0
            elif 23 <= i <= 27:
                return eval[player][-1]
            elif i >= 28:
                return eval[player][-3]
            return eval[player][i]
    return 0


def checkValuesALL(maps):
    lenx = len(maps)
    leny = len(maps[0])
    lineX = [1, 1, 0, 1]
    lineY = [0, 1, 1, -1]
    values = np.array([])
    for x in range(lenx):
        for y in range(leny):
            player = maps[x][y]
            if player != 0:
                for i in range(0, 4):
                    line = np.array([], dtype=int)
                    head = -1
                    tail = -1
                    line = np.append(line, player)
                    for j in [-1, 1, 2, 3, 4, 5]:
                        vtx = x + lineX[i]*j
                        vty = y + lineY[i]*j
                        if((vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny) and j == -1):
                            head = 4
                        elif j == -1 and maps[vtx][vty] == 3-player:
                            head = 4
                        elif j == -1 and maps[vtx][vty] == player:
                            head = player
                            break
                        if head == player:
                            break
                        if((vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny) and j == 5):
                            tail = 4
                        elif j == 5 and maps[vtx][vty] == 3-player:
                            tail = 4
                        if(vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny) and 1 <= j <= 4:
                            line = np.append(line, 4)
                        elif 1 <= j <= 4:
                            line = np.append(line, maps[vtx][vty])
                    if head == player:
                        continue
                    value = getvalue(
                        line, head, tail, player)
                    values = np.append(values, value)

    return values


def checkValue(maps, x, y, player, lenx, leny):
    lineX = [1, 1, 0, 1]
    lineY = [0, 1, 1, -1]
    values = np.array([])
    for i in range(0, 4):
        line = np.array([])
        head = -1
        tail = -1
        line = np.append(line, player)
        for j in [-1, 1, 2, 3, 4, 5]:
            vtx = x + lineX[i]*j
            vty = y + lineY[i]*j
            if((vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny) and j == -1):
                head = 4
            elif j == -1 and maps[vtx][vty] == 3-player:
                head = 4
            elif j == -1 and maps[vtx][vty] == player:
                head = player
                break
            if head == player:
                break
            if((vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny) and j == 5):
                tail = 4
            elif j == 5 and maps[vtx][vty] == 3-player:
                tail = 4
            if(vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny) and 1 <= j <= 4:
                line = np.append(line, 4)
            elif 1 <= j <= 4:
                line = np.append(line, maps[vtx][vty])
        value = getvalue(
            line, head, tail, player)
        values = np.append(values, abs(value))
    return values.max()


def checkwinAll(maps):
    lenx = len(maps)
    leny = len(maps[0])
    lineX = [1, 1, 0, 1]
    lineY = [0, 1, 1, -1]
    for x in range(lenx):
        for y in range(leny):
            player = maps[x][y]
            if player != 0:
                for i in range(0, 4):
                    count = 1
                    for j in range(1, 5):
                        vtx = x + lineX[i]*j
                        vty = y + lineY[i]*j
                        if(vtx < 0 or vty < 0 or vtx >= lenx or vty >= leny):
                            break
                        if(maps[vtx][vty] == player):
                            count += 1
                        else:
                            break
                    if(count == 5 and player == 1):
                        return 1
                    elif (count == 5 and player == 2):
                        return 2
    return None


def isEndnode(maps):
    if checkdraw(maps) or checkwinAll(maps) is None:
        return True
    return False


def Values(maps):
    values = checkValuesALL(maps)
    if len(values) > 0:
        max = np.amax(values)
        min = np.amin(values)
        if max > abs(min):
            return max
        elif abs(min) >= max:
            return min


def turns(maps):
    sum = np.count_nonzero(maps == 0)
    if sum % 2 == 0:
        return 1
    else:
        return 2


def move(maps, i, j):
    # mapcopy = copy.deepcopy(maps)
    # player = turns(mapcopy)
    # mapcopy[i][j] = player
    # return mapcopy
    player = turns(maps)
    maps[i][j] = player
    return maps


def getMove(maps, pl, space):
    lenx = len(maps)
    leny = len(maps[0])
    values = {}
    for x in range(lenx):
        for y in range(leny):
            if maps[x][y] != 0:
                continue
            value = checkValue(maps, x, y, pl, lenx, leny)
            values[x, y] = value
    t = list(sorted(values.items(), key=lambda item: item[1]))
    t = list(arr[0] for arr in t[-space:])
    return t


class GameAI:
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
        self.pos_compter = [14, 14]

    def update(self, event):
        self.event = event
        self.playerisclikMouse()
        self.__checkwin()
        self.__turns()
        self.__coolDown()
        self.draw()
        self.AI_X()
        # print(Values(self.map))

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
            pg.draw.rect(self.screen, (51, 187, 255),
                         (x_mouse//31*31, y_mouse//31*31, 31, 31))
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
        if 0 <= x_mouse < self.lenmap[0] and 0 <= y_mouse < self.lenmap[1] and self.player == 1:
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

    def AI_X(self):
        if self.player == 2:
            maps=copy.deepcopy(self.map)
            maps=maps.flatten()
            maps=(ctypes.c_int * len(maps))(*maps)
            actions=np.zeros((400,2), dtype=np.int32)
            actions=actions.flatten()
            actions =(ctypes.c_int * len(actions))(*actions)
            idx=brain.getLegalActions(maps,actions )
            actions=np.array(actions).reshape(400,2)[:idx,:]

            maxaction = 99999999999
            # result=[9,9]
            for action in actions:
                action_c =(ctypes.c_int * len(action))(*action)
                value=brain.minmaxalphabeta(maps,action_c,1,1,-9999999,9999999)
                print(value)
                if maxaction > value:
                    maxaction = value
                   
                    self.pos_compter = action
                # elif maxaction == value:
                #     if random.random() < 0.5:
                #         result = action
            # print( self.pos_compter)  
            # print(self.map)
            # if  self.pos_compter[0]!=0 and self.pos_compter[1]!=0:      
            self.map[ self.pos_compter[0]][ self.pos_compter[1]]=self.player 
            self.checkpoint=self.pos_compter
            # else:
            #     self.map[1][1]=self.player 
        # def Minmaxanphabeta( maps, dep, a, b, mp, pl):
        #     if dep == 0 or (isEndnode(maps) is None):
        #         return Values(maps)
        #     steps = getMove(maps, pl, 6)
        #     if mp == True:
        #         maxEva = -np.inf
        #         for step in steps:
        #             child = move(maps, step[0], step[1])
        #             tamp = Minmaxanphabeta(
        #                 child, dep-1, a, b, False,  1)
        #             print(tamp, step, 'max')
        #             if maxEva < tamp:
        #                 if dep == 3:
        #                     self.pos_compter = step
        #             maxEva = max(maxEva, tamp)
        #             a = max(a, maxEva)
        #             maps[step[0]][step[1]]=0
        #             if(a >= b):
        #                 break
        #         return maxEva
        #     elif mp == False:
        #         minEva = np.inf
        #         for step in steps:
        #             child = move(maps, step[0], step[1])
        #             tamp = Minmaxanphabeta(
        #                 child, dep-1, a, b, True, 2)
        #             print(tamp, step, 'min')
        #             minEva = min(minEva, tamp)
        #             b = min(b, minEva)
        #             maps[step[0]][step[1]]=0
        #             if(a >= b):
        #                 break
        #         return minEva
            
        # if self.player == 2:
        #     print(Minmaxanphabeta(
        #         maps, 3, -np.inf, np.inf, True, 2))
        #     self.map[self.pos_compter[0]
        #                 ][self.pos_compter[1]] = self.player
