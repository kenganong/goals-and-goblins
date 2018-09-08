import pygame

class Button:
  def __init__(self, func, rect, font, text, text_color, button_color, focus_color):
    self.func = func
    self.rect = rect
    self.label = font.render(text, False, text_color)
    self.label_rect = self.label.get_rect()
    self.label_rect.center = self.rect.center
    self.color = button_color
    self.focus_color = focus_color
    self.focus = False
    self.changed = True
  def handle_event(self, event):
    if event.type == pygame.MOUSEMOTION:
      collide = self.rect.collidepoint(event.pos)
      if collide and not self.focus:
        self.focus = True
        self.changed = True
      elif not collide and self.focus:
        self.focus = False
        self.changed = True
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      collide = self.rect.collidepoint(event.pos)
      if collide:
        self.func()
  def update(self, surface):
    if self.changed:
      if self.focus:
        color = self.focus_color
      else:
        color = self.color
      pygame.draw.rect(surface, color, self.rect)
      surface.blit(self.label, self.label_rect)
      self.changed = False
