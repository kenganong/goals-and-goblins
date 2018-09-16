import pygame
from ui.component.component import Component

class Label(Component):
  def __init__(self, position, font, text, color=None, background=None):
    super().__init__(position)
    if color == None:
      color = pygame.Color('black')
    if background == None:
      background = pygame.Color('white')
    self.surface = font.render(text, True, color, background)
