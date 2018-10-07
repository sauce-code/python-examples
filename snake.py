from tkinter import *
import random


class Apple:

    def __init__(self):
        self.x = random.randint(1, App.BOARD_WIDTH - 2)
        self.y = random.randint(1, App.BOARD_HEIGHT - 2)

    def create_new_apple(self):
        self.x = random.randint(1, App.BOARD_WIDTH - 2)
        self.y = random.randint(1, App.BOARD_HEIGHT - 2)
          
    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
        

class Snake:

    KEYS = ["w", "a", "s", "d"]
    MAP_KEY_OPP = {"w": "s", "a": "d", "s": "w", "d": "a"}

    def __init__(self, apple):
        self.apple = apple
        self.x = [20, 20, 20]
        self.y = [20, 21, 22]
        self.length = 3
        self.key_current = "w"
        self.key_last = self.key_current
        self.points = 0

    def move(self):  # move and change direction with wasd

        self.key_last = self.key_current

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.key_current == "w":
            self.y[0] = self.y[0] - 1

        elif self.key_current == "s":
            self.y[0] = self.y[0] + 1

        elif self.key_current == "a":
            self.x[0] = self.x[0] - 1

        elif self.key_current == "d":
            self.x[0] = self.x[0] + 1

        self.eat_apple()

    def eat_apple(self):

        if self.x[0] == self.apple.get_x() and self.y[0] == self.apple.get_y():

            self.length = self.length + 1

            x = self.x[len(self.x) - 1]  # snake grows
            y = self.y[len(self.y) - 1]
            self.x.append(x + 1)
            self.y.append(y)

            self.points = self.points + 1
            self.apple.create_new_apple()

    def check_game_over(self):

        for i in range(1, self.length, 1):

            if self.y[0] == self.y[i] and self.x[0] == self.x[i]:
                return True  # snake ate itself

        if self.x[0] < 1 or self.x[0] >= App.BOARD_WIDTH - 1 or self.y[0] < 1 or self.y[0] >= App.BOARD_HEIGHT - 1:
            return True  # snake out of bounds

        return False

    def set_key_event(self, event):

        if event.char in Snake.KEYS and event.char != Snake.MAP_KEY_OPP[self.key_last]:
            self.key_current = event.char

    def get_x(self, index):
        return self.x[index]

    def get_y(self, index):
        return self.y[index]

    def get_length(self):
        return self.length

    def get_points(self):
        return self.points


class App(Tk):

    BOARD_WIDTH = 30
    BOARD_HEIGHT = 30
    TILE_SIZE = 10

    TITLE = "Snake"
    COLOR_BACKGROUND = "yellow"
    COLOR_SNAKE_HEAD = "red"
    COLOR_SNAKE_BODY = "blue"
    COLOR_APPLE = "green"
    COLOR_FONT = "darkblue"
    FONT = "Times 20 italic bold"

    TICK_RATE = 200  # in ms
    
    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        Tk.__init__(self, screenName, baseName, className, useTk, sync, use)
        
        self.apple = Apple()
        self.snake = Snake(self.apple)

        self.canvas = Canvas(self, width=App.BOARD_WIDTH * App.TILE_SIZE, height=App.BOARD_HEIGHT * App.TILE_SIZE)
        self.canvas.pack()
        self.canvas.configure(background=App.COLOR_BACKGROUND)
    
        self.title(App.TITLE)
        self.bind('<KeyPress>', self.snake.set_key_event)

    def mainloop(self, n=0):
        self.gameloop()
        Tk.mainloop(self, n)

    def gameloop(self):

        self.after(App.TICK_RATE, self.gameloop)
        self.canvas.delete(ALL)

        if not self.snake.check_game_over():

            self.snake.move()
            self.snake.check_game_over()

            self.canvas.create_rectangle(
                self.snake.get_x(0) * App.TILE_SIZE,
                self.snake.get_y(0) * App.TILE_SIZE,
                self.snake.get_x(0) * App.TILE_SIZE + App.TILE_SIZE,
                self.snake.get_y(0) * App.TILE_SIZE + App.TILE_SIZE,
                fill=App.COLOR_SNAKE_HEAD
            )  # Head

            for i in range(1, self.snake.get_length(), 1):
                self.canvas.create_rectangle(
                    self.snake.get_x(i) * App.TILE_SIZE,
                    self.snake.get_y(i) * App.TILE_SIZE,
                    self.snake.get_x(i) * App.TILE_SIZE + App.TILE_SIZE,
                    self.snake.get_y(i) * App.TILE_SIZE + App.TILE_SIZE,
                    fill=App.COLOR_SNAKE_BODY
                )  # Body

            self.canvas.create_rectangle(
                self.apple.get_x() * App.TILE_SIZE,
                self.apple.get_y() * App.TILE_SIZE,
                self.apple.get_x() * App.TILE_SIZE + App.TILE_SIZE,
                self.apple.get_y() * App.TILE_SIZE + App.TILE_SIZE,
                fill=App.COLOR_APPLE
            )  # Apple

        else:  # GameOver Message
            x = App.BOARD_WIDTH * App.TILE_SIZE / 2  # x coordinate of screen center
            y = App.BOARD_HEIGHT * App.TILE_SIZE / 2  # y coordinate of screen center
            self.canvas.create_text(x, y - 25, fill=App.COLOR_FONT, font=App.FONT, text="GameOver!")
            self.canvas.create_text(x, y + 25, fill=App.COLOR_FONT, font=App.FONT,
                                    text="Points: " + str(self.snake.get_points()))
    

if __name__ == "__main__":
    App().mainloop()
