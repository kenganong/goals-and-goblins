import functools
import pygame
from context import context
from model import Profile
from ui.component.button import Button
from ui.component.label import Label

class ListProfiles:
  def __init__(self, manager):
    self.manager = manager
    self.profiles = context['db_session'].query(Profile).order_by(Profile.name).all()
    theme = context['theme']
    self.label = Label((100, 50), theme.font, 'Choose Profile', theme.label_text_color, theme.background_color)
    self.buttons = [Button((100, 150 + 100 * idx), (600, 98), theme.font, profile.name,
                           click_func=functools.partial(self.choose_profile, profile),
                           text_color=theme.label_text_color, color=theme.button_color,
                           focus_color=theme.button_focus_color)
                      for idx, profile in enumerate(self.profiles)]
    self.buttons.append(Button((100, 150 + 100 * len(self.buttons)), (600, 98), theme.font, 'New Profile',
                               click_func=self.add_profile, text_color=theme.label_text_color,
                               color=theme.button_color, focus_color=theme.button_focus_color))
    self.painted = False
  def paint(self, screen):
    self.update(screen)
    self.painted = True
  def update(self, screen):
    self.label.update(screen)
    for button in self.buttons:
      button.update(screen)
  def handle_event(self, event):
    for button in self.buttons:
      button.handle_event(event)
  def choose_profile(self, profile):
    context['profile'] = profile
    self.manager.select_profile()
  def add_profile(self):
    self.manager.set_screen('create_profile')
