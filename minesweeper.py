import os
import sys
import tkinter as tk
import random
from PIL import Image, ImageTk
import time
from playsound import playsound

# create window
window = tk.Tk()

#create lists of tiles
coords = [[None]*20 for i in range(15)]
tiles = []

firstClick = True
gameOver = False

numClicked = 0

#tile class
class Tile(object):
    def __init__(self, master, y, x, bgColor, hoverColor):
        self.drawing = tk.Label(master=master, bg=bgColor, bd=0, width=2, height=2)
        self.isMine = False
        self.markedMine = False
        self.isClicked = False
        # tile colors
        self.color = self.drawing['background']
        self.hoverColor = hoverColor
        if self.color == '#a2d149':
            self.clickColor = '#d7b899'
        elif self.color == '#aad751':
            self.clickColor = '#e5c29f'
        #hovering and clicking tiles
        self.drawing.bind("<Enter>", self.on_enter)
        self.drawing.bind("<Leave>", self.on_leave)
        self.drawing.bind("<Button-1>", self.left_click)
        self.drawing.bind("<Button-2>", self.right_click)
        self.drawing.bind("<Button-3>", self.right_click)

        #create 2d list of tiles
        self.x = x
        self.y = y
        coords[y][x] = self

    #change color when hovering
    def on_enter(self, e):
        self.drawing['background']=self.hoverColor

    def on_leave(self, e):
        self.drawing['background']=self.color

    #randomly place mines
    def placeMines(self):
        chance = [0, 0, 0, 0, 0, 1]
        num = random.choice(chance)
        if num == 1:
            self.isMine = True
            self.clickColor = 'red'

    #left click
    def left_click(self, e):
        global firstClick
        global gameOver
        global numClicked

        #place mines and spread tiles after first click
        if gameOver == False:
            if firstClick == True:
                near = self.nearTiles()
                near.append(self)

                for tile in tiles:
                    if not tile in near:
                        tile.placeMines()

                for tile in tiles:
                    tile.nearMines()

                #start timer and mine counter
                global start
                start = time.time()

                window.after(1, showMines)
                window.after(1, showTime)
                firstClick = False

            #game is lost if mine is clicked
            if self.isMine == True and self.markedMine == False:
                gameOver = True
                playsound("assets/minesweeperassets/sounds_gameLose.mp3", block=False)
                for tile in tiles:
                    if tile.isMine == True:
                        tile.click()
                tk.Label(window, text='You Lost.', font=('Fixedsys', 36, 'bold'), anchor='n', fg='white', bg='#4a752c',
                         pady=20, width=12, height=2).grid(row=4, column=5, rowspan=7, columnspan=10)
                tk.Label(window, image=clock, bg='#4a752c').grid(row=7, column=8, columnspan=2, rowspan=2)
                tk.Label(window, text='---', font=('Fixedsys', 24, 'bold'), fg='white', bg='#4a752c').grid(
                    row=7, column=9, columnspan=3, rowspan=2)
                tk.Button(window, text='⭮ Try Again', font=('Fixedsys', 24), command=self.restart, fg='white',
                          bg='#4a752c', bd=0, padx=25, pady=15).grid(row=9, column=6, columnspan=8, rowspan=3)

            #spread mines if regular click
            if gameOver == False:
                if self.markedMine == False:
                    if self.numMines == 0:
                        self.spread()
                    self.click()

                #click sound
                playsound("assets/minesweeperassets/sounds_click.wav", block=False)

                #game is won if all non-mine tiles are clicked
                total = totalMines()
                if numClicked == 300-total:
                    gameOver = True
                    playsound("assets/minesweeperassets/sounds_gameWin.wav", block=False)
                    tk.Label(window, text='You win!', font=('Fixedsys', 36, 'bold'), anchor='n', fg='white', bg='#4a752c',
                             pady=20, width=12, height=2).grid(row=4, column=5, rowspan=7, columnspan=10)

                    text = timeLabel['text']

                    tk.Label(window, image=clock, bg='#4a752c').grid(row=7, column=8, columnspan=2, rowspan=2)
                    tk.Label(window, text=text, font=('Fixedsys', 30, 'bold'), fg='white', bg='#4a752c').grid(
                        row=7, column=9, columnspan=4, rowspan=2)
                    tk.Button(window, text='⭮ Try Again', font=('Fixedsys', 24), command=self.restart, fg='white',
                              bg='#4a752c', bd=0, padx=25, pady=15).grid(row=9, column=6, columnspan=8, rowspan=3)

    #click tile
    def click(self):
        if self.isClicked == False:
            global numClicked
            self.color = self.clickColor
            self.drawing['background']=self.clickColor
            self.hoverColor=self.clickColor

            if self.numMines > 0:
                if self.isMine == False:
                    self.num = tk.Label(window, text=self.numMines, font=('Helvetica', 26, 'bold'), fg=self.numColor,
                                        bg=self.drawing['background']).grid(row=self.y + 2, column=self.x)

            self.isClicked = True
            numClicked += 1

    #find nearby tiles
    def nearTiles(self):
        nearTiles = []

        nearX = [self.x-1, self.x, self.x+1]
        nearY = [self.y-1, self.y, self.y+1]

        for x in nearX:
            for y in nearY:
                for tile in tiles:
                    if ((tile.x, tile.y) == (x, y)) and (tile != self):
                            nearTiles.append(tile)
        return nearTiles

    #spread until all edge tiles have nearby mines
    def spread(self):
        nearTiles = self.nearTiles()
        while True:
            lastLen = len(nearTiles)
            for nearTile in nearTiles:
                if nearTile.numMines == 0:
                    nextNears = nearTile.nearTiles()
                    for nextNear in nextNears:
                        if nextNear.isMine == False:
                            if not nextNear in nearTiles:
                                nearTiles.append(nextNear)
            newLen = len(nearTiles)

            if lastLen == newLen:
                break
        for tile in nearTiles:
            tile.click()

    #find number of nearby mines
    def nearMines(self):
        self.numMines = 0

        nearTiles = self.nearTiles()
        for tile in nearTiles:
            if tile.isMine == True:
                self.numMines += 1

        if self.numMines > 0:
            if self.isMine == False:

                if self.numMines == 1:
                    self.numColor = '#1975d2'
                if self.numMines == 2:
                    self.numColor = '#388e3c'
                if self.numMines == 3:
                    self.numColor = '#d32f2f'
                if self.numMines == 4:
                    self.numColor = '#7b1fa2'
                if self.numMines == 5:
                    self.numColor = '#fc8f02'
                if self.numMines == 6:
                    self.numColor = '#1a97a7'
                if self.numMines == 7:
                    self.numColor = '#464544'

    #mark mines with right click
    def right_click(self, e):
        global flag
        global gameOver
        if gameOver == False:
            if self.isClicked == False:
                if self.markedMine == False:
                    self.drawing.configure(image=flag, width=16, height=32)
                    self.markedMine = True
                    playsound("assets/minesweeperassets/sounds_flag.wav", block=False)
                elif self.markedMine == True:
                    self.drawing.configure(image='', width=2, height=2)
                    self.markedMine = False
                    playsound("assets/minesweeperassets/sounds_unflag.wav", block=False)

    #restart program
    def restart(self):
        window.destroy()
        os.execl(sys.executable, 'python', "minesweeper.py", *sys.argv[1:])

#title
tk.Label(window, text='Minesweeper', font=('Fixedsys', 29), fg='white', bg='#4a752c', width=44).grid(
    row=0, column=0, columnspan=20, rowspan=2, ipadx=17, ipady=8)

#create tiles
for y in range(15):
    for x in range(20):
        if (y%2 == 0 and x%2 != 0) or (y%2 != 0 and x%2 == 0):
            bgColor = '#a2d149'
            hoverColor = '#b9dd77'
        else:
            bgColor = '#aad751'
            hoverColor = '#bfe17d'
        tile = Tile(window, y, x, bgColor, hoverColor)
        tiles.append(tile)
        tile.drawing.grid(row=y+2, column=x, ipadx=15, ipady=8)

#flag image for counter and marking mines
flag = Image.open("assets/minesweeperassets/minesweeperflag.png")
flag = flag.convert("RGBA")

pixels = flag.getdata()
newPixels = []
for pixel in pixels:
    if pixel[0] < 220:
        newPixels.append((255, 255, 255, 0))
    else:
        newPixels.append(pixel)
flag.putdata(newPixels)
flag = ImageTk.PhotoImage(flag)

#mine counter
tk.Label(window, image=flag, bg='#4a752c', width=33).grid(row=0, column=0, columnspan=3)
minesLabel = tk.Label(window, text="=  ??? ", font=('Fixedsys', 18), fg='white', bg='#4a752c')
minesLabel.grid(row=0, column=2, columnspan=2)

#count mines
def totalMines():
    totalMines = 0
    for tile in tiles:
        if tile.isMine == True:
            totalMines += 1
    return totalMines

#update mine counter every 100ms
def showMines():
    numMines = 0
    for tile in tiles:
        if tile.isMine == True and tile.markedMine == False:
            numMines += 1
    minesLabel.config(text="=  " + str(numMines)+"  ")
    window.after(100, showMines)

#clock image for time counter
clock = Image.open("assets/minesweeperassets/minesweeperclock.png")
clock = clock.resize((41, 51))
clock = ImageTk.PhotoImage(clock)

#time counter
tk.Label(window, image=clock, bg='#4a752c').grid(row=0, column=15, columnspan=3)

start = 0
timeLabel = tk.Label(window, text='000  ', font=('Fixedsys', 18), fg='white', bg='#4a752c')
timeLabel.grid(row=0, column=17, columnspan=2)

#update time counter every second
def showTime():
    if gameOver == False:
        current = time.time()
        timePassed = str(int(current-start))
        if int(timePassed) <= 999:
            if len(timePassed) == 1:
                timeLabel.config(text='00'+timePassed+'  ')
            elif len(timePassed) == 2:
                timeLabel.config(text='0'+timePassed+'  ')
            elif len(timePassed) == 3:
                timeLabel.config(text=timePassed+'  ')

        window.after(1000, showTime)


# show window
window.mainloop()
