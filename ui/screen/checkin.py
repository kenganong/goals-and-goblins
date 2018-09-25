from datetime import date
from context import context
import model
from ui.component.button import Button
from ui.component.label import Label
from ui.component.text_entry import TextEntry, NUMERIC

class Checkin:
  def __init__(self, manager):
    self.manager = manager
    self.today = date.today().isoformat()
    theme = context['theme']
    profile = context['profile']
    self.label = Label((100, 50), theme.font, 'Daily Check-in', theme.label_text_color, theme.background_color)
    self.day = Label((100, 50 + self.label.surface.get_height()), theme.font, self.today,
                     theme.label_text_color, theme.background_color)
    self.goal = profile.goals[0]
    sentence = 'How many {} of {} did you {} today?'.format(*self.goal.words)
    self.goal_text = Label((100, 150), theme.font, sentence, theme.label_text_color, theme.background_color)
    self.goal_amount = Label((100, 150 + self.goal_text.surface.get_height()), theme.font,
                             'Goal: {}'.format(self.goal.number), theme.label_text_color, theme.background_color)
    self.goal_input = TextEntry((100 + self.goal_text.surface.get_width(), 150), 50, theme.font,
                                color=theme.entry_text_color, background=theme.entry_background_color)
    self.goal_input.set_allowed(NUMERIC)
    self.goal_input.focus = True
    self.complete_button = Button((100, 300), (200, 100), theme.font, 'Complete Check-in', click_func=self.complete,
                                  text_color=theme.label_text_color, color=theme.button_color,
                                  focus_color=theme.button_focus_color, disabled_color=theme.button_disabled_color)
    self.complete_button.set_enabled(False)
    self.painted = False
  def paint(self, screen):
    self.update(screen)
    self.painted = True
  def update(self, screen):
    for element in [self.label, self.day, self.goal_text, self.goal_amount, self.goal_input, self.complete_button]:
      element.update(screen)
  def handle_event(self, event):
    self.goal_input.handle_event(event)
    self.complete_button.set_enabled(len(self.goal_input.text) > 0)
    self.complete_button.handle_event(event)
  def complete(self):
    number = int(self.goal_input.text)
    checkin = model.Checkin(goal=self.goal, date=self.today, number=number)
    session = context['db_session']
    for character in self.goal.characters:
      character.gold += 1
      character.modified_date = self.today
      session.add(character)
    session.add(checkin)
    session.commit()
    self.manager.set_screen('shop')
