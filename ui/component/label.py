import pygame
from ui.component.component import Component

class Label(Component):
  def __init__(self, position, font, text, color=None, background=None, width=-1, align='left'):
    super().__init__(position)
    if color == None:
      color = pygame.Color('black')
    if background == None:
      background = pygame.Color('white')
    self.color = color
    self.background = background
    self.width = width
    self.align = align
    self.font = font
    self.set_text(text)
  def set_text(self, text):
    self.surface = self.font.render(text, True, self.color, self.background)
    if self.width >= 0:
      text_surface = self.surface
      if self.align == 'center':
        left = (self.width - text_surface.get_width()) / 2
      elif self.align == 'right':
        left = self.width - text_surface.get_width()
      else:
        left = 0
      self.surface = pygame.Surface((self.width, self.font.get_linesize()))
      self.surface.fill(self.background)
      self.surface.blit(text_surface, (left, 0))
    self.dirty = True
