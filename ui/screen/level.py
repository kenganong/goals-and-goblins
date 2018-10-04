import functools
import pygame
from context import context
from ui.component.component import Component
from ui.component.button import Button
from ui.component.label import Label

class Level:
  def __init__(self, manager):
    self.manager = manager
    theme = context['theme']
    quest = context['run_quest']
    stage = context['run_stage']
    self.title = Label((50, 20), theme.font, 'Level {}-{}'.format(quest, stage), color=theme.label_text_color,
                       background=theme.background_color)
    board_left = (context['width'] - 500) / 2
    player = context['run_character']
    rat = Character(7, 2)
    self.board = Board(player, rat, (board_left, 100), (500, 400), theme.background_color, theme.label_text_color,
                       theme.button_color, theme.button_focus_color, self.perform_action)
    self.buttons = ActionButtons((0, 760), (1000, 30), theme, self.action_activated, self.action_deactivated)
    self.buttons.set_actions(['Wait', 'Move', 'Attack'])
    self.painted = False
  def paint(self, screen):
    self.update(screen)
    self.painted = True
  def update(self, screen):
    self.title.update(screen)
    self.board.update(screen)
    self.buttons.update(screen)
  def handle_event(self, event):
    self.board.handle_event(event)
    self.buttons.handle_event(event)
  def action_activated(self, action):
    if action == 'Next Level':
      context['run_stage'] += 1
      self.manager.set_screen('level')
    else:
      self.board.activate(action)
  def action_deactivated(self, action):
    self.board.deactivate()
  def perform_action(self, action, index):
    self.board.perform(action, index)
    if self.board.enemy.hp <= 0:
      self.buttons.set_actions(['Next Level'])
    else:
      self.buttons.set_actions(['Wait', 'Move', 'Attack'])

class Board(Component):
  def __init__(self, player, enemy, position, size, background, foreground, highlight, highlight_focus, action_func):
    super().__init__(position)
    self.player = player
    self.enemy = enemy
    self.surface = pygame.Surface(size)
    self.height = size[1]
    self.background = background
    self.foreground = foreground
    self.highlight = highlight
    self.highlight_focus = highlight_focus
    self.action_func = action_func
    self.character = pygame.image.load('fighter.gif').convert_alpha()
    self.rat = pygame.image.load('rat.gif').convert_alpha()
    self.spaces = ['p', 'e', 'e', 'e', 'r']
    self.space_width = size[0] // len(self.spaces)
    self.action = None
    self.lit = []
    self.focused = -1
  def update(self, screen):
    if self.dirty == True:
      self.surface.fill(self.background)
      left = 0
      highlight_start = self.height // 4
      highlight_end = self.height * 3 // 4
      space_start = self.height - 30
      for idx, space in enumerate(self.spaces):
        if space == 'p':
          self.surface.blit(self.character, (left, 0))
        elif space == 'r':
          self.surface.blit(self.rat, (left, 0))
        color = self.foreground
        if idx in self.lit:
          if self.focused == idx:
            color = self.highlight_focus
          else:
            color = self.highlight
          pygame.draw.line(self.surface, color, (left + 2, highlight_start), (left + 2, highlight_end), 2)
          pygame.draw.line(self.surface, color, (left + self.space_width - 2, highlight_start),
                           (left + self.space_width - 2, highlight_end), 2)
        pygame.draw.lines(self.surface, color, False,
                          [(left, space_start), (left, self.height - 1),
                           (left + self.space_width - 1, self.height - 1),
                           (left + self.space_width - 1, space_start)], 2)
        left += self.space_width
      screen.blit(self.surface, self.position)
      self.dirty = False
  def handle_event(self, event):
    if event.type == pygame.MOUSEMOTION:
      pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
      collide = self.surface.get_rect().collidepoint(pos)
      if collide:
        focused = pos[0] // self.space_width
      else:
        focused = -1
      if focused != self.focused:
        self.focused = focused
        self.dirty = True
    elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
      pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
      collide = self.surface.get_rect().collidepoint(pos)
      if collide:
        index = int(pos[0]) // self.space_width
        if index in self.lit:
          self.action_func(self.action, index)
  def activate(self, action):
    if action == 'Wait':
      self.lit.append(self.spaces.index('p'))
    elif action == 'Attack':
      p_idx = self.spaces.index('p')
      if p_idx > 0 and self.spaces[p_idx - 1] == 'r':
        self.lit.append(p_idx - 1)
      if p_idx < len(self.spaces) - 1 and self.spaces[p_idx + 1] == 'r':
        self.lit.append(p_idx + 1)
    elif action == 'Move':
      p_idx = self.spaces.index('p')
      if p_idx > 0 and self.spaces[p_idx - 1] == 'e':
        self.lit.append(p_idx - 1)
      if p_idx < len(self.spaces) - 1 and self.spaces[p_idx + 1] == 'e':
        self.lit.append(p_idx + 1)
    self.action = action
    self.dirty = True
  def deactivate(self):
    self.action = None
    self.lit = []
    self.dirty = True
  def perform(self, action, index):
    if action == 'Move':
      self.spaces[self.spaces.index('p')] = 'e'
      self.spaces[index] = 'p'
    elif action == 'Attack':
      self.enemy.hp = max(self.enemy.hp - self.player.damage, 0)
      if self.enemy.hp == 0:
        self.spaces[self.spaces.index('r')] = 'e'
    self.deactivate()

class Character:
  def __init__(self, hp, damage):
    self.hp = hp
    self.damage = damage

class ActionButtons(Component):
  def __init__(self, position, size, theme, activate_func, deactivate_func):
    super().__init__(position)
    self.surface = pygame.Surface(size)
    self.size = size
    self.theme = theme
    self.activate = activate_func
    self.deactivate = deactivate_func
    self.active = -1
    self.actions = []
    self.buttons = []
  def set_actions(self, actions):
    button_width = 120
    padding = 10
    left = (self.size[0] - len(actions) * (button_width + padding) + padding) / 2
    self.actions = actions
    self.buttons = []
    for idx, action in enumerate(actions):
      self.buttons.append(Button((left, 0), (button_width, self.size[1]), self.theme.font, str(action),
          click_func=functools.partial(self.click, idx), text_color=self.theme.button_text_color,
          color=self.theme.button_color, focus_color=self.theme.button_focus_color))
      left += button_width + padding
    self.active = -1
    self.dirty = True
  def update(self, screen):
    if self.dirty:
      self.surface.fill(self.theme.background_color)
      for button in self.buttons:
        button.dirty = True
        button.update(self.surface)
      self.dirty = False
    else:
      for button in self.buttons:
        button.update(self.surface)
    screen.blit(self.surface, self.position)
  def handle_event(self, event):
    if hasattr(event, 'pos'):
      orig_pos = event.pos
      event.pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
    for button in self.buttons:
      button.handle_event(event)
    if hasattr(event, 'pos'):
      event.pos = orig_pos
  def click(self, index):
    if self.active > -1:
      button = self.buttons[self.active]
      button.color = self.theme.button_color
      button.focus_color = self.theme.button_focus_color
      button.dirty = True
      self.deactivate(self.actions[self.active])
    if index == self.active:
      self.active = -1
    else:
      self.active = index
      button = self.buttons[index]
      button.color = self.theme.button_active_color
      button.focus_color = self.theme.button_active_focus_color
      button.dirty = True
      self.activate(self.actions[self.active])
