import random

from typing import Optional
from pygments.console import colorize
from abc import ABCMeta, abstractmethod

from game.utils import read_vocab
from game.constants import level_mapper, VULNERABLE_MODIFIER


class Actor(metaclass=ABCMeta):

    def __init__(self, hp: int, weakness: str = None):
        self.hp = hp
        self.weakness = weakness
        self._vocab_dict = read_vocab(input_filter="N")  # Only nouns

    @property
    def hp(self) -> int:
        """Get the HP value."""
        return self.hp

    @hp.setter
    def hp(self, value: int):
        """Manually set the HP."""
        self.hp = value

    def take_mental_damage(self, insult: str):
        """Take a certain amount of mental damage. If damage type matches weakness, take double damage."""
        dmg_data = self._vocab_dict.loc[self._vocab_dict["output"] == insult, ["damage", "damage_type"]]
        damage_value = dmg_data.damage.iloc[0]
        damage_type = dmg_data.damage_type.iloc[0]

        if damage_type == self.weakness:
            self.hp -= round(VULNERABLE_MODIFIER * damage_value)

        else:
            self.hp -= damage_value

    @staticmethod
    @abstractmethod
    def respond():
        pass


class Enemy(Actor):

    def __init__(self, hp: int, xp: int, weakness: str):
        super().__init__(hp=hp, weakness=weakness)
        self.xp_worth = xp

    def respond(self) -> str:
        """Randomly selects from allowed insults and returns insult, damage value, and damage type."""
        options = list(self._vocab_dict.output)
        response_choice = random.choice(options)
        return response_choice


class Player(Actor):

    def __init__(self, hp: int, weakness: str, level: int = 1):
        super().__init__(hp=hp, weakness=weakness)
        self.level = level
        self.xp = level_mapper[self.level]
        self.vocabulary = self._vocab_dict.loc[(self._vocab_dict['level'] <= self.level)].output.to_list()

        # Battle attributes
        # self.in_encounter = False
        self.current_enemy: Optional[Enemy] = None
        self.encounter_responses = None

        self._response_history = []  # Used for player stats

    # def trigger_encounter(self, target: Enemy):
    #     """Set encounter state to True."""
    #     self.in_encounter = True

    def end_encounter(self):
        """End encounter, add responses to player history, and clear battle insult history."""
        self.current_enemy = None
        # self.in_encounter = False

        if self.encounter_responses:  # Add to full response history for player stats
            self._response_history += self.encounter_responses

        self.encounter_responses = None

    def gain_xp(self, foe: Enemy):
        """Add XP gained for vanquishing foe."""
        self.xp += foe.xp_worth

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
    player = Player(hp=100, weakness="intelligence")
    enemy = Enemy(hp=10, xp=50, weakness="personality")

    player.repartee(enemy)
