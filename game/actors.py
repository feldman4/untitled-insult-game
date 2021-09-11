import random

from typing import Tuple
from pygments.console import colorize
from abc import ABCMeta, abstractmethod


insult_dict = {
    "idiot": (3, "intelligence"),
    "fatso": (5, "weight"),
    "streber": (7, "personality"),
}

level_mapper = {
    2: 30,
    3: 90,
    4: 270,
    5: 650,
    6: 1400,
}


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
        options = list(insult_dict.keys())
        response_choice = random.choice(options)
        return response_choice, insult_dict[response_choice]


class Player(Actor):

    def __init__(self, hp: int, weakness: str):
        super().__init__(hp=hp, weakness=weakness)
        self.level = 1
        self.xp = 0

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

        allowed_words = insult_dict.keys()
        print(" ".join(allowed_words))
        player_input = input("Please enter your insult: ")

        # For testing
        # player_input = "fatso"

        while player_input.lower() not in allowed_words:
            print(f"Word not allowed! Please choose from the following: {' '.join(allowed_words)}")
            player_input = input("New insult: ")

        return insult_dict[player_input]


if __name__ == "__main__":
    player = Player(hp=100, weakness="intelligence")
    enemy = Enemy(hp=10, xp=50, weakness="personality")

    player.trigger_encounter(enemy)
