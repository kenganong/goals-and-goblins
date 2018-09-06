import pygame
from context import context
from model import Profile
from ui.component.button import Button

class ListProfiles:
  def __init__(self):
    self.profiles = context['db_session'].query(Profile).order_by(Profile.name).all()
    font = context['ui_font']
    label_color = context['ui_label_text_color']
    text = context['ui_button_text_color']
    color = context['ui_button_color']
    focus = context['ui_button_focus_color']
    self.label = font.render('Choose Profile', False, label_color)
    self.buttons = [Button(pygame.Rect(100, 150 + 100 * idx, 600, 98), font, profile.name, text, color, focus)
                      for idx, profile in enumerate(self.profiles)]
    self.painted = False
  def paint(self, screen, mouse_pos):
    screen.blit(self.label, (100, 50))
    self.update(screen, mouse_pos)
    self.painted = True
  def update(self, screen, mouse_pos):
    for button in self.buttons:
      button.register_mouse(mouse_pos)
      button.update(screen)
