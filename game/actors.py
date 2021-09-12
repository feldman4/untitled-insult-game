import random

from typing import Optional
from collections import Counter
from pygments.console import colorize
from abc import ABCMeta, abstractmethod

from game.utils import read_vocab, calc_similarity_modifier, get_grammar
from game.constants import level_mapper, VULNERABLE_MODIFIER
from game.cfg import get_all_insults


class Actor(metaclass=ABCMeta):

    def __init__(self, hp: int, classification: str, weakness: list = None, ):
        self.hp = hp
        self.weakness = weakness
        self.encounter_responses = []
        self._vocab_dict = read_vocab()
        self.grammar = get_grammar(classification)
        self.vocabulary = get_all_insults(self.grammar)

    #@property
    #def hp(self) -> int:
    #    """Get the HP value."""
    #    return self.hp

    #@hp.setter
    #def hp(self, value: int) -> None:
    #    """Manually set the HP."""
    #    self.hp = value

    def get_current_responses(self) -> Counter:
        """Returns of counter of responses used during current combat. If None, then actor not in combat."""
        return Counter(self.encounter_responses)

    def take_mental_damage(self, insult: str) -> None:
        """Take a certain amount of mental damage. If damage type matches weakness, take double damage."""
        dmg_data = self._vocab_dict.loc[self._vocab_dict["output"] == insult, ["damage", "damage_type"]]
        damage_value = dmg_data.damage.iloc[0]
        damage_type = dmg_data.damage_type.iloc[0]

        similarity_modifier = calc_similarity_modifier(self.encounter_responses, insult)

        # First apply similarity modifier to damage
        modified_dmg = round(similarity_modifier * damage_value)

        # Apply vulnerability multiplier to damage if applies
        if damage_type == self.weakness:
            self.hp -= round(VULNERABLE_MODIFIER * modified_dmg)

        else:
            self.hp -= modified_dmg

        self.encounter_responses.append(insult)  # Add insult to list of previously heard ones

    def take_mental_damage2(self, insult: str) -> None:
        from game.word_handling import multi_word_dmg
        from game.utils import get_dmg_map
        dmg_mod = multi_word_dmg(insult.split(), self.weakness)
        dmg_map = get_dmg_map()

        self.hp -= (max(dmg_map.get(x, 0) for x in insult)*dmg_mod)
        self.encounter_responses.append(insult)

    @staticmethod
    @abstractmethod
    def respond():
        pass


class Enemy(Actor):

    def __init__(self, hp: int, xp: int, classification: str, weakness: list):
        super().__init__(hp=hp, classification=classification, weakness=weakness)
        self.xp_worth = xp

    def respond(self) -> str:
        """Randomly selects from allowed insults and returns insult, damage value, and damage type."""
        options = list(self._vocab_dict.output)
        response_choice = random.choice(options)
        return response_choice


class Player(Actor):

    def __init__(self, hp: int, classification: str, weakness: list, level: int = 1):
        super().__init__(hp=hp, classification=classification, weakness=weakness)
        self.level = level
        self.xp = level_mapper[self.level]
        #self.vocabulary = self._vocab_dict.loc[(self._vocab_dict['level'] <= self.level)].output.to_list()

        # Battle attributes
        # self.in_encounter = False
        self.current_enemy: Optional[Enemy] = None

        self._response_history = []  # Used for player stats

    # def trigger_encounter(self, target: Enemy):
    #     """Set encounter state to True."""
    #     self.in_encounter = True

    def end_encounter(self):
        """End encounter, add responses to player history, and clear battle insult history."""
        # Add the encounter responses received by enemy (i.e. said by player) to global history
        self._response_history += self.current_enemy.encounter_responses
        self.current_enemy = None
        # self.in_encounter = False

        self.encounter_responses = []  # Empty encounter response cache

    def gain_xp(self):
        """Add XP gained for vanquishing foe."""
        self.xp += self.current_enemy.xp_worth

    def check_level_up(self):
        """Checks current XP against requirements for leveling up."""
        if self.xp >= level_mapper[self.level + 1]:
            self.level += 1
            print(f"LEVEL UP: {self.level}")
            self.vocabulary += self._vocab_dict.loc[self._vocab_dict['level'] == self.level].output.to_list()

    def repartee(self, target: Enemy):
        """Main verbal battle method. Mostly used for testing."""
        while self.hp > 0 and target.hp > 0:
            # Show health
            print(colorize("green", f"Your mental health: {self.hp}"))
            print(colorize("yellow", f"Enemy mental health: {target.hp}"))

            # Player inputs response and applies damage to enemy
            player_response = self.respond()
            target.take_mental_damage(player_response)

            # Enemy randomly selects insult and applies damage to player
            enemy_response = target.respond()
            print(colorize("red", f"Your enemy said: {enemy_response}!"))
            self.take_mental_damage(enemy_response)

        if self.hp <= 0:  # You died
            print(colorize("red", "You have been pwned!\nGAME OVER"))

        else:
            print("You have schooled your foe.")
            self.xp += target.xp_worth  # Gain XP based on foe slain
            self.check_level_up()

    def respond(self) -> str:
        """Player enters verbal response from predefined list. Returns accepted response and insult type."""

        allowed_words = self.vocabulary
        print(" ".join(allowed_words))
        player_input = input("Please enter your insult: ")

        while player_input not in allowed_words:
            print(f"Word not allowed! Please choose from the following: {' '.join(allowed_words)}")
            player_input = input("New insult: ")

        return player_input


if __name__ == "__main__":
    player = Player(hp=100, classification='idiot == "x"', weakness=["intelligence"])
    enemy = Enemy(hp=10, xp=50, classification='idiot == "x"', weakness=["personality"])

    player.repartee(enemy)
