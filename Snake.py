import pygame as pg
import random as rd

pg.init()

from pygame.locals import (
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
)

WIDTH = 6
HEIGHT = 6
SCALE = 40

class Snake:

	def __init__(self, x, y, l):
		self.xpos = x
		self.ypos = y
		self.leng = l
		self.body = []
		self.momentum = "D"
		self.birth()

	def birth(self):
		for i in range(self.leng):
			self.body.append((self.xpos, self.ypos - self.leng + i + 1))

	def update(self, dir = "", grow = False):
		if dir:
			self.momentum = dir

		if self.momentum == "U":
			self.ypos -= 1
		elif self.momentum == "D":
			self.ypos += 1
		elif self.momentum == "L":
			self.xpos -= 1
		elif self.momentum == "R":
			self.xpos += 1

		if not grow: 
			self.body.pop(0)
		else:
			self.leng += 1
		self.body.append((self.xpos, self.ypos))

	def print(self):
		for i in self.body:
			print(i)
		print()

class SnakeGame:

	def __init__(self, w, h, s):
		self.gw = w
		self.gh = h
		self.dw = w * s
		self.dh = h * s
		self.scale = s
		self.snek = Snake(self.gw // 2, self.gh // 2, 5)
		self.apple = (self.gw // 2, self.gh // 3)
		self.Main()

	def Main(self):
		window = pg.display.set_mode((self.dw, self.dh))
		windowclock = pg.time.Clock()

		running = True

		while running:
			window.fill((255, 255, 255))

			self.draw_board(window)

			dir = ""
			grow = False

			for event in pg.event.get():
				if event.type == KEYDOWN:
					if event.key == K_UP:
						dir = "U"
					if event.key == K_DOWN:
						dir = "D"
					if event.key == K_LEFT:
						dir = "L"
					if event.key == K_RIGHT:
						dir = "R"
				elif event.type == pg.QUIT:
					running = False

			if self.snek.body[-1] == self.apple:
				grow = True
				while True:
					self.apple = (rd.randint(0, self.gw - 1), rd.randint(0, self.gh - 1))
					if not self.apple in self.snek.body:
						break

			if dir:
				self.snek.update(dir, grow)
			else:
				self.snek.update(grow = grow)

			if self.check_victory():
				print("YOU WIN!!!")
				running = False

			if self.check_death():
				print("You lose")
				running = False

			self.draw_apple(window)
			self.draw_snake(window)

			pg.display.flip()
			windowclock.tick(3)
		pg.quit()

	def draw_board(self, window):
		for i in range(self.gw):
				for j in range(self.gh):
					surf = pg.Surface((self.scale, self.scale))
					if (i + j) % 2 == 0:
						surf.fill((200, 200, 200))
					else:
						surf.fill((170, 170, 170))
					window.blit(surf, (i * self.scale, j * self.scale))

	def draw_snake(self, window):
		for i in range(self.snek.leng):
			surf = pg.Surface((self.scale, self.scale))
			surf.fill((200, 50, 50))
			window.blit(surf, (self.snek.body[i][0] * self.scale, self.snek.body[i][1] * self.scale))

	def draw_apple(self, window):
		surf = pg.Surface((self.scale, self.scale))
		surf.fill((50, 200, 50))
		window.blit(surf, (self.apple[0] * self.scale, self.apple[1] * self.scale))

	def check_death(self):
		if len(self.snek.body) != len(set(self.snek.body)):
			return True
		elif self.snek.xpos < 0 or self.snek.ypos < 0 or self.snek.xpos >= self.gw or self.snek.ypos >= self.gh:
			return True
		return False

	def check_victory(self):
		print(self.snek.leng)
		return self.snek.leng == self.gw * self.gh


def main():
	s = SnakeGame(WIDTH, HEIGHT, SCALE)

if __name__ == '__main__':
	main()