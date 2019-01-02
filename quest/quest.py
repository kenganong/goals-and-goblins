import random
from quest.stage import Stage, Area, Character, Wait, Move, Attack
import quest.ai as ai

quests = []

def populate_quests():
  quests.append(RatKing)

def get_quest(quest_num):
  if not quests:
    populate_quests()
  return quests[quest_num - 1]()

class RatKing:
  def create_stage(self, stage_num, player):
    rat = self.generate_rat(stage_num)
    area = Area(5)
    area.set(0, player)
    area.set(4, rat)
    return Stage(area, player)
  def generate_rat(self, stage_num):
    rat = Character('rat', 5)
    rat.faction = 'enemy'
    rat.add_action(Move())
    rat.add_action(Wait())
    rat_attack = Attack(2)
    rat.add_action(rat_attack)
    rat.ai = ai.MeleeSimple(rat)
    hp_upgrade = HealthUpgrade(1, 2.5, rat)
    attack_upgrade = DamageUpgrade(2, 1, rat_attack)
    choose_upgrades(stage_num, [hp_upgrade, attack_upgrade])
    return rat

def choose_upgrades(amount, upgrades):
  while amount > 0:
    upgrade = random.choice([u for u in upgrades if u.cost <= amount])
    upgrade.level += 1
    amount -= upgrade.cost
  for upgrade in upgrades: upgrade.apply()

class HealthUpgrade:
  def __init__(self, cost, health_per, character):
    self.cost = cost
    self.health_per = health_per
    self.character = character
    self.level = 0
  def apply(self):
    self.character.hp += int(self.level * self.health_per)

class DamageUpgrade:
  def __init__(self, cost, damage_per, attack):
    self.cost = cost
    self.damage_per = damage_per
    self.attack = attack
    self.level = 0
  def apply(self):
    self.attack.damage += int(self.level * self.damage_per)
