import random

from typing import Tuple
from pygments.console import colorize
from abc import ABCMeta, abstractmethod

from game.constants import vocab_dict, level_mapper, PERSONALITY, INTELLIGENCE, WEIGHT


class Actor(metaclass=ABCMeta):

    def __init__(self, hp: int, weakness: str = None):
        self.hp = hp
        self.weakness = weakness

    def take_mental_damage(self, dmg_pair: Tuple[int, str]):
        """Take a certain amount of mental damage. If damage type matches weakness, take double damage."""
        dmg_value, dmg_type = dmg_pair

        if dmg_type == self.weakness:
            self.hp -= 1.5 * dmg_value

        else:
            self.hp -= dmg_value

    def take_mental_damage2(self, insult: str):
        """Take damage from a word."""

        if insult == self.weakness:
            self.hp -= 1.5

        else:
            self.hp -= 1

    @staticmethod
    @abstractmethod
    def respond():
        pass


class Enemy(Actor):

    def __init__(self, hp: int, xp: int, weakness: str):
        super().__init__(hp=hp, weakness=weakness)
        self.xp = xp

    @staticmethod
    def respond() -> Tuple[str, Tuple[int, str]]:
        """Randomly selects from allowed insults and returns insult, damage value, and damage type."""
        options = list(vocab_dict.keys())
        response_choice = random.choice(options)
        return response_choice, vocab_dict[response_choice]


class Player(Actor):

    def __init__(self, hp: int, weakness: str, level: int = 1):
        super().__init__(hp=hp, weakness=weakness)
        self.level = level
        self.xp = level_mapper[self.level]
        self.vocabulary = self.__build_vocabulary()

        self.current_enemy = None

    def __build_vocabulary(self) -> list:
        """Compile all known words based on level."""
        available_words = []
        for i in range(1, self.level + 1):
            available_words += vocab_dict[i].keys()
        return available_words

    def trigger_encounter(self, target: Enemy):
        """Set encounter state to True."""
        self.repartee(target=target)

    def check_level_up(self):
        """Checks current XP against requirements for leveling up."""
        if self.xp >= level_mapper[self.level + 1]:
            self.level += 1
            print(f"LEVEL UP: {self.level}")

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
            enemy_insult, enemy_response = target.respond()
            print(colorize("red", f"Your enemy said: {enemy_insult}!"))
            self.take_mental_damage(enemy_response)

        if self.hp <= 0:  # You died
            print(colorize("red", "You have been pwned!\nGAME OVER"))

        else:
            print("You have schooled your foe.")
            self.xp += target.xp  # Gain XP based on foe slain
            self.check_level_up()

    @staticmethod
    def respond() -> Tuple[int, str]:
        """Player enters verbal response from predefined list. Returns accepted response and insult type."""

        allowed_words = vocab_dict.keys()
        print(" ".join(allowed_words))
        player_input = input("Please enter your insult: ")

        # For testing
        # player_input = "fatso"

        while player_input.lower() not in allowed_words:
            print(f"Word not allowed! Please choose from the following: {' '.join(allowed_words)}")
            player_input = input("New insult: ")

        return vocab_dict[player_input]


if __name__ == "__main__":
    player = Player(hp=100, weakness=INTELLIGENCE)
    enemy = Enemy(hp=10, xp=50, weakness=PERSONALITY)

    player.trigger_encounter(enemy)
