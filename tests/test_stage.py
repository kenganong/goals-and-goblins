import pytest
import quest.stage as stage

@pytest.fixture
def fighter_beginner():
  character = stage.Character('Biff', 50)
  character.add_action(stage.Wait())
  character.add_action(stage.Move())
  character.add_action(stage.Attack(1))
  return character

@pytest.fixture
def rat_small():
  character = stage.Character('Rat', 7)
  character.add_action(stage.Wait())
  character.add_action(stage.Move())
  character.add_action(stage.Attack(2))
  return character

@pytest.fixture
def beginner_area(fighter_beginner, rat_small):
  area = stage.Area(5)
  area.set(0, fighter_beginner)
  area.set(4, rat_small)

def test_setup_area(fighter_beginner, rat_small):
  area = stage.Area(5)
  area.set(0, fighter_beginner)
  area.set(3, rat_small)
  assert 'Biff' == area.get(0).name
  assert None == area.get(1)
  assert None == area.get(2)
  assert 'Rat' == area.get(3).name
  assert None == area.get(4)

@pytest.mark.parametrize('action_name,start,expected', [
  ('Wait', 0, [0,]),
  ('Wait', 1, [1,]),
  ('Wait', 2, [2,]),
  ('Wait', 3, [3,]),
  ('Wait', 4, [4,]),
  ('Move', 0, [1,]),
  ('Move', 1, [0,2]),
  ('Move', 2, [1,3]),
  ('Move', 3, [2,4]),
  ('Move', 4, [3,]),
])
def test_possible_targets_alone(fighter_beginner, action_name, start, expected):
  area = stage.Area(5)
  area.set(start, fighter_beginner)
  action = fighter_beginner.actions[action_name]
  possible = list(action.possible_targets(area, start))
  assert expected == possible
