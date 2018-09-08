import pygame
from pygame.locals import *

class TextEntry:
  def __init__(self, position, font, text_color, background_color):
    self.position = position
    self.font = font
    self.text_color = text_color
    self.background_color = background_color
    self.text = ''
    self.cursor_index = 0
    self.rect = pygame.Rect(position, (0, 0))
    self.focus = False
    self.changed = True
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
          self.changed = True
      elif event.key == K_DELETE:
        if self.cursor_index < len(self.text):
          self.text = self.text[:self.cursor_index] + self.text[self.cursor_index + 1:]
          self.changed = True
      else:
        eu = event.unicode
        if eu >= 'a' and eu <= 'z' or eu >= 'A' and eu <= 'Z':
          self.text = self.text[:self.cursor_index] + eu + self.text[self.cursor_index:]
          self.cursor_index += 1
          self.changed = True
  def update(self, surface):
    if self.changed:
      pygame.draw.rect(surface, self.background_color, self.rect) #Clear the old
      text_surface = self.font.render(self.text, False, self.text_color)
      self.rect = text_surface.get_rect(topleft=self.position)
      surface.blit(text_surface, self.position)
      self.changed = False
