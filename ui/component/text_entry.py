import pygame
from pygame.locals import *
from ui.component.component import Component

ALPHA = 1
NUMERIC = 2
ALPHANUMERIC = 3

class TextEntry(Component):
  def __init__(self, position, width, font, text='', color=None, background=None, click_func=None):
    super().__init__(position)
    self.font = font
    if color == None:
      color = pygame.Color('black')
    if background == None:
      background = pygame.Color('white')
    self.color = color
    self.background = background
    self.click_func = click_func
    self.text = text
    self.cursor_index = 0
    self.surface = pygame.Surface((width, font.get_linesize()))
    self.set_allowed(ALPHANUMERIC)
  def set_allowed(self, allow):
    self.allow_alpha = False
    self.allow_number = False
    if allow == ALPHA or allow == ALPHANUMERIC:
      self.allow_alpha = True
    if allow == NUMERIC or allow == ALPHANUMERIC:
      self.allow_number = True
  def handle_event(self, event):
    if self.click_func and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
      collide = self.surface.get_rect().collidepoint(pos)
      if collide:
        self.click_func()
    elif self.focus and event.type == pygame.KEYDOWN:
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
        if ((self.allow_alpha and (eu >= 'a' and eu <= 'z' or eu >= 'A' and eu <= 'Z'))
            or (self.allow_number and eu >= '0' and eu <= '9')):
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
