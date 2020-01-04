import pygame,sys

from window import Window, BaseWindow
from gameplay import GamePlay
from leaderbord import LeaderBoard
from mainMenu import MainMenu
from controlsDescription import ControlsDescription

pygame.init()


def main():
	w,h = 400,600
	screen = pygame.display.set_mode((w,h))

	windows={"MainMenu":MainMenu, "LeaderBoard":LeaderBoard, "GamePlay":GamePlay, "ControlsDescription":ControlsDescription, "BaseWindow":BaseWindow}

	Window.setWindow(MainMenu())


	running=True
	while running:
		Window.current.clock.tick(Window.current.fps)

		for ev in pygame.event.get():
			if ev.type == pygame.QUIT:
				running = False
			if ev.type == pygame.KEYDOWN:
				if ev.key == pygame.K_ESCAPE:
					running = False

			Window.current.checkEvents(ev)

		Window.current.update()
		Window.current.draw(screen)

		if not isinstance(Window.current, windows[Window.name]):
			className = windows[Window.name]
			Window.setWindow(className())

		pygame.display.update()

if __name__ =="__main__":
	main()