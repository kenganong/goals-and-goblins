import pygame
from context import context
from ui.component.button import Button
from ui.component.label import Label
from ui.component.text_entry import TextEntry

class CreateGoal:
  def __init__(self, manager):
    blank_width = 100
    self.manager = manager
    theme = context['theme']
    self.label = Label((100, 50), theme.font, 'Create New Goal', theme.label_text_color, theme.background_color)
    self.goal_text = []
    self.goal_text.append(Label((100, 150), theme.font, 'Reduce the number of ',
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
                                     color=theme.label_text_color, background=theme.background_color))
    self.goal_input.append(TextEntry((100 + self.goal_text[0].surface.get_width()
                                     + self.goal_text[1].surface.get_width() + blank_width, 150), blank_width,
                                     theme.font, color=theme.label_text_color, background=theme.background_color))
    self.goal_input.append(TextEntry((100 + self.goal_text[0].surface.get_width()
                                     + self.goal_text[1].surface.get_width() + self.goal_text[2].surface.get_width()
                                     + blank_width * 2, 150), blank_width, theme.font,
                                     color=theme.label_text_color, background=theme.background_color))
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
    # TODO: madlibs should be centered
    self.goal_madlib.append(Label((100 + self.goal_text[0].surface.get_width(), 151 + theme.font.get_linesize()),
                             theme.small_font, 'measurement', theme.label_text_color, theme.background_color))
    self.goal_madlib.append(Label((100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                             + blank_width, 151 + theme.font.get_linesize()), theme.small_font, 'noun',
                             theme.label_text_color, theme.background_color))
    self.goal_madlib.append(Label((100 + self.goal_text[0].surface.get_width() + self.goal_text[1].surface.get_width()
                             + self.goal_text[2].surface.get_width() + blank_width * 2,
                             151 + theme.font.get_linesize()), theme.small_font, 'verb',
                             theme.label_text_color, theme.background_color))
    self.goal_number = Label((100, 250), theme.font, 'Goal Number: ', theme.label_text_color, theme.background_color)
    self.goal_number_input = TextEntry((100 + self.goal_number.surface.get_width(), 250), blank_width, theme.font,
                                       color=theme.label_text_color, background=theme.background_color)
    self.add_button = Button(self.create, pygame.Rect(100, 350, 100, 100),
                             theme.font, 'Add Goal', theme.button_text_color,
                             theme.button_color, theme.button_focus_color)

    self.painted = False
  def paint(self, screen):
    theme = context['theme']
    blank_width = 100
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
    # TODO: blanks, madlibs
  def handle_event(self, event):
    pass
  def create(self):
    pass
