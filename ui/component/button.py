import pygame
from ui.component.component import Component

class Button(Component):
  def __init__(self, position, size, font, text, click_func=None, text_color=None, color=None,
               focus_color=None, disabled_color=None):
    super().__init__(position)
    self.surface = pygame.Surface(size)
    if text_color == None:
      text_color = pygame.Color('black')
    if color == None:
      color = pygame.Color('grey')
    if focus_color == None:
      focus_color = color
    if disabled_color == None:
      disabled_color = color
    self.color = color
    self.focus_color = focus_color
    self.disabled_color = disabled_color
    self.label = font.render(text, True, text_color)
    label_size = self.label.get_size()
    self.label_position = ((size[0] - label_size[0]) / 2, (size[1] - label_size[1]) / 2)
    self.func = click_func
    self.enabled = True
  def set_enabled(self, enabled):
    if self.enabled != enabled:
      self.enabled = enabled
      self.dirty = True
  def handle_event(self, event):
    if self.enabled:
      if event.type == pygame.MOUSEMOTION:
        pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
        collide = self.surface.get_rect().collidepoint(pos)
        if collide and not self.focus:
          self.focus = True
          self.dirty = True
        elif not collide and self.focus:
          self.focus = False
          self.dirty = True
      elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
        collide = self.surface.get_rect().collidepoint(pos)
        if collide:
          self.func()
  def update(self, screen):
    if self.dirty:
      if not self.enabled:
        color = self.disabled_color
      elif self.focus:
        color = self.focus_color
      else:
        color = self.color
      self.surface.fill(color)
      self.surface.blit(self.label, self.label_position)
      screen.blit(self.surface, self.position)
      self.dirty = False
