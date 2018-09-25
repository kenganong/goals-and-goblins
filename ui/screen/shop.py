import functools
import pygame
from context import context
from ui.component.component import Component
from ui.component.label import Label
from ui.component.button import Button

class Shop:
  def __init__(self, manager):
    self.manager = manager
    theme = context['theme']
    self.weapons = []
    self.weapons.append(Weapon('None', 0, 0))
    self.weapons.append(Weapon('Broken Sword', 1, 2))
    self.weapons.append(Weapon('Bent Sword', 2, 4))
    self.weapons.append(Weapon('Sword', 3, 8))
    self.character = context['profile'].characters[0] # TODO: while one character is supported
    self.gold = self.character.gold
    self.wallet = Label((0, 0), theme.font, 'Gold: {}'.format(self.gold),
                      color=theme.label_text_color, background=theme.background_color)
    self.enemies = Label((0, 0), theme.font, 'Experience: {}'.format(self.character.enemies),
                         color=theme.label_text_color, background=theme.background_color)
    top_spacing = 20
    top_label_left = (context['width'] - self.wallet.surface.get_width()
                      - self.enemies.surface.get_width() - top_spacing) / 2
    self.wallet.position = (top_label_left, 10)
    self.enemies.position = (top_label_left + self.wallet.surface.get_width() + top_spacing, 10)
    self.character_sheet = CharacterComponent((20, 50), (460, 600), self.character, self.weapons[0], theme.font,
                                              theme.entry_text_color, theme.entry_background_color)
    grey_green = pygame.Color(50, 70, 50)
    grey_red = pygame.Color(70, 50, 50)
    self.shop = ShopComponent((520, 50), (460, 600), self.buy, theme.font, theme.entry_text_color,
                              theme.entry_background_color, grey_green, grey_red)
    self.shop.set_stock(self.gold, self.character_sheet.get_weapon(), self.weapons)
    self.enter = Button((400, 670), (200, 30), theme.font, 'Enter the Dungeon', click_func=self.enter_dungeon,
                        text_color=theme.button_text_color, color=theme.button_color,
                        focus_color=theme.button_focus_color)
    self.painted = False
  def paint(self, screen):
    self.update(screen)
    self.painted = True
  def update(self, screen):
    self.wallet.update(screen)
    self.enemies.update(screen)
    self.character_sheet.update(screen)
    self.shop.update(screen)
    self.enter.update(screen)
  def handle_event(self, event):
    self.shop.handle_event(event)
    self.enter.handle_event(event)
  def enter_dungeon(self):
    pass
  def buy(self, item):
    current = self.character_sheet.get_weapon()
    self.gold += current.cost - item.cost
    self.character_sheet.set_weapon(item)
    self.shop.set_stock(self.gold, item, self.weapons)
    self.wallet.set_text('Gold: {}'.format(self.gold))

class CharacterComponent(Component):
  def __init__(self, position, size, character, weapon, font, color, background):
    super().__init__(position)
    self.run = RunCharacter()
    self.run.base_hp = 50
    self.run.base_damage = 1
    self.run.weapon = weapon
    self.background = background
    self.surface = pygame.Surface(size)
    self.name = Label((0, 0), font, character.name, color=color, background=background)
    left_space = 20
    self.hp = Label((left_space, 30), font, 'HP: {}'.format(self.run.base_hp), color=color, background=background)
    self.damage = Label((left_space, 60), font, 'Damage: {}'.format(self.run.base_damage + self.run.weapon.damage),
                        color=color, background=background)
    self.weapon = Label((left_space, 120), font, 'Weapon: {}'.format(self.run.weapon.name),
                        color=color, background=background)
  def update(self, screen):
    if self.dirty:
      self.surface.fill(self.background)
      for label in [self.name, self.hp, self.damage, self.weapon]:
        label.dirty = True
        label.update(self.surface)
      screen.blit(self.surface, self.position)
  def get_weapon(self):
    return self.run.weapon
  def set_weapon(self, weapon):
    self.run.weapon = weapon
    self.damage.set_text('Damage: {}'.format(self.run.base_damage + self.run.weapon.damage))
    self.weapon.set_text('Weapon: {}'.format(self.run.weapon.name))
    self.dirty = True

class RunCharacter:
  pass

class ShopComponent(Component):
  def __init__(self, position, size, buy_func, font, color, background, focus, disabled):
    super().__init__(position)
    self.font = font
    self.color = color
    self.background = background
    self.focus = focus
    self.disabled = disabled
    self.buy = buy_func
    self.surface = pygame.Surface(size)
    self.label = Label((0, 0), self.font, 'Shop', width=size[0], align='right',
                       color=self.color, background=self.background)
    self.stock = []
  def update(self, screen):
    if self.dirty:
      self.surface.fill(self.background)
      self.label.dirty = True
      self.label.update(self.surface)
      for item in self.stock:
        item.dirty = True
        item.update(self.surface)
      screen.blit(self.surface, self.position)
    else:
      for item in self.stock:
        item.update(self.surface)
  def handle_event(self, event):
    for item in self.stock:
      if hasattr(event, 'pos'):
        orig_pos = event.pos
        event.pos = (event.pos[0] - self.position[0], event.pos[1] - self.position[1])
      item.handle_event(event)
      if hasattr(event, 'pos'):
        event.pos = orig_pos
  def set_stock(self, gold, weapon, stock):
    self.stock = []
    for idx, item in enumerate(item for item in stock if item.name != weapon.name):
      cost = weapon.cost - item.cost
      text = '{}, {:+d} damage, {:+d} gold'.format(item.name, item.damage - weapon.damage, cost)
      button = Button((20, 30 * (idx + 1)), (self.surface.get_width() - 40, self.font.get_linesize()), self.font, text,
                      click_func=functools.partial(self.buy, item), text_color=self.color, color=self.background,
                      focus_color=self.focus, disabled_color=self.disabled, align='left')
      button.set_enabled(gold + cost >= 0)
      self.stock.append(button)
    self.dirty = True

class Weapon:
  def __init__(self, name, damage, cost):
    self.name = name
    self.damage = damage
    self.cost = cost
