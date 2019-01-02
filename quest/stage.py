class Stage:
  def __init__(self, area, player):
    next_num = 0
    next_wait = 10
    self.area = area
    self.player = player
    self.player.next_action = next_num
    next_num += next_wait
    self.character_order = []
    for i in range(len(self.area)):
      character = self.area.get(i)
      if character and hasattr(character, 'actions') and character.name != player:
        character.next_action = next_num
        next_num += next_wait
        self.character_order.append(character.name)
    self.callback = Callback()
    self.callback.damage = self.damage
    self.done = len(self.area) <= 1
  def __len__(self):
    return len(self.area)
  def get_content(self, index):
    character = self.area.get(index)
    if character:
      return [character,]
    else:
      return []
  def next_actor(self):
    if self.done:
      return None
    character = self.player
    for character_name in self.character_order:
      contender = self.area.lookup(character_name)
      if contender.next_action < character.next_action:
        character = contender
    return character.name
  def possible_actions(self, actor_name):
    if not self.done:
      location = self.area.locate(actor_name)
      actor = self.area.lookup(actor_name)
      for action in actor.actions:
        if next(actor.actions[action].possible_targets(self.area, location), None) != None:
          yield action
  def possible_targets(self, actor_name, action):
    if not self.done:
      location = self.area.locate(actor_name)
      actor = self.area.lookup(actor_name)
      return actor.actions[action].possible_targets(self.area, location)
  def perform_next(self, action_name=None, target=None):
    actor_name = self.next_actor()
    actor = self.area.lookup(actor_name)
    source = self.area.locate(actor_name)
    if actor_name == self.player.name:
      action = self.player.actions[action_name]
    else:
      (action, target) = actor.ai.next_action(self.area)
    actor.next_action += action.cooldown
    action.act(self.area, self.callback, source, target)
  def damage(self, damage, source, target):
    target_char = self.area.get(target)
    target_char.hp = max(0, target_char.hp - damage)
    if target_char.hp == 0:
      if target_char.name == self.player.name:
        self.done = True
        self.outcome = False
      else:
        self.area.remove(target)
        self.character_order.remove(target_char.name)
        self.done = len(self.area) <= 1
        if self.done:
          self.outcome = True

class Area:
  def __init__(self, num_slots):
    self.slots = [None,] * num_slots
    self.things = dict()
  def __len__(self):
    return len(self.slots)
  def set(self, index, character):
    self.slots[index] = character
    self.things[character.name] = index
  def get(self, index):
    return self.slots[index]
  def move(self, start, end):
    character = self.slots[start]
    if character:
      self.slots[start] = None
      self.slots[end] = character
      self.things[character.name] = end
  def remove(self, location):
    character = self.slots[location]
    if character:
      self.slots[location] = None
      del self.things[character.name]
  def lookup(self, name):
    return self.slots[self.things[name]]
  def locate(self, name):
    return self.things[name]

class Callback:
  pass

class Something:
  def __init__(self, name, hp):
    self.name = name
    self.hp = hp

class Character(Something):
  def __init__(self, name, hp):
    super().__init__(name, hp)
    self.actions = {}
  def add_action(self, action):
    self.actions[action.name] = action

class Action:
  def __init__(self, name):
    self.name = name
    self.cooldown = 50

class Wait(Action):
  def __init__(self):
    super().__init__('Wait')
  def possible_targets(self, area, start):
    yield start
  def act(self, area, callback, source, target):
    pass

class Move(Action):
  def __init__(self):
    super().__init__('Move')
  def possible_targets(self, area, start):
    if start - 1 >= 0 and area.get(start - 1) == None:
      yield start - 1
    if start + 1 < len(area) and area.get(start + 1) == None:
      yield start + 1
  def act(self, area, callback, source, target):
    area.move(source, target)

class Attack(Action):
  def __init__(self, damage):
    super().__init__('Attack')
    self.damage = damage
  def possible_targets(self, area, start):
    if start - 1 >= 0 and area.get(start - 1) != None:
      yield start - 1
    if start + 1 < len(area) and area.get(start + 1) != None:
      yield start + 1
  def act(self, area, callback, source, target):
    callback.damage(self.damage, source, target)
