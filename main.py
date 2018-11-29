import pygame
import os
import random
import numpy as np

from display import Display
from player import Player
from box import Box

WIDTH = 800
HEIGHT = 600

BOX_WIDTH = 60
BOX_HEIGHT = 60
BOX_DIST = 10
CHEQUE_WIDTH = 30
CHEQUE_HEIGHT = 15
DOC_WIDTH = 20
DOC_HEIGHT = 40

class Game:
  def __init__(self):
    # sets basic game features
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    # plays background song repeatedly
    # pygame.mixer.music.load("The Marching Pirate Spy.mp3")
    # pygame.mixer.music.play(-1, 0)

    # initialize display
    self.display = Display(pygame, 135, 115, WIDTH, HEIGHT, BOX_WIDTH, BOX_HEIGHT)

    self.initializeBoxes()
    self.docs = []

    # initialize player
    self.player = Player(135, 115, 5, 0)
    self.player.setRect(self.display.dogImages[0][0].get_rect())

    self.clock = pygame.time.Clock()
    self.keepPlaying = True

  def handleEvents(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.keepPlaying = False

      if event.type == self.boxSpawnEvent:
        self.spawnBox()

      if event.type == pygame.KEYDOWN and game.player.getAttack() == False:
        if event.key == pygame.K_LEFT:
          game.player.setAllMoveFalse()
          game.player.setMoveLeft(True)
        if event.key == pygame.K_RIGHT:
          game.player.setAllMoveFalse()
          game.player.setMoveRight(True)
        if event.key == pygame.K_UP:
          game.player.setAllMoveFalse()
          game.player.setMoveUp(True)
        if event.key == pygame.K_DOWN:
          game.player.setAllMoveFalse()
          game.player.setMoveDown(True)
        if event.key == pygame.K_SPACE:
          game.player.setAttack(True)
          self.docs += self.boxes[0].openBox()
          #game.player.setRect(game.player.getRect)
        
      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
          game.player.resetMoveX()
          game.player.setMoveLeft(False)
        if event.key == pygame.K_RIGHT:
          game.player.resetMoveX()
          game.player.setMoveRight(False)
        if event.key == pygame.K_UP:
          game.player.resetMoveY()
          game.player.setMoveUp(False)
        if event.key == pygame.K_DOWN:
          game.player.resetMoveY()
          game.player.setMoveDown(False)
        # if event.key == pygame.K_DOWN:
        #   game.player.setAttack(False)

    if (game.player.getMoveLeft()):
      game.player.moveX(-1)
    elif (game.player.getMoveRight()):
      game.player.moveX(1)
    elif (game.player.getMoveUp()):
      game.player.moveY(-1)
    elif (game.player.getMoveDown()):
      game.player.moveY(1)


  def updateBoxes(self):
    print('update')

  def updateDocuments(self):
    for d in self.docs:
      if d.getSpread() == True:
        d.spread()

  def spawnBox(self):
    for i in range(self.boxSpawnRate):
      size = np.random.choice(['B', 'S'], 1, replace=False, p=[self.bigBoxChance, self.smallBoxChance])[0]
      logo = random.randint(0, len(self.banks[size]) - 1)
      while True:
        randX = random.randint(10, WIDTH - 10 - BOX_WIDTH)
        randY = random.randint(10, HEIGHT - 10 - BOX_HEIGHT)
        rect = pygame.Rect(randX, randY, BOX_WIDTH, BOX_HEIGHT)
        box_rects = list(map(lambda b: b.getRect(), self.boxes))
        if (rect.collidelist(box_rects) < 0):
          self.boxes.append(Box(size, self.banks[size][logo], rect))
          break

  def initializeBoxes(self):
    bigBanks = ['amex', 'bmo', 'chase', 'td', 'wellsFargo']
    smallBanks = ['fido', 'tangerine', 'telstra']
    self.banks = {'B':bigBanks, 'S':smallBanks}
    self.boxes = []
    # i.e spawn {boxSpawnRate} boxes every {boxSpawnFrequency} seconds
    self.boxSpawnRate = 1
    self.boxSpawnFrequency = 2000
    self.boxSpawnEvent = pygame.USEREVENT + 1
    self.bigBoxChance = 0.2
    self.smallBoxChance = 0.8

    #self.boxes.append(Box('B', 'bmo', (40, 40, BOX_WIDTH, BOX_HEIGHT)))
    pygame.time.set_timer(self.boxSpawnEvent, self.boxSpawnFrequency)

  def __del__(self):
    pygame.quit()

game = Game()
while game.keepPlaying:
  game.updateDocuments()

  game.display.gameDisplay.blit(game.display.map, (0, 0))
  game.display.drawBoxes(game.boxes)
  game.display.drawDocuments(game.docs)
  pygame.draw.rect(game.display.gameDisplay, (0, 0, 255), game.player.getRect())
  game.display.drawDog(game.player)
  pygame.display.update()
  game.handleEvents()

quit()
