import pygame
from ui.component.component import Component

class Label(Component):
  def __init__(self, position, font, text, color=None, background=None, width=-1, align='left'):
    super().__init__(position)
    if color == None:
      color = pygame.Color('black')
    if background == None:
      background = pygame.Color('white')
    self.surface = font.render(text, True, color, background)
    if width >= 0:
      text_surface = self.surface
      if align == 'center':
        left = (width - text_surface.get_width()) / 2
      elif align == 'right':
        left = width - text_surface.get_width()
      else:
        left = 0
      self.surface = pygame.Surface((width, font.get_linesize()))
      self.surface.fill(background)
      self.surface.blit(text_surface, (left, 0))
