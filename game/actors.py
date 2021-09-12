import random

import pandas as pd

from typing import Tuple
from pygments.console import colorize
from abc import ABCMeta, abstractmethod

from game.constants import level_mapper, PERSONALITY, INTELLIGENCE, VOCAB_FILE


vocab_df = pd.read_csv(VOCAB_FILE)
vocab_dict = vocab_df.loc[vocab_df["rule"] == "vocabulary"]


class Actor(metaclass=ABCMeta):

    def __init__(self, hp: int, weakness: str = None):
        self.hp = hp
        self.weakness = weakness

    def take_mental_damage(self, insult: str):
        """Take a certain amount of mental damage. If damage type matches weakness, take double damage."""
        dmg_data = vocab_dict.loc[vocab_dict["output"] == insult, ["damage", "damage_type"]]
        damage_value = dmg_data.damage.iloc[0]
        damage_type = dmg_data.damage_type.iloc[0]

        if damage_type == self.weakness:
            self.hp -= 1.5 * damage_value

        else:
            self.hp -= damage_value

    @staticmethod
    @abstractmethod
    def respond():
        pass


class Enemy(Actor):

    def __init__(self, hp: int, xp: int, weakness: str):
        super().__init__(hp=hp, weakness=weakness)
        self.xp = xp

    @staticmethod
    def respond() -> str:
        """Randomly selects from allowed insults and returns insult, damage value, and damage type."""
        options = list(vocab_dict.output)
        response_choice = random.choice(options)
        return response_choice


class Player(Actor):

    def __init__(self, hp: int, weakness: str, level: int = 1):
        super().__init__(hp=hp, weakness=weakness)
        self.level = level
        self.xp = level_mapper[self.level]
        self.vocabulary = vocab_dict.loc[
            (vocab_dict['level'] <= self.level) & (vocab_dict['input'] == "N")
        ].output.to_list()

        self.current_enemy = None

    def trigger_encounter(self, target: Enemy):
        """Set encounter state to True."""
        self.repartee(target=target)

    def check_level_up(self):
        """Checks current XP against requirements for leveling up."""
        if self.xp >= level_mapper[self.level + 1]:
            self.level += 1
            print(f"LEVEL UP: {self.level}")
            self.vocabulary += vocab_dict.loc[vocab_dict['level'] == self.level].output.to_list()

    def repartee(self, target: Enemy):
        """Main verbal battle method."""
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
            self.xp += target.xp  # Gain XP based on foe slain
            self.check_level_up()

    def respond(self) -> str:
        """Player enters verbal response from predefined list. Returns accepted response and insult type."""

        allowed_words = self.vocabulary
        print(" ".join(allowed_words))
        player_input = input("Please enter your insult: ")

        # For testing
        # player_input = "fatso"

        while player_input not in allowed_words:
            print(f"Word not allowed! Please choose from the following: {' '.join(allowed_words)}")
            player_input = input("New insult: ")

        return player_input


if __name__ == "__main__":
    player = Player(hp=100, weakness=INTELLIGENCE)
    enemy = Enemy(hp=10, xp=50, weakness=PERSONALITY)

    player.trigger_encounter(enemy)
