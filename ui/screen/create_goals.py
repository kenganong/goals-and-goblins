from datetime import date
import functools
import pygame
from context import context
from model import Goal
from ui.component.button import Button
from ui.component.label import Label
from ui.component.text_entry import TextEntry, ALPHA, NUMERIC

class CreateGoal:
  def __init__(self, manager):
    blank_width = 100
    self.manager = manager
    theme = context['theme']
    self.label = Label((100, 50), theme.font, 'Create New Goal', theme.label_text_color, theme.background_color)
    self.goal_text = []
    self.goal_text.append(Label((100, 150), theme.font, 'Reduce how many ',
                                theme.label_text_color, theme.background_color))
    self.goal_text.append(Label((100 + self.goal_text[0].surface.get_width() + blank_width, 150), theme.font, ' of ',
                                theme.label_text_color, theme.background_color))
    self.goal_text.append(Label((100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                                + blank_width * 2, 150), theme.font, ' I ',
                                theme.label_text_color, theme.background_color))
    self.goal_text.append(Label((100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                                + self.goal_text[2].surface.get_width() + blank_width * 3, 150),
                                theme.font, ' each week ', theme.label_text_color, theme.background_color))
    self.goal_input = []
    self.goal_input.append(TextEntry((100 + self.goal_text[0].surface.get_width(), 150), blank_width, theme.font,
                                     color=theme.entry_text_color, background=theme.entry_background_color))
    self.goal_input.append(TextEntry((100 + self.goal_text[0].surface.get_width()
                                     + self.goal_text[1].surface.get_width() + blank_width, 150), blank_width,
                                     theme.font, color=theme.entry_text_color, background=theme.entry_background_color))
    self.goal_input.append(TextEntry((100 + self.goal_text[0].surface.get_width()
                                     + self.goal_text[1].surface.get_width() + self.goal_text[2].surface.get_width()
                                     + blank_width * 2, 150), blank_width, theme.font,
                                     color=theme.entry_text_color, background=theme.entry_background_color))
    for goal_input in self.goal_input:
      goal_input.click_func = functools.partial(self.focus_on, goal_input)
      goal_input.set_allowed(ALPHA)
    self.blanks = []
    self.blanks.append([theme.label_text_color,
                        (100 + self.goal_text[0].surface.get_width(), 150 + theme.font.get_linesize()),
                        (100 + self.goal_text[0].surface.get_width() + blank_width, 150 + theme.font.get_linesize())])
    self.blanks.append([theme.label_text_color,
                        (100 + self.goal_text[0].surface.get_width() +
                         self.goal_text[1].surface.get_width() + blank_width, 150 + theme.font.get_linesize()),
                        (100 + self.goal_text[0].surface.get_width() +
                         self.goal_text[1].surface.get_width() + blank_width * 2, 150 + theme.font.get_linesize())])
    self.blanks.append([theme.label_text_color,
                        (100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                         + self.goal_text[2].surface.get_width() + blank_width * 2, 150 + theme.font.get_linesize()),
                        (100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                         + self.goal_text[2].surface.get_width() + blank_width * 3, 150 + theme.font.get_linesize())])
    self.goal_madlib = []
    self.goal_madlib.append(Label((100 + self.goal_text[0].surface.get_width(), 151 + theme.font.get_linesize()),
                             theme.small_font, 'measurement', theme.label_text_color, theme.background_color,
                             width=blank_width, align='center'))
    self.goal_madlib.append(Label((100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                             + blank_width, 151 + theme.font.get_linesize()), theme.small_font, 'noun',
                             theme.label_text_color, theme.background_color, width=blank_width, align='center'))
    self.goal_madlib.append(Label((100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                             + self.goal_text[2].surface.get_width() + blank_width * 2,
                             151 + theme.font.get_linesize()), theme.small_font, 'verb',
                             theme.label_text_color, theme.background_color, width=blank_width, align='center'))
    self.goal_number = Label((100, 250), theme.font, 'Goal Number: ', theme.label_text_color, theme.background_color)
    self.goal_number_input = TextEntry((100 + self.goal_number.surface.get_width(), 250), blank_width, theme.font,
                                       color=theme.entry_text_color, background=theme.entry_background_color)
    self.goal_number_input.click_func = functools.partial(self.focus_on, self.goal_number_input)
    self.goal_number_input.set_allowed(NUMERIC)
    self.add_button = Button((100, 350), (100, 100), theme.font, 'Add Goal', click_func=self.create,
                             text_color=theme.label_text_color, color=theme.button_color,
                             focus_color=theme.button_focus_color, disabled_color=theme.button_disabled_color)
    self.add_button.set_enabled(False)
    self.text_focus = self.goal_input[0]
    self.goal_input[0].focus = True
    self.painted = False
  def paint(self, screen):
    for blank in self.blanks:
      pygame.draw.line(screen, blank[0], blank[1], blank[2])
    self.update(screen)
    self.painted = True
  def update(self, screen):
    self.label.update(screen)
    for goal_text in self.goal_text:
      goal_text.update(screen)
    for goal_input in self.goal_input:
      goal_input.update(screen)
    for goal_madlib in self.goal_madlib:
      goal_madlib.update(screen)
    self.goal_number.update(screen)
    self.goal_number_input.update(screen)
    self.add_button.update(screen)
  def handle_event(self, event):
    all_filled = True
    for goal_input in self.goal_input:
      goal_input.handle_event(event)
      if all_filled and len(goal_input.text) == 0:
        all_filled = False
    self.goal_number_input.handle_event(event)
    if all_filled and len(self.goal_number_input.text) == 0:
      all_filled = False
    self.add_button.set_enabled(all_filled)
    self.add_button.handle_event(event)
  def create(self):
    words = [x.text for x in self.goal_input]
    number = int(self.goal_number_input.text)
    today = date.today().isoformat()
    goal = Goal(profile=context['profile'], start_date=today, period='week', number=number)
    goal.words = words
    session = context['db_session']
    session.add(goal)
    # TODO: Move this after profiles have more than one character
    goal.characters.append(context['profile'].characters[0])
    session.commit()
    self.manager.set_screen('checkin')
  def focus_on(self, entry):
    if not entry.focus:
      self.text_focus.focus = False
      self.text_focus = entry
      entry.focus = True
