import pygame
from pygame.locals import *
from ui.component.component import Component

class TextEntry(Component):
  def __init__(self, position, width, font, text='', color=None, background=None):
    super().__init__(position)
    self.font = font
    self.color = color
    self.background = background
    self.text = text
    self.cursor_index = 0
    self.surface = pygame.Surface((width, font.get_linesize()))
  def handle_event(self, event):
    if self.focus and event.type == pygame.KEYDOWN:
      if event.key == K_LEFT:
        if self.cursor_index > 0:
          self.cursor_index -= 1
      elif event.key == K_RIGHT:
        if self.cursor_index < len(self.text):
          self.cursor_index += 1
      elif event.key == K_HOME:
        self.cursor_index = 0
      elif event.key == K_END:
        self.cursor_index = len(self.text)
      elif event.key == K_BACKSPACE:
        if self.cursor_index > 0:
          self.text = self.text[:self.cursor_index - 1] + self.text[self.cursor_index:]
          self.cursor_index -= 1
          self.dirty = True
      elif event.key == K_DELETE:
        if self.cursor_index < len(self.text):
          self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]
          self.dirty = True
      else:
        eu = event.unicode
        if eu >= 'a' and eu <= 'z' or eu >= 'A' and eu <= 'Z':
          self.text = self.text[:self.cursor_index] + eu + self.text[self.cursor_index:]
          self.cursor_index += 1
          self.dirty = True
  def update(self, screen):
    if self.dirty:
      self.surface.fill(self.background)
      text_surface = self.font.render(self.text, False, self.color)
      self.surface.blit(text_surface, (0, 0))
      screen.blit(self.surface, self.position)
      self.dirty = False
