class MeleeSimple:
  def __init__(self, character):
    self.character = character
  def next_action(self, area):
    location = area.locate(self.character.name)
    attack = self.character.actions['Attack']
    # Attack an enemy
    for target in attack.possible_targets(area, location):
      if area.get(target).faction != self.character.faction:
        return (attack, target)
    # Move toward the closest enemy
    closest_opponent = None
    for name in area.things:
      thing = area.lookup(name)
      if thing.faction != self.character.faction and thing.faction != 'neutral':
        enemy_loc = area.locate(name)
        if closest_opponent == None or abs(location - enemy_loc) < abs(location - closest_opponent):
          closest_opponent = enemy_loc
    if closest_opponent != None:
      move = self.character.actions['Move']
      closest_move = location
      for target in move.possible_targets(area, location):
        if abs(target - closest_opponent) < abs(closest_move - closest_opponent):
          closest_move = target
      if closest_move != location:
        return (move, closest_move)
    return (self.character.actions['Wait'], location)
