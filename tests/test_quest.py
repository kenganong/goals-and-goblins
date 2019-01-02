import pytest
import quest.quest as questlib
import quest.stage as stagelib
import quest.ai as ai

@pytest.fixture
def fighter():
  character = stagelib.Character('Biff', 50)
  character.add_action(stagelib.Wait())
  character.add_action(stagelib.Move())
  character.add_action(stagelib.Attack(1))
  return character

def test_get_quest():
  quest = questlib.get_quest(1)
  assert isinstance(quest, questlib.RatKing)

def test_rat_stage(fighter):
  quest = questlib.get_quest(1)
  stage = quest.create_stage(1, fighter)
  assert len(stage) == 5
  assert stage.get_content(0) == [fighter,]
  assert stage.get_content(1) == []
  assert len(stage.get_content(4)) == 1
  rat = stage.get_content(4)[0]
  assert rat.name == 'rat'
  assert rat.faction == 'enemy'
  assert rat.hp == 7
  assert 'Wait' in rat.actions
  assert 'Move' in rat.actions
  assert 'Attack' in rat.actions
  assert rat.actions['Attack'].damage == 2
  assert isinstance(rat.ai, ai.MeleeSimple)
