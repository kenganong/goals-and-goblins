import functools
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
    self.buttons = [Button(functools.partial(self.choose_profile, profile),
                           pygame.Rect(100, 150 + 100 * idx, 600, 98),
                           font, profile.name, text, color, focus)
                      for idx, profile in enumerate(self.profiles)]
    self.buttons.append(Button(self.add_profile,
                               pygame.Rect(100, 150 + 100 * len(self.buttons), 600, 98),
                               font, 'New Profile', text, color, focus))
    self.painted = False
  def paint(self, screen):
    screen.blit(self.label, (100, 50))
    self.update(screen)
    self.painted = True
  def update(self, screen):
    for button in self.buttons:
      button.update(screen)
  def handle_event(self, event):
    for button in self.buttons:
      button.handle_event(event)
  def choose_profile(self, profile):
    print('clicked {}'.format(profile.name))
  def add_profile(self):
    print('clicked add profile')
